
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from .proto import serialization_pb2

from .targets import TargetValue
from .comparison import ComparedValue
from .comparison import ComparedValueCollection
from .entity import EntityCollection
from .targets import TargetValueCollection
from .entity import Entity
from .extraction import ExtractedValueCollection
from .extraction import ExtractedValue
from .record import RecordContext


@dataclass
class Serialized:
  _proto: serialization_pb2.Serialized
  _reference_map: Mapping[str, Any]

  @property
  def data(self) -> Mapping[str, Any]:
    return self._proto.data
  @property
  def root(self) -> 'SerializedTypeOneOf':
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
    return self._proto.record_context
  @property
  def extracted_value(self) -> ExtractedValue:
    return self._proto.extracted_value
  @property
  def target_value(self) -> TargetValue:
    return self._proto.target_value
  @property
  def compared_value(self) -> ComparedValue:
    return self._proto.compared_value
  @property
  def entity(self) -> Entity:
    return self._proto.entity
  @property
  def extracted_value_collection(self) -> ExtractedValueCollection:
    return self._proto.extracted_value_collection
  @property
  def target_value_collection(self) -> TargetValueCollection:
    return self._proto.target_value_collection
  @property
  def compared_value_collection(self) -> ComparedValueCollection:
    return self._proto.compared_value_collection
  @property
  def entity_collection(self) -> EntityCollection:
    return self._proto.entity_collection

  def as_proto(self) -> serialization_pb2.SerializedTypeOneOf:
    return self._proto

  @staticmethod
  def from_proto(proto: serialization_pb2.SerializedTypeOneOf, reference_map: Mapping[str, Any]):
    return SerializedTypeOneOf(proto, reference_map)

