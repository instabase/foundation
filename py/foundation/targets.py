
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from .proto import targets_pb2

from .geometry import BBox


@dataclass
class TargetValue:
  _proto: targets_pb2.TargetValue
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @property
  def field_name(self) -> 'str':
    return self._proto.field_name
  @property
  def bbox(self) -> BBox:
    return BBox(self._proto.bbox, self._reference_map)
  @property
  def value(self) -> 'str':
    return self._proto.value

  def as_proto(self) -> targets_pb2.TargetValue:
    return self._proto

  @staticmethod
  def from_proto(proto: targets_pb2.TargetValue, reference_map: Mapping[str, Any]):
    return TargetValue(proto, reference_map)



@dataclass
class TargetValueCollection:
  _proto: targets_pb2.TargetValueCollection
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @property
  def target_values(self) -> Iterable['TargetValue']:
    yield from (self._reference_map[i] for i in self._proto.target_value_ids)


  def as_proto(self) -> targets_pb2.TargetValueCollection:
    return self._proto

  @staticmethod
  def from_proto(proto: targets_pb2.TargetValueCollection, reference_map: Mapping[str, Any]):
    return TargetValueCollection(proto, reference_map)

