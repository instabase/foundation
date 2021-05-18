
from typing import Any, Mapping, Union
from dataclasses import dataclass

from .proto import serialization_pb2

from .comparison import ComparedValueCollection
from .targets import TargetValueCollection
from .extraction import ExtractedValueCollection
from .entity import EntityCollection
from .entity import Entity
from .extraction import ExtractedValue
from .record import RecordContext
from .comparison import ComparedValue
from .targets import TargetValue

SerializedTypeOneOf = Union[
  RecordContext,
  ExtractedValue,
  TargetValue,
  ComparedValue,
  Entity,
  ExtractedValueCollection,
  TargetValueCollection,
  ComparedValueCollection,
  EntityCollection
]
@dataclass
class Serialized(Mapping[str, SerializedTypeOneOf]):
  _proto: serialization_pb2.Serialized

  @property
  def root(self) -> SerializedTypeOneOf:
    return self[self._proto.root_id]

  @property
  def foundation_type_version(self) -> 'int':
    return self._proto.foundation_type_version

  def __getitem__(self, k: str) -> SerializedTypeOneOf:
      item = self._proto.data[k]
      item_type = item.WhichOneof("serialized_type_one_of")
      return None

  def as_proto(self) -> serialization_pb2.Serialized:
    return self._proto

  @staticmethod
  def from_proto(proto: serialization_pb2.Serialized, reference_map: Mapping[str, Any]):
    return Serialized(proto, reference_map)