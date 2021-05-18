
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from .proto import comparison_pb2

from .targets import TargetValue
from .extraction import ExtractedValue


@dataclass
class ComparedValue:
  _proto: comparison_pb2.ComparedValue
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @property
  def target_value(self) -> TargetValue:
    return self._reference_map[self._proto.target_value_id]

  @property
  def extracted_value(self) -> ExtractedValue:
    return self._reference_map[self._proto.extracted_value_id]

  @property
  def score(self) -> 'float':
    return self._proto.score
  @property
  def message(self) -> 'str':
    return self._proto.message

  def as_proto(self) -> comparison_pb2.ComparedValue:
    return self._proto

  @staticmethod
  def from_proto(proto: comparison_pb2.ComparedValue, reference_map: Mapping[str, Any]):
    return ComparedValue(proto, reference_map)



@dataclass
class ComparedValueCollection:
  _proto: comparison_pb2.ComparedValueCollection
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @property
  def compared_values(self) -> Iterable['ComparedValue']:
    yield from (self._reference_map[i] for i in self._proto.compared_value_ids)


  def as_proto(self) -> comparison_pb2.ComparedValueCollection:
    return self._proto

  @staticmethod
  def from_proto(proto: comparison_pb2.ComparedValueCollection, reference_map: Mapping[str, Any]):
    return ComparedValueCollection(proto, reference_map)

