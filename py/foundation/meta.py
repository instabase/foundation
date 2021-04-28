from typing import Dict, Type
from typing_extensions import Protocol

from abc import ABC, abstractmethod

foundation_types: Dict[str, Type['FoundationType']] = {}

class FoundationType(Protocol):
  @property
  @abstractmethod
  def type(self) -> str: ...

  def __init_subclass__(cls) -> None:
    foundation_types[cls.__name__] = cls

  # @abstractmethod
  # def as_dict(self) -> Dict[str, Any]: ...

  # @staticmethod
  # @abstractmethod
  # def from_dict(type_as_dict: Dict) -> 'FoundationType': ...

# class DataGetter(ABC):
#   @abstractmethod
#   def get(self, key: str) -> Any:
#     ...
# class FoundationType(ABC):
#   """
#   A superclass that registers foundation types
#   (including non-entity types) that might show up
#   in the "data" k/v store
#   """
#   id: str
#   _data: DataGetter

#   def __init_subclass__(cls) -> None:
#     foundation_types[cls.__name__] = cls
