""" Entity wrappers. """

import abc
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar, Union

from foundation.protos import geometry_pb2
from foundation.protos.doc import entity_pb2
from foundation.protos.doc.entity_pb2 import Currency as Currency_pb2

from .ocr import InputWord
""" These are the built-in Entity types supported by Foundation. """
PbEntityPayloadType = Union[entity_pb2.OcrWord, entity_pb2.Line,
                            entity_pb2.Paragraph, entity_pb2.TableCell,
                            entity_pb2.TableRow, entity_pb2.Table,
                            entity_pb2.Token, entity_pb2.Phrase,
                            entity_pb2.Number, entity_pb2.Integer,
                            entity_pb2.Date, entity_pb2.Time,
                            entity_pb2.Currency, entity_pb2.Name,
                            entity_pb2.Address, entity_pb2.Cluster]


class Entity(abc.ABC):

  @staticmethod
  @abc.abstractmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Entity':
    pass


@dataclass(frozen=True)
class OcrWordEntity(Entity):
  word: InputWord

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'OcrWordEntity':
    assert isinstance(msg, entity_pb2.OcrWord)
    return OcrWordEntity(InputWord.from_proto(msg.word))


@dataclass(frozen=True)
class LineEntity(Entity):
  ocr_words: List[InputWord]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'LineEntity':
    assert isinstance(msg, entity_pb2.Line)
    ocr_words = [InputWord.from_proto(w) for w in msg.ocr_words]
    return LineEntity(ocr_words)


@dataclass(frozen=True)
class ParagraphEntity(Entity):
  lines: List[LineEntity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'ParagraphEntity':
    assert isinstance(msg, entity_pb2.Paragraph)
    lines = [LineEntity.from_proto(l) for l in msg.lines]
    return ParagraphEntity(lines)


@dataclass(frozen=True)
class TableCellEntity(Entity):
  content: List[Entity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableCellEntity':
    assert isinstance(msg, entity_pb2.TableCell)
    content = [proto_to_entity(e) for e in msg.content]
    return TableCellEntity(content)


@dataclass(frozen=True)
class TableRowEntity(Entity):
  cells: List[TableCellEntity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableRowEntity':
    assert isinstance(msg, entity_pb2.TableRow)
    cells = [TableCellEntity.from_proto(c) for c in msg.cells]
    return TableRowEntity(cells)


@dataclass(frozen=True)
class TableEntity(Entity):
  rows: List[TableRowEntity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableEntity':
    assert isinstance(msg, entity_pb2.Table)
    rows = [TableRowEntity.from_proto(r) for r in msg.rows]
    return TableEntity(rows)


@dataclass(frozen=True)
class TokenEntity(Entity):
  span: List[InputWord]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TokenEntity':
    assert isinstance(msg, entity_pb2.Token)
    span = [InputWord.from_proto(w) for w in msg.span]
    score = None
    if msg.HasField('score'):
      score = msg.score
    return TokenEntity(span, score)


@dataclass(frozen=True)
class PhraseEntity(Entity):
  words: List[TokenEntity]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'PhraseEntity':
    assert isinstance(msg, entity_pb2.Phrase)
    words = [TokenEntity.from_proto(t) for t in msg.words]
    score = None
    if msg.HasField('score'):
      score = msg.score
    return PhraseEntity(words, score)


@dataclass(frozen=True)
class NumberEntity(Entity):
  token: TokenEntity
  value: Optional[float]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'NumberEntity':
    assert isinstance(msg, entity_pb2.Number)
    token = TokenEntity.from_proto(msg.token)
    value = None
    if msg.HasField('value'):
      value = msg.value
    score = None
    if msg.HasField('score'):
      score = msg.score
    return NumberEntity(token, value, score)


@dataclass(frozen=True)
class IntegerEntity(Entity):
  token: TokenEntity
  value: Optional[int]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'IntegerEntity':
    assert isinstance(msg, entity_pb2.Integer)
    token = TokenEntity.from_proto(msg.token)
    value = None
    if msg.HasField('value'):
      value = msg.value
    score = None
    if msg.HasField('score'):
      score = msg.score
    return IntegerEntity(token, value, score)


@dataclass(frozen=True)
class DateEntity(Entity):
  token: TokenEntity
  value: Optional[str]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'DateEntity':
    assert isinstance(msg, entity_pb2.Date)
    token = TokenEntity.from_proto(msg.token)
    value = None
    if msg.HasField('value'):
      value = msg.value
    score = None
    if msg.HasField('score'):
      score = msg.score
    return DateEntity(token, value, score)


@dataclass(frozen=True)
class TimeEntity(Entity):
  token: TokenEntity
  value: Optional[int]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TimeEntity':
    assert isinstance(msg, entity_pb2.Time)
    token = TokenEntity.from_proto(msg.token)
    value = None
    if msg.HasField('value'):
      value = msg.value
    score = None
    if msg.HasField('score'):
      score = msg.score
    return TimeEntity(token, value, score)


@dataclass(frozen=True)
class CurrencyEntity(Entity):
  token: TokenEntity
  # TODO: wrap FixedDecimal
  value: Optional[Currency_pb2.FixedDecimal]
  score: Optional[float]
  units: Optional[str]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'CurrencyEntity':
    assert isinstance(msg, entity_pb2.Currency)
    token = TokenEntity.from_proto(msg.token)
    units = None
    if msg.HasField('units'):
      units = msg.units
    value = None
    if msg.HasField('value'):
      value = msg.value
    score = None
    if msg.HasField('score'):
      score = msg.score
    return CurrencyEntity(token, value, score, units)


@dataclass(frozen=True)
class NameEntity(Entity):
  name_parts: PhraseEntity
  value: Optional[str]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'NameEntity':
    assert isinstance(msg, entity_pb2.Name)
    name_parts = PhraseEntity.from_proto(msg.name_parts)
    value = None
    if msg.HasField('value'):
      value = msg.value
    score = None
    if msg.HasField('score'):
      score = msg.score
    return NameEntity(name_parts, value, score)


@dataclass(frozen=True)
class AddressEntity(Entity):
  lines: List[PhraseEntity]
  value: Optional[str]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'AddressEntity':
    assert isinstance(msg, entity_pb2.Address)
    lines = [PhraseEntity.from_proto(l) for l in msg.lines]
    value = None
    if msg.HasField('value'):
      value = msg.value
    score = None
    if msg.HasField('score'):
      score = msg.score
    return AddressEntity(lines, value, score)


@dataclass(frozen=True)
class ClusterEntity(Entity):
  token_span: PhraseEntity
  label: Optional[str]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'ClusterEntity':
    assert isinstance(msg, entity_pb2.Cluster)
    token_span = PhraseEntity.from_proto(msg.token_span)
    label = None
    if msg.HasField('label'):
      label = msg.label
    score = None
    if msg.HasField('score'):
      score = msg.score
    return ClusterEntity(token_span, label, score)


def proto_to_entity(msg: entity_pb2.Entity) -> Entity:
  if msg.HasField('ocr_word'):
    return OcrWordEntity.from_proto(msg.ocr_word)
  if msg.HasField('line'):
    return LineEntity.from_proto(msg.line)
  if msg.HasField('paragraph'):
    return ParagraphEntity.from_proto(msg.paragraph)
  if msg.HasField('table_cell'):
    return TableCellEntity.from_proto(msg.table_cell)
  if msg.HasField('table_row'):
    return TableRowEntity.from_proto(msg.table_row)
  if msg.HasField('table'):
    return TableEntity.from_proto(msg.table)
  if msg.HasField('token'):
    return TokenEntity.from_proto(msg.token)
  if msg.HasField('phrase'):
    return TokenEntity.from_proto(msg.phrase)
  if msg.HasField('number'):
    return NumberEntity.from_proto(msg.number)
  if msg.HasField('integer'):
    return IntegerEntity.from_proto(msg.integer)
  if msg.HasField('date'):
    return DateEntity.from_proto(msg.date)
  if msg.HasField('time'):
    return TimeEntity.from_proto(msg.time)
  if msg.HasField('currency'):
    return CurrencyEntity.from_proto(msg.currency)
  if msg.HasField('name'):
    return NameEntity.from_proto(msg.name)
  if msg.HasField('address'):
    return AddressEntity.from_proto(msg.address)
  if msg.HasField('cluster'):
    return ClusterEntity.from_proto(msg.cluster)

  # TODO: handle custom entity types, maybe this function should take a custom
  # decoder handle or something?
  raise AssertionError('Unhandled message type: {}'.format(
      msg.WhichOneof('payload')))
