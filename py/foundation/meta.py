from typing import Dict, Tuple, Type, cast

from abc import ABCMeta

foundation_types: Dict[str, 'FoundationType'] = {}

class FoundationType(ABCMeta):
  """
  A Metaclass that registers all foundation types with 
  """
  def __new__(meta: Type[type], name: str, bases: Tuple, attrs: Dict) -> 'FoundationType':
    # get ABCMeta version
    cls = cast(FoundationType, ABCMeta.__new__(meta, name, bases, attrs))

    # register foundation type
    foundation_types[name] = cls

    # return ABCMeta version
    return cls