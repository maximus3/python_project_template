import typing as tp

from sqlalchemy.orm import Session

from app.database.connection import SessionManager
from app.database.models import BaseModel
from app.database.schemas import BaseModel as SchemaBaseModel


BaseProxyType = tp.TypeVar('BaseProxyType', bound='BaseProxy')


class BaseProxy:
    BASE_MODEL: tp.Type[BaseModel] = BaseModel
    SCHEMA_MODEL: tp.Type[SchemaBaseModel] = SchemaBaseModel

    def __init__(self, model: BaseModel):
        self.id = model.id

    def __eq__(self: BaseProxyType, other: object) -> bool:
        if not isinstance(other, BaseProxy):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(id={self.id!r})>'

    @classmethod
    def get(
        cls: tp.Type[BaseProxyType],
        session: Session = None,
        **kwargs: tp.Any,
    ) -> tp.Optional[BaseProxyType]:
        if session is None:
            with SessionManager().create_session() as new_session:
                return cls.get(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one_or_none()
        if model:
            return cls(model)
        return None

    @classmethod
    def get_expect(
        cls: tp.Type[BaseProxyType],
        session: Session = None,
        **kwargs: tp.Any,
    ) -> BaseProxyType:
        if session is None:
            with SessionManager().create_session() as new_session:
                return cls.get_expect(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one()
        return cls(model)

    @classmethod
    def get_model(
        cls: tp.Type[BaseProxyType],
        session: Session = None,
        **kwargs: tp.Any,
    ) -> BaseModel:
        if session is None:
            with SessionManager().create_session() as new_session:
                return cls.get_model(new_session, **kwargs)
        return session.query(cls.BASE_MODEL).filter_by(**kwargs).one()

    @classmethod
    def get_schema_model(
        cls: tp.Type[BaseProxyType],
        session: Session = None,
        **kwargs: tp.Any,
    ) -> SchemaBaseModel:
        if session is None:
            with SessionManager().create_session() as new_session:
                return cls.get_schema_model(new_session, **kwargs)
        model = session.query(cls.BASE_MODEL).filter_by(**kwargs).one()
        return cls.SCHEMA_MODEL.from_orm(model)

    @classmethod
    def get_all(
        cls: tp.Type[BaseProxyType],
        session: Session = None,
        **kwargs: tp.Any,
    ) -> list[BaseProxyType]:
        if session is None:
            with SessionManager().create_session() as new_session:
                return cls.get_all(new_session, **kwargs)
        data = []
        for model in session.query(cls.BASE_MODEL).filter_by(**kwargs).all():
            data.append(cls(model))
        return data

    @classmethod
    def get_or_create(
        cls: tp.Type[BaseProxyType], session: Session = None, **kwargs: tp.Any
    ) -> tp.Optional[BaseProxyType]:
        if session is None:
            with SessionManager().create_session() as new_session:
                model = cls.get(new_session, **kwargs)
                if model:
                    return model
                if not cls.create(new_session, **kwargs):
                    return None
            with SessionManager().create_session() as new_session:
                return cls.get(new_session, **kwargs)
        return None

    @classmethod
    def create(
        cls: tp.Type[BaseProxyType],
        session: Session = None,
        **kwargs: tp.Any,
    ) -> bool:
        if session is None:
            with SessionManager().create_session() as new_session:
                return cls.create(new_session, **kwargs)
        model = cls.BASE_MODEL(**kwargs)
        session.add(model)
        return True

    def update(
        self: BaseProxyType,
        session: Session = None,
        **kwargs: tp.Any,
    ) -> tp.Optional[BaseProxyType]:
        if session is None:
            with SessionManager().create_session() as new_session:
                return self.update(new_session, **kwargs)
        model = (
            session.query(self.BASE_MODEL).filter_by(id=self.id).one_or_none()
        )
        if model is None:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key) and hasattr(self, key):
                setattr(model, key, value)
                setattr(self, key, value)
            else:
                return None
        session.add(model)
        return self

    def get_me(self: BaseProxyType, session: Session) -> BaseModel:
        return session.query(self.BASE_MODEL).get(self.id)
