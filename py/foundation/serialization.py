"""
Functions related to serialization of Foundation types
"""

from typing import Dict

from .entity import Entity

def dumps(entities: Dict[str, Entity]) -> bytes:
  ...

def loads(serialized_entities: bytes) -> Dict[str, Entity]:
  ...