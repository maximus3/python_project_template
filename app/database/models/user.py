from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    username = Column(
        'username',
        TEXT,
        nullable=False,
        unique=True,
        index=True,
        doc='Username for authentication.',
    )
    password = Column(
        'password',
        TEXT,
        nullable=False,
        index=True,
        doc='Hashed password.',
    )
