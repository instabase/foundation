from typing import Optional, Iterable
from dataclasses import dataclass

from .geometry import BBox
from .proto import entity_pb2

@dataclass
class Entity:
  _proto: entity_pb2.Entity

  @property
  def id(self) -> str:
    return self._proto.id

  @property
  def bbox(self) -> BBox:
    return BBox(self._proto.bbox)

  @property
  def field_name(self) -> str:
    return self._proto.field_name

  @property
  def serialized_value(self) -> bytes:
    return self._proto.serialized_value

@dataclass
class EntityCollection:
  _proto: entity_pb2.EntityCollection

  @property
  def id(self) -> str:
    return self._proto.id
  
  def get_entities(self) -> Optional[Iterable[Entity]]:
    ...