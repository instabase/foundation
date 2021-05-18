
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from .proto import extraction_pb2

from .entity import Entity


@dataclass
class ExtractedValue:
  _proto: extraction_pb2.ExtractedValue
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @property
  def field_name(self) -> 'str':
    return self._proto.field_name
  @property
  def type(self) -> 'str':
    return self._proto.type
  @property
  def serialized_value(self) -> 'bytes':
    return self._proto.serialized_value
  @property
  def entitys(self) -> Iterable[Entity]:
    yield from (self._reference_map[i] for i in self._proto.entity_ids)


  def as_proto(self) -> extraction_pb2.ExtractedValue:
    return self._proto

  @staticmethod
  def from_proto(proto: extraction_pb2.ExtractedValue, reference_map: Mapping[str, Any]):
    return ExtractedValue(proto, reference_map)



@dataclass
class ExtractedValueCollection:
  _proto: extraction_pb2.ExtractedValueCollection
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @property
  def extracted_values(self) -> Iterable['ExtractedValue']:
    yield from (self._reference_map[i] for i in self._proto.extracted_value_ids)


  def as_proto(self) -> extraction_pb2.ExtractedValueCollection:
    return self._proto

  @staticmethod
  def from_proto(proto: extraction_pb2.ExtractedValueCollection, reference_map: Mapping[str, Any]):
    return ExtractedValueCollection(proto, reference_map)

