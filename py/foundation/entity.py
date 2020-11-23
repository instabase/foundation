""" Entity wrappers. """

import abc
from dataclasses import dataclass
from itertools import chain
from typing import (Dict, Generic, Iterable, List, Optional, Type, TypeVar,
                    Union)

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
                            entity_pb2.Address, entity_pb2.Cluster,
                            entity_pb2.GenericEntity]

E = TypeVar('E', bound='Entity')


class Entity(abc.ABC, Generic[E]):

  @staticmethod
  @abc.abstractmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Entity':
    """Defines the necessary logic for unpacking a protobuf Entity payload.

    See implementing subclass methods for entity-specific definitions.
    Custom Entities will receive msg as a entity_pb2.GenericEntity instance,
    and are responsible for handling its 'bytes' field.

    """
    ...

  @property
  @abc.abstractmethod
  def children(self) -> Iterable[E]:
    """Yields all sub-entities of this entity.

    See implementing subclass methods for entity-specific definitions.
    Can be seen as returning the adjacent entities in a document's Entity
    DAG.

    This method CANNOT call ocr_words().
    """
    ...

  def ocr_words(self) -> Iterable['OcrWordEntity']:
    """Yields all OcrWordEntity's among this entity's children.

    Can be seen as returning an iterator over the leaves of this
    Entity's DAG.

    If this Entity is a WORD, yields itself.

    STRONGLY RECOMMENDED not to override this.
    """
    yield from chain.from_iterable(e.ocr_words() for e in self.children)


@dataclass(frozen=True)
class OcrWordEntity(Entity):
  word: InputWord

  @property
  def origin(self) -> InputWord:
    """Provenance data.

    Returns the OCR InputWord corresponding to this Entity.
    """
    return self.word

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'OcrWordEntity':
    assert isinstance(msg, entity_pb2.OcrWord)
    return OcrWordEntity(InputWord.from_proto(msg.word))

  @property
  def children(self) -> Iterable[E]:
    """ OcrWordEntity has no children. """
    yield from []

  def ocr_words(self) -> Iterable['OcrWordEntity']:
    """ Yields itself.

    This provides the base case for Entity.ocr_words.
    """
    yield self


@dataclass(frozen=True)
class LineEntity(Entity):
  _ocr_words: List[OcrWordEntity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'LineEntity':
    assert isinstance(msg, entity_pb2.Line)
    ocr_words = [OcrWordEntity(InputWord.from_proto(w)) for w in msg.ocr_words]
    return LineEntity(ocr_words)

  @property
  def children(self) -> Iterable[OcrWordEntity]:
    """ A LineEntity's children are its OCR words. """
    yield from self._ocr_words


@dataclass(frozen=True)
class ParagraphEntity(Entity):
  lines: List[LineEntity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'ParagraphEntity':
    assert isinstance(msg, entity_pb2.Paragraph)
    lines = [LineEntity.from_proto(l) for l in msg.lines]
    return ParagraphEntity(lines)

  @property
  def children(self) -> Iterable[LineEntity]:
    """ A ParagraphEntity's children are its Lines. """
    yield from self.lines


@dataclass(frozen=True)
class TableCellEntity(Entity):
  content: List[Entity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableCellEntity':
    assert isinstance(msg, entity_pb2.TableCell)
    content = [proto_to_entity(e) for e in msg.content]
    return TableCellEntity(content)

  @property
  def children(self) -> Iterable[Entity]:
    """ A TableCellEntity's children are its contents. """
    yield from self.content


@dataclass(frozen=True)
class TableRowEntity(Entity):
  cells: List[TableCellEntity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableRowEntity':
    assert isinstance(msg, entity_pb2.TableRow)
    cells = [TableCellEntity.from_proto(c) for c in msg.cells]
    return TableRowEntity(cells)

  @property
  def children(self) -> Iterable[TableCellEntity]:
    """ A TableRowEntity's children are its cells. """
    yield from self.cells


@dataclass(frozen=True)
class TableEntity(Entity):
  rows: List[TableRowEntity]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableEntity':
    assert isinstance(msg, entity_pb2.Table)
    rows = [TableRowEntity.from_proto(r) for r in msg.rows]
    return TableEntity(rows)

  @property
  def children(self) -> Iterable[TableRowEntity]:
    """ A Table's children are its rows. """
    yield from self.rows


@dataclass(frozen=True)
class TokenEntity(Entity):
  span: List[OcrWordEntity]
  score: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TokenEntity':
    assert isinstance(msg, entity_pb2.Token)
    span = [OcrWordEntity(InputWord.from_proto(w)) for w in msg.span]
    score = None
    if msg.HasField('score'):
      score = msg.score
    return TokenEntity(span, score)

  @property
  def children(self) -> Iterable[OcrWordEntity]:
    """ A TokenEntity's children are its span of OcrWordEntities. """
    yield from self.span


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

  @property
  def children(self) -> Iterable[TokenEntity]:
    """ A PhraseEntity's children are its tokens. """
    yield from self.words


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

  @property
  def children(self) -> Iterable[Entity]:
    """ A NumberEntity's child is its token. """
    yield self.token


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

  @property
  def children(self) -> Iterable[Entity]:
    """ An IntegerEntity's child is its token. """
    yield self.token


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

  @property
  def children(self) -> Iterable[Entity]:
    """ A DateEntity's child is its token. """
    yield self.token


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

  @property
  def children(self) -> Iterable[Entity]:
    """ A TimeEntity's child is its token. """
    yield self.token


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

  @property
  def children(self) -> Iterable[Entity]:
    """ A CurrencyEntity's child is its token. """
    yield self.token


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

  @property
  def children(self) -> Iterable[PhraseEntity]:
    """ A NameEntity's child is the PhraseEntity of its name parts. """
    yield self.name_parts


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

  @property
  def children(self) -> Iterable[PhraseEntity]:
    """ A AddressEntity's children are the PhraseEntities of its line parts. """
    yield from self.lines


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

  @property
  def children(self) -> Iterable[PhraseEntity]:
    """ A ClusterEntity's child is the PhraseEntity spanning its tokens. """
    yield self.token_span


""" Associates a string entity type name to a custom class that inherits
    from Entity.
"""
CustomEntityRegistry = Dict[str, Type[Entity]]


def proto_to_entity(
    msg: entity_pb2.Entity,
    entity_registry: Optional[CustomEntityRegistry] = None) -> Entity:
  """Handles dispatching entity_pb2.Entity unpacking to subclasses of Entity.

  In the proto definition, Entity is a message containing a payload which
  is any of the possible Entity types.

  See https://github.com/instabase/foundation/pull/6#discussion_r528896807.

  Args:
    msg: The deserialized entity_pb2.Entity data
    entity_registry: Provides a lookup from custom Entity type name to the
                 appropriate class which implements from_proto for the custom
                 entity data.
  Returns:
    An instance of subclass of Entity which wraps the protobuf data.
  Raises:
    ValueError: If msg is a GenericEntity and no custom Entity decoder is
                found in decoder_ctx for the 'msg.custom.type' field.
    AssertionError: If not all payload types (defined in the .proto spec) are
                    cased in this function.
  """
  payload_type = msg.WhichOneof('payload')
  if payload_type == 'ocr_word':
    return OcrWordEntity.from_proto(msg.ocr_word)
  elif payload_type == 'line':
    return LineEntity.from_proto(msg.line)
  elif payload_type == 'paragraph':
    return ParagraphEntity.from_proto(msg.paragraph)
  elif payload_type == 'table_cell':
    return TableCellEntity.from_proto(msg.table_cell)
  elif payload_type == 'table_row':
    return TableRowEntity.from_proto(msg.table_row)
  elif payload_type == 'table':
    return TableEntity.from_proto(msg.table)
  elif payload_type == 'token':
    return TokenEntity.from_proto(msg.token)
  elif payload_type == 'phrase':
    return TokenEntity.from_proto(msg.phrase)
  elif payload_type == 'number':
    return NumberEntity.from_proto(msg.number)
  elif payload_type == 'integer':
    return IntegerEntity.from_proto(msg.integer)
  elif payload_type == 'date':
    return DateEntity.from_proto(msg.date)
  elif payload_type == 'time':
    return TimeEntity.from_proto(msg.time)
  elif payload_type == 'currency':
    return CurrencyEntity.from_proto(msg.currency)
  elif payload_type == 'name':
    return NameEntity.from_proto(msg.name)
  elif payload_type == 'address':
    return AddressEntity.from_proto(msg.address)
  elif payload_type == 'cluster':
    return ClusterEntity.from_proto(msg.cluster)
  elif payload_type == 'custom':
    custom_type: str = getattr(msg.custom, 'type')
    if entity_registry is not None:
      if custom_type in entity_registry:
        CustomClass = entity_registry[custom_type]
        return CustomClass.from_proto(msg.custom)
    raise ValueError(
        f'No implementation found for GenericEntity type "{custom_type}".')

  # This is a protocol decoding error, probably missing an if statement
  # in this function.
  raise AssertionError(f'Unhandled message type: {payload_type}')
