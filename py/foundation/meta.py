from typing import Dict, Tuple, Type, cast

from abc import ABCMeta

foundation_types: Dict[str, Type['FoundationType']] = {}

class FoundationType():
  """
  A superclass that registers foundation types
  (including non-entity types)
  """
  def __init_subclass__(cls) -> None:
    foundation_types[cls.__name__] = cls