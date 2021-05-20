
from typing import Optional, Iterable, Any, Mapping, Dict
from dataclasses import dataclass
import itertools

from foundation.proto import targets_pb2

from foundation.geometry import BBox


@dataclass
class TargetValue:
  _proto: targets_pb2.TargetValue

  @property
  def id(self) -> 'str':
    return self._proto.id
  @id.setter
  def id(self, new_obj: 'str') -> None:
    self._proto.id = new_obj
    
  @property
  def field_name(self) -> 'str':
    return self._proto.field_name
  @field_name.setter
  def field_name(self, new_obj: 'str') -> None:
    self._proto.field_name = new_obj
    
  @property
  def bbox(self) -> BBox:
    return BBox(self._proto.bbox)
  @bbox.setter
  def bbox(self, new_obj: BBox) -> None:
    self._proto.bbox.page_index = new_obj._proto.page_index
    self._proto.bbox.rectangle.ix.a = new_obj._proto.rectangle.ix.a
    self._proto.bbox.rectangle.ix.b = new_obj._proto.rectangle.ix.b
    self._proto.bbox.rectangle.iy.a = new_obj._proto.rectangle.iy.a
    self._proto.bbox.rectangle.iy.b = new_obj._proto.rectangle.iy.b
  @property
  def value(self) -> 'str':
    return self._proto.value
  @value.setter
  def value(self, new_obj: 'str') -> None:
    self._proto.value = new_obj
    

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from []

  def as_proto(self) -> targets_pb2.TargetValue:
    return self._proto

  @staticmethod
  def from_proto(proto: targets_pb2.TargetValue, reference_map: Dict[str, Any] = None) -> 'TargetValue':
    return TargetValue(proto)



@dataclass
class TargetValueCollection:
  _proto: targets_pb2.TargetValueCollection
  _reference_map: Dict[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @id.setter
  def id(self, new_obj: 'str') -> None:
    self._proto.id = new_obj
    
  @property
  def target_values(self) -> Iterable['TargetValue']:
    yield from (self._reference_map[i] for i in self._proto.target_value_ids)
  @target_values.setter
  def target_values(self, new_obj: Iterable['TargetValue']) -> None:
    # TODO(erick): check to make sure object is a valid foundation type
    del self._proto.target_value_ids[:]
    for obj in new_obj:
      if not isinstance(obj, TargetValue):
        raise TypeError("target_value element must be a 'TargetValue', not {}".format(type(obj)))
      self._proto.target_value_ids.append(obj.id)
      self._reference_map[obj.id] = obj


  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain(self._proto.target_value_ids)

  def as_proto(self) -> targets_pb2.TargetValueCollection:
    return self._proto

  @staticmethod
  def from_proto(proto: targets_pb2.TargetValueCollection, reference_map: Dict[str, Any]) -> 'TargetValueCollection':
    return TargetValueCollection(proto, reference_map)

