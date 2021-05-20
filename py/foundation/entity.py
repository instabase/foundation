
from typing import Optional, Iterable, Any, Mapping, Dict
from dataclasses import dataclass
import itertools

from foundation.proto import entity_pb2

from foundation.geometry import BBox



@dataclass
class Entity:
  _proto: entity_pb2.Entity
  _reference_map: Dict[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @id.setter
  def id(self, new_obj: 'str') -> None:
    self._proto.id = new_obj

  @property
  def children(self) -> Iterable['Entity']:
    yield from (self._reference_map[i] for i in self._proto.children_ids)
  @children.setter
  def children(self, new_obj: Iterable['Entity']) -> None:
    # TODO(erick): check to make sure object is a valid foundation type
    del self._proto.children_ids[:]
    for obj in new_obj:
      if not isinstance(obj, Entity):
        raise TypeError("children element must be a 'Entity', not {}".format(type(obj)))
      self._proto.children_ids.append(obj.id)
      self._reference_map[obj.id] = obj

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain(self._proto.children_ids)

  def as_proto(self) -> entity_pb2.Entity:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'Entity':
    return Entity(proto, reference_map)

@dataclass
class Word(Entity):
  @property
  def bbox(self) -> BBox:
    return BBox(self._proto.word.bbox)
  @bbox.setter
  def bbox(self, new_obj: BBox) -> None:
    self._proto.word.bbox.page_index = new_obj._proto.page_index
    self._proto.word.bbox.rectangle.ix.a = new_obj._proto.rectangle.ix.a
    self._proto.word.bbox.rectangle.ix.b = new_obj._proto.rectangle.ix.b
    self._proto.word.bbox.rectangle.iy.a = new_obj._proto.rectangle.iy.a
    self._proto.word.bbox.rectangle.iy.b = new_obj._proto.rectangle.iy.b
  @property
  def text(self) -> 'str':
    return self._proto.word.text
  @text.setter
  def text(self, new_obj: 'str') -> None:
    self._proto.word.text = new_obj

  @staticmethod
  def build(id: str, bbox: BBox, text: str, reference_map: Dict[str, Any]) -> 'Word':
    proto = entity_pb2.Entity(
      id=id,
      children_ids=[],
      word=entity_pb2.Word(
        bbox=bbox.as_proto(),
        text=text
      )
    )
    return Word(proto, reference_map)

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'Word':
    return Word(proto, reference_map)


@dataclass
class Text(Entity):
  @property
  def children(self) -> Iterable['Word']:
    yield from (self._reference_map[i] for i in self._proto.children_ids)
  @children.setter
  def children(self, new_obj: Iterable[Entity]) -> None:
    del self._proto.children_ids[:]
    for obj in new_obj:
      if not isinstance(obj, Word):
        raise TypeError("word element must be a 'Word', not {}".format(type(obj)))
      self._proto.children_ids.append(obj.id)
      self._reference_map[obj.id] = obj

  @property
  def likeness_score(self) -> float:
    return self._proto.text.likeness_score
  @likeness_score.setter
  def likeness_score(self, new_obj: float) -> None:
    self._proto.text.likeness_score = new_obj

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain(self._proto.children_ids)

  def as_proto(self) -> entity_pb2.Entity:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'Text':
    return Text(proto, reference_map)


@dataclass
class Address(Text):

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'Address':
    return Address(proto, reference_map)



@dataclass
class CurrencyAmount(Text):

  @property
  def currency(self) -> entity_pb2.CurrencyAmount.Currency:
    return self._proto.text.currency_amount.currency
  @currency.setter
  def currency(self, new_obj: entity_pb2.CurrencyAmount.Currency) -> None:
    self._proto.text.currency_amount.currency = new_obj
    
  @property
  def amount(self) -> int:
    return self._proto.text.currency_amount.amount
  @amount.setter
  def amount(self, new_obj: int) -> None:
    self._proto.text.currency_amount.amount = new_obj

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'CurrencyAmount':
    return CurrencyAmount(proto, reference_map)



@dataclass
class Date(Text):

  @property
  def year(self) -> int:
    return self._proto.text.date.year
  @year.setter
  def year(self, new_obj: int) -> None:
    self._proto.text.date.year = new_obj
    
  @property
  def month(self) -> int:
    return self._proto.text.date.month
  @month.setter
  def month(self, new_obj: int) -> None:
    self._proto.text.date.month = new_obj
    
  @property
  def day(self) -> int:
    return self._proto.text.date.day
  @day.setter
  def day(self, new_obj: int) -> None:
    self._proto.text.date.day = new_obj

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'Date':
    return Date(proto, reference_map)



@dataclass
class EntityCollection:
  _proto: entity_pb2.EntityCollection
  _reference_map: Dict[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @id.setter
  def id(self, new_obj: 'str') -> None:
    self._proto.id = new_obj
    
  @property
  def entities(self) -> Iterable['Entity']:
    yield from (self._reference_map[i] for i in self._proto.entity_ids)
  @entities.setter
  def entities(self, new_obj: Iterable[Entity]) -> None:
    del self._proto.entity_ids[:]
    for obj in new_obj:
      if not isinstance(obj, Entity):
        raise TypeError("entity element must be a 'Entity', not {}".format(type(obj)))
      self._proto.entity_ids.append(obj.id)
      self._reference_map[obj.id] = obj


  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain(self._proto.entity_ids)

  def as_proto(self) -> entity_pb2.EntityCollection:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.EntityCollection, reference_map: Dict[str, Any]) -> 'EntityCollection':
    return EntityCollection(proto, reference_map)



@dataclass
class FillerString(Entity):

  @property
  def text(self) -> 'str':
    return self._proto.filler_string.text
  @text.setter
  def text(self, new_obj: 'str') -> None:
    self._proto.filler_string.text = new_obj

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'FillerString':
    return FillerString(proto, reference_map)



@dataclass
class Page(Entity):

  @property
  def bbox(self) -> BBox:
    return BBox(self._proto.page.bbox)
  @bbox.setter
  def bbox(self, new_obj: BBox) -> None:
    self._proto.page.bbox.page_index = new_obj._proto.page_index
    self._proto.page.bbox.rectangle.ix.a = new_obj._proto.rectangle.ix.a
    self._proto.page.bbox.rectangle.ix.b = new_obj._proto.rectangle.ix.b
    self._proto.page.bbox.rectangle.iy.a = new_obj._proto.rectangle.iy.a
    self._proto.page.bbox.rectangle.iy.b = new_obj._proto.rectangle.iy.b
  @property
  def image_path(self) -> 'str':
    return self._proto.page.image_path
  @image_path.setter
  def image_path(self, new_obj: 'str') -> None:
    self._proto.page.image_path = new_obj

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'Page':
    return Page(proto, reference_map)



@dataclass
class PersonName(Entity):

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'PersonName':
    return PersonName(proto, reference_map)



@dataclass
class SubWord(Entity):

  @property
  def word(self) -> 'Word':
    return self._reference_map[self._proto.sub_word.word_id]
  @word.setter
  def word(self, new_obj: 'Word') -> None:
    if not isinstance(new_obj, Word):
      raise TypeError("word must be a 'Word', not {}".format(type(new_obj)))
    self._proto.sub_word.word_id = new_obj.id
    self._reference_map[new_obj.id] = new_obj

  @property
  def start_index(self) -> int:
    return self._proto.sub_word.start_index
  @start_index.setter
  def start_index(self, new_obj: int) -> None:
    self._proto.sub_word.start_index = new_obj
    
  @property
  def end_index(self) -> int:
    return self._proto.sub_word.end_index
  @end_index.setter
  def end_index(self, new_obj: int) -> None:
    self._proto.sub_word.end_index = new_obj
    

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from itertools.chain([self._proto.sub_word.word_id], self._proto.children_ids)

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Dict[str, Any]) -> 'SubWord':
    return SubWord(proto, reference_map)



