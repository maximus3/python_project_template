import pytest

from database import create_session as real_create_session

from .database import tmp_database_engine, tmp_database_name
from .database.config import Session, prepare_db, remove_db
from .static import user_proxy_data


@pytest.fixture()
def prepare_db_env(mocker):
    mocker.patch('database.Session', Session)
    mocker.patch('config.cfg.DATABASE_NAME', tmp_database_name)
    mocker.patch('config.cfg.DATABASE_ENGINE', tmp_database_engine)
    prepare_db()
    yield
    remove_db()


@pytest.fixture()
def prepare_db_user_env(prepare_db_env):
    user_proxy_data()[0].create(**user_proxy_data()[2])
    yield


@pytest.fixture()
def create_session(prepare_db_env):
    return real_create_session
