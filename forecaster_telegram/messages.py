from inspect import cleandoc

from aiogram import html

from forecaster.schemas.user import User
from forecaster.const import CurrencyDymanicPeriod
from forecaster.schemas.currency import CurrencyData


def start_command_message(user: User) -> str:
    return cleandoc(f"""
        Привіт, {user.telegram.first_name}❕
        
        Я бот 🤖, який допоможе тобі слідкувати за змінами курсу валют.

        Ознайомся зі списком команд, які я підтримую 😉🚀:

        1️⃣ /help - Отримати інформацію про команди, які я підтримую.

        2️⃣ /actual_currency - Отримати актульний курс валюти {html.bold('UAH/USD')}.

        3️⃣ /forecast - Отримати прогноз курсу валюти {html.bold('UAH/USD')}.

        4️⃣ /currency_dynamics - Отримати інфорграфіку про зміни курсу валюти {html.bold('UAH/USD')}.

        5️⃣ /forecast_subscribe - Отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.

        6️⃣ /forecast_unsubscribe - Припинити отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.
    """)


def error_occurred_message() -> str:
    return cleandoc("""
        Вибач, але під час обробки твого запиту сталась помилка 😔
        Спробуй повторити запит трохи пізніше 😉🚀
    """)


def help_command_message() -> str:
    return cleandoc(f"""
        Я бот 🤖, який допоможе тобі:
                    
        ▶️ відслідковувати зміни курсу валют {html.bold('UAH/USD')}.
                    
        ▶️ дивитись історію змін курсу валют {html.bold('UAH/USD')}.
                    
        ▶️ отримувати інформацію про актуальний курс валют {html.bold('UAH/USD')}.
                    
        ▶️ отримувати прозноз стосовно майбутнього курсу валют {html.bold('UAH/USD')}.
                    
        ▶️ отримувати від мене повідомлення про прогноз зміни курсу валют {html.bold('UAH/USD')}.
        
        Нижче ⬇️, ти можеш ознайомитись з повним списком команд, які я підтримую 😉🚀:
                    
        1️⃣ /help - Отримати інформацію про команди, які я підтримую.

        2️⃣ /actual_currency - Отримати актульний курс валюти {html.bold('UAH/USD')}.

        3️⃣ /forecast - Отримати прогноз курсу валюти {html.bold('UAH/USD')}.

        4️⃣ /currency_dynamics - Отримати інфорграфіку про зміни курсу валюти {html.bold('UAH/USD')}.

        5️⃣ /forecast_subscribe - Отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.

        6️⃣ /forecast_unsubscribe - Припинити отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.
    """)


def actual_currency_data_not_exist_message() -> str:
    return cleandoc("""
        Вибач, проте станом на зараз немає актуальної інформації щодо курсу валют 😔
        Спробуй повторити запит трохи пізніше 😉🚀
    """)


def actual_currency_command_message(currecy_data: CurrencyData) -> str:
    return cleandoc(f"""
        Актуальний курс валюти {html.bold('UAH/USD')} станом на {html.bold(currecy_data.created_at.strftime("%d.%m.%Y"))}

        📊 Купівля: {html.bold(f"{round(currecy_data.buy, 2)} грн.")}

        📊 Продаж: {html.bold(f"{round(currecy_data.sell, 2)} грн.")}
    """)


def currency_data_by_period_caption(period: CurrencyDymanicPeriod) -> str:
    return cleandoc(f"""
        Інфографіка зміни курсу валюти {html.bold('UAH/USD')} за {period.value}
    """)


def forecast_command_message(
    *,
    sell_forecast: float,
    currecy_data: CurrencyData,
) -> str:
    return cleandoc(f"""
        Актуальний курс валюти {html.bold('UAH/USD')} станом на {html.bold(currecy_data.created_at.strftime("%d.%m.%Y"))}

        📊 Купівля: {html.bold(f"{round(currecy_data.buy, 2)} грн.")}

        📊 Продаж: {html.bold(f"{round(currecy_data.sell, 2)} грн.")}
                    
        Прогнозований курс валюти {html.bold('UAH/USD')}⬇️

        📊 Продаж: {html.bold(f"{round(sell_forecast, 2)} грн.")}
    """)


def forecast_command_actual_currency_data_not_exist_message() -> str:
    return cleandoc("""
        Вибач, проте станом на зараз немає актуальної інформації щодо курсу валют 😔

        Тому я не можу спрогнозувати динаміку курсу валют {html.bold('UAH/USD')} 📈☹️
                    
        Спробуй повторити запит трохи пізніше 😉🚀
    """)


def forecast_subscribe_command_subscription_already_exist_message() -> str:
    return cleandoc(f"""
        У тебе вже є активна підписка на отримання нотифікацій від мене з прогнозуванням курсу валюти {html.bold('UAH/USD')} 😃

        Нижче ⬇️, ти можеш ознайомитись з повним списком команд, які я підтримую 😉🚀:
                    
        1️⃣ /help - Отримати інформацію про команди, які я підтримую.

        2️⃣ /actual_currency - Отримати актульний курс валюти {html.bold('UAH/USD')}.

        3️⃣ /forecast - Отримати прогноз курсу валюти {html.bold('UAH/USD')}.

        4️⃣ /currency_dynamics - Отримати інфорграфіку про зміни курсу валюти {html.bold('UAH/USD')}.

        5️⃣ /forecast_subscribe - Отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.

        6️⃣ /forecast_unsubscribe - Припинити отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.
    """)


def forecast_subscribe_command_message() -> str:
    return cleandoc(f"""
        Вітаю 🎉
        Ти підписався на отримання щоденного прогнозу курсу валюти {html.bold('UAH/USD')} від мене 📈🚀

        Тепер я буду щодня відправляти тобі прогноз курсу валюти {html.bold('UAH/USD')} 📊
        
        Нижче ⬇️, ти можеш ознайомитись з повним списком команд, які я підтримую 😉🚀:
                    
        1️⃣ /help - Отримати інформацію про команди, які я підтримую.

        2️⃣ /actual_currency - Отримати актульний курс валюти {html.bold('UAH/USD')}.

        3️⃣ /forecast - Отримати прогноз курсу валюти {html.bold('UAH/USD')}.

        4️⃣ /currency_dynamics - Отримати інфорграфіку про зміни курсу валюти {html.bold('UAH/USD')}.

        5️⃣ /forecast_subscribe - Отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.

        6️⃣ /forecast_unsubscribe - Припинити отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.
    """)


def forecast_unsubscribe_command_active_subscription_not_exist_message() -> str:
    return cleandoc(f"""
        На жаль, у тебе ще немає активної підписки на прогнозування курсу валюти {html.bold('UAH/USD')} від мене 😔

        Надішли мені команду /forecast_subscribe, щоб отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')} 😃🚀
    """)


def forecast_unsubscribe_command_message() -> str:
    return cleandoc(f"""
        Мені дуже шкода, що ти вирішив відписатись від отримання щоденного прогнозу курсу валюти від мене 😔
        
        Твій запит успішно виконано ☹️
                    
        Нижче ⬇️, ти можеш ознайомитись з повним списком команд, які я підтримую 😉🚀:
                    
        1️⃣ /help - Отримати інформацію про команди, які я підтримую.

        2️⃣ /actual_currency - Отримати актульний курс валюти {html.bold('UAH/USD')}.

        3️⃣ /forecast - Отримати прогноз курсу валюти {html.bold('UAH/USD')}.

        4️⃣ /currency_dynamics - Отримати інфорграфіку про зміни курсу валюти {html.bold('UAH/USD')}.

        5️⃣ /forecast_subscribe - Отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.

        6️⃣ /forecast_unsubscribe - Припинити отримувати щоденний прогноз курсу валюти {html.bold('UAH/USD')}.
""")


def currency_forecasted_by_subscription_message(
    *,
    user: User,
    sell_forecast: float,
    currecy_data: CurrencyData,
) -> str:
    return cleandoc(f"""
        Привіт, {user.telegram.first_name} ❕

        Це твій щоденний прогноз курсу валюти {html.bold('UAH/USD')} від мене 😉

        Актуальний курс валюти {html.bold('UAH/USD')} станом на {html.bold(currecy_data.created_at.strftime("%d.%m.%Y"))}

        📊 Купівля: {html.bold(f"{round(currecy_data.buy, 2)} грн.")}

        📊 Продаж: {html.bold(f"{round(currecy_data.sell, 2)} грн.")}
                    
        Прогнозований курс валюти {html.bold('UAH/USD')}⬇️

        📊 Продаж: {html.bold(f"{round(sell_forecast, 2)} грн.")}
    """)
