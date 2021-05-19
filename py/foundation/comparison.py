
from typing import Optional, Iterable, Any, Mapping, Dict
from dataclasses import dataclass
import itertools

from foundation.proto import comparison_pb2

from foundation.extraction import ExtractedValue
from foundation.targets import TargetValue


@dataclass
class ComparedValue:
  _proto: comparison_pb2.ComparedValue
  _reference_map: Dict[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @id.setter
  def id(self, new_obj: 'str') -> None:
    self._proto.id = new_obj
    
  @property
  def target_value(self) -> TargetValue:
    return self._reference_map[self._proto.target_value_id]
  @target_value.setter
  def target_value(self, new_obj: TargetValue) -> None:
    if not isinstance(new_obj, TargetValue):
      raise TypeError("target_value must be a TargetValue, not {}".format(type(new_obj)))
    self._proto.target_value_id = new_obj.id
    self._reference_map[new_obj.id] = new_obj

  @property
  def extracted_value(self) -> ExtractedValue:
    return self._reference_map[self._proto.extracted_value_id]
  @extracted_value.setter
  def extracted_value(self, new_obj: ExtractedValue) -> None:
    if not isinstance(new_obj, ExtractedValue):
      raise TypeError("extracted_value must be a ExtractedValue, not {}".format(type(new_obj)))
    self._proto.extracted_value_id = new_obj.id
    self._reference_map[new_obj.id] = new_obj

  @property
  def score(self) -> 'float':
    return self._proto.score
  @score.setter
  def score(self, new_obj: 'float') -> None:
    self._proto.score = new_obj
    
  @property
  def message(self) -> 'str':
    return self._proto.message
  @message.setter
  def message(self, new_obj: 'str') -> None:
    self._proto.message = new_obj
    

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain([self._proto.target_value_id], [self._proto.extracted_value_id])

  def as_proto(self) -> comparison_pb2.ComparedValue:
    return self._proto

  @staticmethod
  def from_proto(proto: comparison_pb2.ComparedValue, reference_map: Dict[str, Any]) -> 'ComparedValue':
    return ComparedValue(proto, reference_map)



@dataclass
class ComparedValueCollection:
  _proto: comparison_pb2.ComparedValueCollection
  _reference_map: Dict[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @id.setter
  def id(self, new_obj: 'str') -> None:
    self._proto.id = new_obj
    
  @property
  def compared_values(self) -> Iterable['ComparedValue']:
    yield from (self._reference_map[i] for i in self._proto.compared_value_ids)
  @compared_values.setter
  def compared_values(self, new_obj: Iterable['ComparedValue']) -> None:
    # TODO(erick): check to make sure object is a valid foundation type
    del self._proto.compared_value_ids[:]
    for obj in new_obj:
      if not isinstance(obj, 'ComparedValue'):
        raise TypeError("compared_value element must be a 'ComparedValue', not {}".format(type(obj)))
      self._proto.compared_value_ids.append(obj.id)
      self._reference_map[obj.id] = obj


  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain([self._proto.target_value_id], [self._proto.extracted_value_id], self._proto.compared_value_ids)

  def as_proto(self) -> comparison_pb2.ComparedValueCollection:
    return self._proto

  @staticmethod
  def from_proto(proto: comparison_pb2.ComparedValueCollection, reference_map: Dict[str, Any]) -> 'ComparedValueCollection':
    return ComparedValueCollection(proto, reference_map)

