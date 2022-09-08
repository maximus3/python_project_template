import typing as tp
from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls) -> 'SessionManager':
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(bind=self.engine)

    # def get_async_session_maker(self) -> sessionmaker:
    #     return sessionmaker(
    #         self.async_engine, class_=AsyncSession, expire_on_commit=False
    #     )

    def refresh(self) -> None:
        settings = get_settings()
        self.engine = sa.create_engine(settings.database_uri_sync)
        # self.async_engine = create_async_engine(
        #     settings.database_uri, echo=True, future=True
        # )

    @contextmanager
    def create_session(self, **kwargs: tp.Any) -> Session:
        with self.get_session_maker()(**kwargs) as new_session:
            try:
                yield new_session
                new_session.commit()
            except Exception:
                new_session.rollback()
                raise
            finally:
                new_session.close()

    # @contextmanager
    # async def create_async_session(self, **kwargs: tp.Any) -> Session:
    #     async with self.get_async_session_maker()(**kwargs) as new_session:
    #         try:
    #             yield new_session
    #             new_session.commit()
    #         except Exception:
    #             new_session.rollback()
    #             raise
    #         finally:
    #             new_session.close()
