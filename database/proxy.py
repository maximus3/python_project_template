from typing import Any, Optional, Type, TypeVar

from . import create_session
from .models import BaseModel, User

BaseProxyType = TypeVar('BaseProxyType', bound='BaseProxy')


class BaseProxy:
    BASE_MODEL: Type[BaseModel] = BaseModel

    def __init__(self, model: BaseModel):
        self.id = model.id

    @classmethod
    def get(
        cls: Type[BaseProxyType], **kwargs: Any
    ) -> Optional[BaseProxyType]:
        with create_session() as session:
            model = (
                session.query(cls.BASE_MODEL).filter_by(**kwargs).one_or_none()
            )
            if model:
                return cls(model)
            return None

    @classmethod
    def get_expect(cls: Type[BaseProxyType], **kwargs: Any) -> BaseProxyType:
        with create_session() as session:
            model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one()
            return cls(model)

    @classmethod
    def get_all(
        cls: Type[BaseProxyType], **kwargs: Any
    ) -> list[BaseProxyType]:
        with create_session() as session:
            data = []
            for model in (
                session.query(cls.BASE_MODEL).filter_by(**kwargs).all()
            ):
                data.append(cls(model))
            return data

    @classmethod
    def create(cls: Type[BaseProxyType], **data_dict: Any) -> BaseProxyType:
        with create_session() as session:
            model = cls.BASE_MODEL(**data_dict)
            session.add(model)
            return cls(model)

    def update(
        self: BaseProxyType, **data_dict: Any
    ) -> Optional[BaseProxyType]:
        with create_session() as session:
            model = (
                session.query(self.BASE_MODEL)
                .filter_by(id=self.id)
                .one_or_none()
            )
            if model is None:
                return None
            for key, value in data_dict.items():
                if hasattr(model, key) and hasattr(self, key):
                    setattr(model, key, value)
                    setattr(self, key, value)
                else:
                    return None
            session.add(model)
            return self


class UserProxy(BaseProxy):
    BASE_MODEL = User

    def __init__(self, user: User) -> None:
        super().__init__(user)
        self.username = user.username
        self.password = user.password
