import io
import datetime

import joblib
import pandas as pd
import xgboost as xgb
from sqlalchemy import insert, select, desc, asc, cast, Date
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error

from forecaster.const import MINUTE
from forecaster.services import db
from forecaster.schemas.currency import CurrencyDataToPredict
from forecaster.models.ml import TrainedModel
from forecaster.utilities.retry import retry
from forecaster.utilities.logging import logger
from forecaster.ml.sql import (
    sql_get_all_currency_data,
)


RANDOM_STATE = 42

TEST_SIZE = 0.2

DATE_SHIFT = 7

RSI_WINDOW_LENGTH = 14

DEFAULT_TRAINING_PARAMS = {
    'max_depth': [3, 5, 7, 9, 11],
    'n_estimators': [50, 100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
}


@retry(exceptions=[Exception], tries=3, delay=1, backoff=0.5)
def load_currency_data_to_train_model() -> pd.DataFrame:
    return pd.read_sql(
        sql=sql_get_all_currency_data(date_to=datetime.datetime.today().date()),
        con=db.engine,
    )


def transform_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['year'] = dataframe['created_at'].dt.year
    dataframe['month'] = dataframe['created_at'].dt.month
    dataframe['day_of_week'] = dataframe['created_at'].dt.dayofweek

    dataframe.drop('created_at', axis=1, inplace=True)

    return dataframe


def save_model(
    model, 
    mse: float, 
    training_params: dict[str, list[int | float | str]],
) -> None:
    buffer = io.BytesIO()
    joblib.dump(model, buffer)
    buffer.seek(0)
    try:
        db.Session.execute(
            insert(TrainedModel).values(
                mse=mse,
                model=buffer.getvalue(),
                training_params=training_params,
            )
        )
        db.Session.commit()
        logger.info('[FORECASTER][ML] Saved new trained model to database')
    except Exception:
        logger.exception(
            '[FORECASTER][ML] Failed to save new trained model to database'
        )


def load_model(
    latest: bool = True,
    after_date: datetime.date | None = None
):
    if latest and after_date:
        raise ValueError(
            "You can not fetch latest model if \"after_date\" "
            "param is passed. Choose the one "
            "option \"latest\" or \"after_date\""
        )
    query = select(TrainedModel.model)
    if latest:
        query = query.order_by(desc(TrainedModel.id))
    else:
        assert after_date is not None
        query = (
            query.where(TrainedModel.created_at >= cast(after_date, Date))
            .order_by(asc(TrainedModel.id))
        )
    query_result = db.Session.execute(query)
    try:
        model = query_result.mappings().first()
    except Exception:
        logger.exception('[FORECASTER][ML] Failed to load model')
    
    if model is None:
        logger.error('[FORECASTER][ML] No model found in database')
        return None

    model_buffer = io.BytesIO(model["model"])
    return joblib.load(model_buffer)


async def async_load_model(
    latest: bool = True,
    after_date: datetime.date | None = None
):
    if latest and after_date:
        raise ValueError(
            "You can not fetch latest model if \"after_date\" "
            "param is passed. Choose the one "
            "option \"latest\" or \"after_date\""
        )
    query = select(TrainedModel.model)
    if latest:
        query = query.order_by(desc(TrainedModel.id))
    else:
        assert after_date is not None
        query = (
            query.where(TrainedModel.created_at >= cast(after_date, Date))
            .order_by(asc(TrainedModel.id))
        )
    async with db.async_sessionmaker.begin() as db_session:
        query_result = await db_session.execute(query)
    try:
        model = query_result.mappings().first()
    except Exception:
        logger.exception('[FORECASTER][ML] Failed to load model')
    
    if model is None:
        logger.error('[FORECASTER][ML] No model found in database')
        return None

    model_buffer = io.BytesIO(model["model"])
    return joblib.load(model_buffer)


def train_model(dataframe: pd.DataFrame):
    query_result = db.Session.execute(
        select(TrainedModel.training_params).order_by(
            desc(TrainedModel.id)
        )
    )
    try:
        training_params = query_result.scalars().first()
    except Exception:
        training_params = DEFAULT_TRAINING_PARAMS

    if training_params is None:
        training_params = DEFAULT_TRAINING_PARAMS

    X = dataframe[['buy', 'year', 'month', 'day_of_week']]
    y = dataframe['sell']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=TEST_SIZE, 
        random_state=RANDOM_STATE
    )

    model = xgb.XGBRegressor(objective='reg:squarederror')
    grid_search = GridSearchCV(
        estimator=model, 
        param_grid=training_params, 
        cv=3, 
        scoring='neg_mean_squared_error', 
        verbose=1
    )
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    new_best_params = {
        key: [value] for key, value 
        in grid_search.best_params_.items()
    }

    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    save_model(model=best_model, mse=mse, training_params=new_best_params)


def run_model_training() -> None:
    try:
        logger.info('[FORECASTER][ML] START MODEL TRAINING')
        training_data = load_currency_data_to_train_model()
        logger.info('[FORECASTER][ML] LOADED DATA TO TRAIN MODEL')
        transformed_data = transform_data(training_data)
        logger.info('[FORECASTER][ML] TRANSFORMED DATA TO TRAIN MODEL')
        train_model(transformed_data)
        logger.info('[FORECASTER][ML] MODEL RETRAINED SUCCESSFULLY')
    except Exception:
        logger.exception('[FORECASTER][ML] Failed to retrain model')


async def get_prediction(currency_data: CurrencyDataToPredict) -> float:
    dump_data = currency_data.model_dump(mode="json")

    data_to_predict = pd.DataFrame(dump_data, index=[0])

    data_to_predict['created_at'] = pd.to_datetime(data_to_predict['created_at'])
    data_to_predict['buy'] = data_to_predict['buy_price']
    data_to_predict.drop('buy_price', axis=1, inplace=True)
    data_to_predict['buy'] = data_to_predict['buy'].astype(float)

    transformed_data = transform_data(data_to_predict)

    model = await async_load_model(latest=True)
    prediction = model.predict(transformed_data)

    return sum(prediction) / len(prediction)
