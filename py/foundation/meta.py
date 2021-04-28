from typing import Dict, Tuple, Type, cast, Any

from abc import ABC, abstractmethod

foundation_types: Dict[str, Type['FoundationType']] = {}

class DataGetter(ABC):
  @abstractmethod
  def get(self, key: str) -> Any:
    ...
class FoundationType(ABC):
  """
  A superclass that registers foundation types
  (including non-entity types) that might show up
  in the "data" k/v store
  """
  id: str
  _data: DataGetter

  def __init_subclass__(cls) -> None:
    foundation_types[cls.__name__] = cls
