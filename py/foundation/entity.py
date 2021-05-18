
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from foundation.proto import entity_pb2

from foundation.geometry import BBox


@dataclass
class Address:
  _proto: entity_pb2.Address
  _reference_map: Mapping[str, Any]



  def as_proto(self) -> entity_pb2.Address:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.Address, reference_map: Mapping[str, Any]) -> 'Address':
    return Address(proto, reference_map)



@dataclass
class CurrencyAmount:
  _proto: entity_pb2.CurrencyAmount
  _reference_map: Mapping[str, Any]

  @property
  def currency(self) -> 'int':
    return self._proto.currency
  @property
  def amount(self) -> 'int':
    return self._proto.amount

  def as_proto(self) -> entity_pb2.CurrencyAmount:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.CurrencyAmount, reference_map: Mapping[str, Any]) -> 'CurrencyAmount':
    return CurrencyAmount(proto, reference_map)



@dataclass
class Date:
  _proto: entity_pb2.Date
  _reference_map: Mapping[str, Any]

  @property
  def year(self) -> 'int':
    return self._proto.year
  @property
  def month(self) -> 'int':
    return self._proto.month
  @property
  def day(self) -> 'int':
    return self._proto.day

  def as_proto(self) -> entity_pb2.Date:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.Date, reference_map: Mapping[str, Any]) -> 'Date':
    return Date(proto, reference_map)



@dataclass
class Entity:
  _proto: entity_pb2.Entity
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @property
  def children(self) -> 'Entity':
    return self._reference_map[self._proto.children_id]

  @property
  def word(self) -> 'Word':
    return Word(self._proto.word, self._reference_map)
  @property
  def filler_string(self) -> 'FillerString':
    return FillerString(self._proto.filler_string, self._reference_map)
  @property
  def sub_word(self) -> 'SubWord':
    return SubWord(self._proto.sub_word, self._reference_map)
  @property
  def page(self) -> 'Page':
    return Page(self._proto.page, self._reference_map)
  @property
  def text(self) -> 'Text':
    return Text(self._proto.text, self._reference_map)

  def as_proto(self) -> entity_pb2.Entity:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.Entity, reference_map: Mapping[str, Any]) -> 'Entity':
    return Entity(proto, reference_map)



@dataclass
class EntityCollection:
  _proto: entity_pb2.EntityCollection
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> 'str':
    return self._proto.id
  @property
  def entitys(self) -> Iterable['Entity']:
    yield from (self._reference_map[i] for i in self._proto.entity_ids)


  def as_proto(self) -> entity_pb2.EntityCollection:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.EntityCollection, reference_map: Mapping[str, Any]) -> 'EntityCollection':
    return EntityCollection(proto, reference_map)



@dataclass
class FillerString:
  _proto: entity_pb2.FillerString
  _reference_map: Mapping[str, Any]

  @property
  def text(self) -> 'str':
    return self._proto.text

  def as_proto(self) -> entity_pb2.FillerString:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.FillerString, reference_map: Mapping[str, Any]) -> 'FillerString':
    return FillerString(proto, reference_map)



@dataclass
class Page:
  _proto: entity_pb2.Page
  _reference_map: Mapping[str, Any]

  @property
  def bbox(self) -> BBox:
    return BBox(self._proto.bbox, self._reference_map)
  @property
  def image_path(self) -> 'str':
    return self._proto.image_path

  def as_proto(self) -> entity_pb2.Page:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.Page, reference_map: Mapping[str, Any]) -> 'Page':
    return Page(proto, reference_map)



@dataclass
class PersonName:
  _proto: entity_pb2.PersonName
  _reference_map: Mapping[str, Any]



  def as_proto(self) -> entity_pb2.PersonName:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.PersonName, reference_map: Mapping[str, Any]) -> 'PersonName':
    return PersonName(proto, reference_map)



@dataclass
class SubWord:
  _proto: entity_pb2.SubWord
  _reference_map: Mapping[str, Any]

  @property
  def word(self) -> 'Word':
    return self._reference_map[self._proto.word_id]

  @property
  def start_index(self) -> 'int':
    return self._proto.start_index
  @property
  def end_index(self) -> 'int':
    return self._proto.end_index

  def as_proto(self) -> entity_pb2.SubWord:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.SubWord, reference_map: Mapping[str, Any]) -> 'SubWord':
    return SubWord(proto, reference_map)



@dataclass
class Text:
  _proto: entity_pb2.Text
  _reference_map: Mapping[str, Any]

  @property
  def words(self) -> Iterable['Word']:
    yield from (self._reference_map[i] for i in self._proto.word_ids)

  @property
  def likeness_score(self) -> 'float':
    return self._proto.likeness_score
  @property
  def date(self) -> 'Date':
    return Date(self._proto.date, self._reference_map)
  @property
  def currency_amount(self) -> 'CurrencyAmount':
    return CurrencyAmount(self._proto.currency_amount, self._reference_map)
  @property
  def person_name(self) -> 'PersonName':
    return PersonName(self._proto.person_name, self._reference_map)
  @property
  def address(self) -> 'Address':
    return Address(self._proto.address, self._reference_map)

  def as_proto(self) -> entity_pb2.Text:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.Text, reference_map: Mapping[str, Any]) -> 'Text':
    return Text(proto, reference_map)



@dataclass
class Word:
  _proto: entity_pb2.Word
  _reference_map: Mapping[str, Any]

  @property
  def bbox(self) -> BBox:
    return BBox(self._proto.bbox, self._reference_map)
  @property
  def text(self) -> 'str':
    return self._proto.text

  def as_proto(self) -> entity_pb2.Word:
    return self._proto

  @staticmethod
  def from_proto(proto: entity_pb2.Word, reference_map: Mapping[str, Any]) -> 'Word':
    return Word(proto, reference_map)

