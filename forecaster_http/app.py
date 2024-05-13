from fastapi import FastAPI

from forecaster.config import settings
from forecaster_http.routes import health
from forecaster_http.routes import currency
from forecaster_http.routes import forecast


def make_app() -> None:
    app = FastAPI(
        debug=settings.debug,
        title=settings.app_name,
        version=settings.app_version,
        docs_url='/docs' if settings.debug else None,
        redoc_url='/redoc' if settings.debug else None,
        openapi_url='/openapi.json' if settings.debug else None,
    )
    app.include_router(health.router, tags=['health'])
    app.include_router(currency.router, tags=['currency'])
    app.include_router(forecast.router, tags=['forecast'])

    return app


web = make_app()
