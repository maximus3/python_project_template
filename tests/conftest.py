# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

import typing as tp
from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.command import upgrade
from alembic.config import Config

# from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.config import get_settings
from app.database.connection import SessionManager
from app.database.models import User
from app.database.proxy import UserProxy
from app.database.schemas import UserSchema
from tests.utils import DPSClass, UserData, make_alembic_config

# @pytest.fixture(scope='session')
# def event_loop():
#     """
#     Creates event loop for tests.
#     """
#     loop = new_event_loop()
#     set_event_loop(loop)
#
#     yield loop
#     loop.close()


@pytest.fixture()
def postgres() -> str:  # type: ignore
    """
    Создает временную БД для запуска теста.
    """
    settings = get_settings()

    tmp_name = '.'.join([uuid4().hex, 'pytest'])
    settings.POSTGRES_DB = tmp_name
    environ['POSTGRES_DB'] = tmp_name

    tmp_url = settings.database_uri_sync
    if not database_exists(tmp_url):
        create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


# @pytest.fixture()
# def postgres_engine(postgres):
#     """
#     SQLAlchemy engine, bound to temporary database.
#     """
#     engine = create_engine(postgres)
#     try:
#         yield engine
#     finally:
#         engine.dispose()


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(
        config='',
        name='alembic',
        pg_url=postgres,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)


@pytest.fixture
def migrated_postgres(alembic_config: Config):
    """
    Проводит миграции.
    """
    upgrade(alembic_config, 'head')


@pytest.fixture
def create_session(  # type: ignore
    postgres, migrated_postgres, manager: SessionManager = SessionManager()
) -> tp.Callable:  # type: ignore
    """
    Returns a class object with which you can create a new session to connect to the database.
    """
    manager.refresh()
    yield manager.create_session


@pytest.fixture
def user_data():
    return UserData(username='username', password='password')


@pytest.fixture
def dps_user(user_data) -> DPSClass:
    return DPSClass(data=user_data, proxy=UserProxy, schema=UserSchema)


@pytest.fixture
def created_dps_user(create_session, dps_user) -> DPSClass:
    with create_session() as session:
        user = User(
            username=dps_user.data.username, password=dps_user.data.password
        )
        session.add(user)
    return DPSClass(
        data=dps_user.data, proxy=dps_user.proxy, schema=dps_user.schema
    )
