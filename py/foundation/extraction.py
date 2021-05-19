
from typing import Optional, Iterable, Any, Mapping, Dict
from dataclasses import dataclass
import itertools

from foundation.proto import extraction_pb2

from foundation.entity import Entity


@dataclass
class ExtractedValue:
  _proto: extraction_pb2.ExtractedValue
  _reference_map: Dict[str, Any]

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
  def type(self) -> 'str':
    return self._proto.type
  @type.setter
  def type(self, new_obj: 'str') -> None:
    self._proto.type = new_obj
    
  @property
  def serialized_value(self) -> 'bytes':
    return self._proto.serialized_value
  @serialized_value.setter
  def serialized_value(self, new_obj: 'bytes') -> None:
    self._proto.serialized_value = new_obj
    
  @property
  def entitys(self) -> Iterable[Entity]:
    yield from (self._reference_map[i] for i in self._proto.entity_ids)
  @entitys.setter
  def entitys(self, new_obj: Iterable[Entity]) -> None:
    # TODO(erick): check to make sure object is a valid foundation type
    del self._proto.entity_ids[:]
    for obj in new_obj:
      if not isinstance(obj, Entity):
        raise TypeError("entity element must be a Entity, not {}".format(type(obj)))
      self._proto.entity_ids.append(obj.id)
      self._reference_map[obj.id] = obj


  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain(self._proto.entity_ids)

  def as_proto(self) -> extraction_pb2.ExtractedValue:
    return self._proto

  @staticmethod
  def from_proto(proto: extraction_pb2.ExtractedValue, reference_map: Dict[str, Any]) -> 'ExtractedValue':
    return ExtractedValue(proto, reference_map)



@dataclass
class ExtractedValueCollection:
  _proto: extraction_pb2.ExtractedValueCollection
  _reference_map: Dict[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @id.setter
  def id(self, new_obj: 'str') -> None:
    self._proto.id = new_obj
    
  @property
  def extracted_values(self) -> Iterable['ExtractedValue']:
    yield from (self._reference_map[i] for i in self._proto.extracted_value_ids)
  @extracted_values.setter
  def extracted_values(self, new_obj: Iterable['ExtractedValue']) -> None:
    # TODO(erick): check to make sure object is a valid foundation type
    del self._proto.extracted_value_ids[:]
    for obj in new_obj:
      if not isinstance(obj, ExtractedValue):
        raise TypeError("extracted_value element must be a 'ExtractedValue', not {}".format(type(obj)))
      self._proto.extracted_value_ids.append(obj.id)
      self._reference_map[obj.id] = obj


  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain(self._proto.extracted_value_ids)

  def as_proto(self) -> extraction_pb2.ExtractedValueCollection:
    return self._proto

  @staticmethod
  def from_proto(proto: extraction_pb2.ExtractedValueCollection, reference_map: Dict[str, Any]) -> 'ExtractedValueCollection':
    return ExtractedValueCollection(proto, reference_map)

