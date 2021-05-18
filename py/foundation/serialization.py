
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from .proto import serialization_pb2

from .extraction import ExtractedValue
from .targets import TargetValue
from .entity import Entity
from .targets import TargetValueCollection
from .comparison import ComparedValue
from .record import RecordContext
from .comparison import ComparedValueCollection
from .extraction import ExtractedValueCollection
from .entity import EntityCollection


@dataclass
class Serialized:
  _proto: serialization_pb2.Serialized
  _reference_map: Mapping[str, Any]

  @property
  def data(self) -> Mapping[str, Any]:
    return self._proto.data
  @property
  def root(self) -> SerializedTypeOneOf:
    return self._reference_map[self._proto.root_id]

  @property
  def foundation_type_version(self) -> int:
    return self._proto.foundation_type_version

  def as_proto(self) -> serialization_pb2.Serialized:
    return self._proto

  @staticmethod
  def from_proto(proto: serialization_pb2.Serialized, reference_map: Mapping[str, Any]):
    return Serialized(proto, reference_map)



@dataclass
class SerializedTypeOneOf:
  _proto: serialization_pb2.SerializedTypeOneOf
  _reference_map: Mapping[str, Any]

  @property
  def record_context(self) -> RecordContext:
    return RecordContext(self._proto.record_context, self._reference_map)
  @property
  def extracted_value(self) -> ExtractedValue:
    return ExtractedValue(self._proto.extracted_value, self._reference_map)
  @property
  def target_value(self) -> TargetValue:
    return TargetValue(self._proto.target_value, self._reference_map)
  @property
  def compared_value(self) -> ComparedValue:
    return ComparedValue(self._proto.compared_value, self._reference_map)
  @property
  def entity(self) -> Entity:
    return Entity(self._proto.entity, self._reference_map)
  @property
  def extracted_value_collection(self) -> ExtractedValueCollection:
    return ExtractedValueCollection(self._proto.extracted_value_collection, self._reference_map)
  @property
  def target_value_collection(self) -> TargetValueCollection:
    return TargetValueCollection(self._proto.target_value_collection, self._reference_map)
  @property
  def compared_value_collection(self) -> ComparedValueCollection:
    return ComparedValueCollection(self._proto.compared_value_collection, self._reference_map)
  @property
  def entity_collection(self) -> EntityCollection:
    return EntityCollection(self._proto.entity_collection, self._reference_map)

  def as_proto(self) -> serialization_pb2.SerializedTypeOneOf:
    return self._proto

  @staticmethod
  def from_proto(proto: serialization_pb2.SerializedTypeOneOf, reference_map: Mapping[str, Any]):
    return SerializedTypeOneOf(proto, reference_map)

