from sqlalchemy import NullPool, Engine, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker as alchemy_async_sessionmaker,
)

from forecaster.config import settings
from forecaster.utilities.logging import logger


def create_async_db_engine(
    db_url: str,
    max_connections: int,
    debug: bool = False,
    timeout=5,
    **kwargs,
) -> AsyncEngine:
    if not debug:
        try:
            engine = create_async_engine(
                url=db_url,
                future=True,
                poolclass=NullPool,
                connect_args={**kwargs},
            )
            logger.info("[DB] Created NullPool engine")
        except Exception:
            engine = create_async_engine(
                url=db_url,
                pool_size=max_connections,
                future=True,
                pool_pre_ping=True,
                pool_recycle=3600,
                timeout=timeout,
            )
            logger.info("[DB] Failed to create NullPool engine, creating pool")
        return engine
    else:
        try:
            return create_async_engine(
                url=db_url,
                future=True,
                poolclass=NullPool,
                connect_args={'timeout': timeout, **kwargs},
            )
        except Exception:
            return create_async_engine(
                url=db_url,
                pool_size=max_connections,
                future=True,
                pool_pre_ping=True,
                pool_recycle=3600,
            )


def create_db_engine(
    db_url: str,
    max_connections: int,
    timeout=5,
    debug: bool = True,
    **kwargs,
) -> Engine:
    if not debug:
        try:
            engine = create_engine(
                url=db_url,
                poolclass=NullPool,
                connect_args={**kwargs},
            )
            logger.info("[JE] Created NullPool engine")
        except Exception:
            engine = create_engine(
                url=db_url,
                pool_size=max_connections,
                pool_pre_ping=True,
                pool_recycle=3600,
                timeout=timeout,
            )
            logger.exception("[JE] Failed to create NullPool engine, creating pool")
        return engine
    else:
        try:
            return create_engine(
                url=db_url,
                poolclass=NullPool,
                timeout=timeout,
                connect_args={**kwargs},
            )
        except Exception:
            return create_engine(
                url=db_url,
                pool_size=max_connections,
                pool_pre_ping=True,
                pool_recycle=3600,
            )


# Async DB API

async_engine = create_async_db_engine(
    db_url=settings.async_db_url,
    max_connections=settings.db_max_connections,
    debug=settings.debug,
    timeout=10,
)


async_sessionmaker = alchemy_async_sessionmaker(
    async_engine,
    class_=AsyncSession,
)

# Not Async DB API

engine = create_db_engine(
    db_url=settings.db_url,
    max_connections=settings.db_max_connections,
    debug=settings.debug,
    timeout=10,
)

Session = scoped_session(sessionmaker())

Session.configure(bind=engine)
