from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from itertools import count

from pydantic import BaseModel
from pydantic.generics import GenericModel

from gateway.data.domain.errors import DiscardedEntityError

T = TypeVar("T")


class ValueObjectModel(GenericModel, Generic[T]):
    value: T

    class Config:
        frozen = True


class EntityModel(BaseModel):
    id: int


class ValueObject(Generic[T]):
    def __init__(self, value: T, _type: T) -> None:
        self._type = _type
        self._value = value

        self._checkType()

    def __repr__(self) -> str:
        return "{cls}<value={value}>".format(
            cls=self.__class__.__name__,
            value=self._value,
        )

    def __eq__(self, o: "ValueObject") -> bool:
        return isinstance(o, ValueObject) and self._value == o.value

    def __hash__(self) -> int:
        return hash(self._value)

    def _checkType(self):
        if not isinstance(self._value, self._type):
            raise TypeError(
                "value got an invalid type '{type}', expected '{expected}'".format(
                    type=self._value.__class__.__name__,
                    expected=self._type.__name__,
                )
            )

    @property
    def value(self) -> T:
        return self._value


class Entity(ABC):

    _entity_generator = count()

    def __init__(self, id: int) -> None:
        self._id = id
        self._discarded = False

    @classmethod
    def setGeneratorValue(cls, value: int) -> None:
        cls._entity_generator = count(value)

    @classmethod
    def incr(cls) -> int:
        return next(cls._entity_generator)

    @classmethod
    @abstractmethod
    def create(
        cls,
        *args,
        **kwargs,
    ) -> "Entity":

        _id = cls.incr()
        return cls(_id, *args, **kwargs)

    @property
    def discarded(self) -> bool:
        return self._discarded

    @property
    def id(self) -> int:
        return self._id

    def checkDiscarded(self) -> None:
        if self._discared:
            raise DiscardedEntityError()


class EntityInterface:
    """interface to query methods"""

    class Queries:
        pass
