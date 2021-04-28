"""
Functions related to serialization of Foundation types
"""

from typing import Dict, Union

from .entity import Entity

def dumps(entities: Dict[str, Entity]) -> bytes:
  # flat: Dict[str, Dict[str, Union[str, int, bool]]] = {
  #   k: 
  # }
  ...

def loads(serialized_entities: bytes) -> Dict[str, Entity]:
  ...