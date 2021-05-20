
from typing import Optional, Iterable, Any, Mapping, Dict, Type
from dataclasses import dataclass
import itertools
import uuid

from foundation.proto import record_pb2

from foundation.entity import Text
from foundation.extraction import ExtractedValue
from foundation.entity import Page
from foundation.entity import Entity


@dataclass
class RecordContext:
  _proto: record_pb2.RecordContext
  _reference_map: Dict[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @id.setter
  def id(self, new_obj: 'str') -> None:
    self._proto.id = new_obj
    
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

  @property
  def collections(self) -> Iterable[Entity]:
    yield from (self._reference_map[i] for i in self._proto.collection_ids)
  @collections.setter
  def collections(self, new_obj: Iterable[Entity]) -> None:
    # TODO(erick): check to make sure object is a valid foundation type
    del self._proto.collection_ids[:]
    for obj in new_obj:
      if not isinstance(obj, Entity):
        raise TypeError("collection element must be a Entity, not {}".format(type(obj)))
      self._proto.collection_ids.append(obj.id)
      self._reference_map[obj.id] = obj

  @property
  def pages(self) -> Iterable[Page]:
    yield from (self._reference_map[i] for i in self._proto.page_ids)
  @pages.setter
  def pages(self, new_obj: Iterable[Page]) -> None:
    # TODO(erick): check to make sure object is a valid foundation type
    del self._proto.page_ids[:]
    for obj in new_obj:
      if not isinstance(obj, Page):
        raise TypeError("page element must be a Page, not {}".format(type(obj)))
      self._proto.page_ids.append(obj.id)
      self._reference_map[obj.id] = obj

  @property
  def text(self) -> Text:
    return self._reference_map[self._proto.text_id]
  @text.setter
  def text(self, new_obj: Text) -> None:
    if not isinstance(new_obj, Text):
      raise TypeError("text must be a Text, not {}".format(type(new_obj)))
    self._proto.text_id = new_obj.id
    self._reference_map[new_obj.id] = new_obj

  @property
  def extracted_values(self) -> Iterable[ExtractedValue]:
    yield from (self._reference_map[i] for i in self._proto.extracted_value_ids)
  @extracted_values.setter
  def extracted_values(self, new_obj: Iterable[ExtractedValue]) -> None:
    # TODO(erick): check to make sure object is a valid foundation type
    del self._proto.extracted_value_ids[:]
    for obj in new_obj:
      if not isinstance(obj, ExtractedValue):
        raise TypeError("extracted_value element must be a ExtractedValue, not {}".format(type(obj)))
      self._proto.extracted_value_ids.append(obj.id)
      self._reference_map[obj.id] = obj

  # def add(self, cls: Type, **kwargs: Dict) -> Any:
  #   id: str = kwargs.get("id", str(uuid.uuid4))
  #   return cls(id=id, reference_map=self._reference_map, **kwargs)

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain(self._proto.extracted_value_ids, self._proto.entity_ids, self._proto.collection_ids, [self._proto.text_id], self._proto.page_ids)

  @staticmethod
  def build(id: Optional[str] = None, reference_map: Optional[Dict[str, Any]] = None) -> 'RecordContext':
    """
    Build a new RecordContext. Optionally takes a set `id` and `reference_map` as arguments.
    """
    record_id = str(uuid.uuid4()) if id is None else id
    record_reference_map = {} if reference_map is None else reference_map
    return RecordContext(record_pb2.RecordContext(id=record_id), record_reference_map)

  def as_proto(self) -> record_pb2.RecordContext:
    return self._proto

  @staticmethod
  def from_proto(proto: record_pb2.RecordContext, reference_map: Dict[str, Any]) -> 'RecordContext':
    return RecordContext(proto, reference_map)

