from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app.common.config import settings
from src.app.errors.exceptions import (
    DatabaseEngineAlreadyClosedEx,
    SessionMakerIsNotInitializedEx,
)


class MySQLDatabaseSessionManager(object):
    def __init__(self):
        self._engine: AsyncEngine = None
        self._sessionmaker: async_sessionmaker = None

    def init_app(self):
        # create engine
        self._engine = create_async_engine(
            "mysql+asyncmy://{user}:{passwd}@{host}:{port}/{db}?charset=utf8mb4".format(
                user=settings.DB_USER,
                passwd=settings.DB_PASS,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                db=settings.DB_NAME,
            ),
            echo=settings.DB_ECHO,
            pool_recycle=settings.DB_POOL_RECYCLE,
            pool_pre_ping=settings.DB_POOL_PRE_PING,
        )
        # session maker
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def close(self):
        if self._engine is None:
            raise DatabaseEngineAlreadyClosedEx()

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise SessionMakerIsNotInitializedEx()

        session = self._sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


mysql_session_manager = MySQLDatabaseSessionManager()


def get_mysql_session_manager():
    return mysql_session_manager


# use it with Depends
async def get_db_session():
    async with mysql_session_manager.session() as session:
        yield session
