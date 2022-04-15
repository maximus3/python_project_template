import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True

    id = sa.Column(
        sa.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    created_at = sa.Column(
        sa.DateTime, nullable=False, default=dt.datetime.now
    )
    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=dt.datetime.now,
        onupdate=dt.datetime.now,
    )

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'


class User(BaseModel):
    __tablename__ = 'user'

    username = sa.Column(sa.String)
    password = sa.Column(sa.String)
