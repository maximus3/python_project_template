import datetime as dt

import pytest

from config.departments import departments
from database import proxy

from .database import tmp_database_name
from .database.config import Session, prepare_db, remove_db


@pytest.fixture()
def prepare_db_env(mocker):
    mocker.patch('database.Session', Session)
    mocker.patch('config.cfg.DATABASE_NAME', tmp_database_name)
    mocker.patch(
        'config.cfg.DATABASE_ENGINE', 'sqlite:///' + tmp_database_name
    )
    prepare_db()
    yield
    remove_db()
