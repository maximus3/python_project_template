from contextlib import contextmanager
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.orm import sessionmaker

from config import cfg
from database.models import Base

engine = sa.create_engine(cfg.DATABASE_ENGINE)
Session = sessionmaker(bind=engine)


@contextmanager
def create_session(**kwargs: Any) -> SessionType:
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


def create_all() -> None:
    Base.metadata.create_all(engine)
