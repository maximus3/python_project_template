from app.database.models import User
from app.database.schemas import UserSchema

from .base import BaseProxy


class UserProxy(BaseProxy):
    BASE_MODEL = User
    SCHEMA_MODEL = UserSchema

    def __init__(self, user: User) -> None:
        super().__init__(user)
        self.username = user.username
        self.password = user.password
