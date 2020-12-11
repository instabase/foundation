""" Entity wrappers. """

import abc
from dataclasses import dataclass
from itertools import chain
from typing import (Dict, Generic, Iterable, List, Optional, Type, TypeVar,
                    Union)

from foundation.protos import geometry_pb2
from foundation.protos.doc import entity_pb2
from foundation.protos.doc.entity_pb2 import Currency as Currency_pb2

from .geometry import BBox
from .ocr import InputWord
from .typing_utils import assert_exhaustive, unwrap
""" These are the built-in Entity types supported by Foundation. """
PbEntityPayloadType = Union[entity_pb2.Word, entity_pb2.Line,
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

  @abc.abstractmethod
  def to_proto(self) -> PbEntityPayloadType:
    """Defines the necessary serialization logic for the Entity.

    Custom Entities should return an entity_pb2.GenericEntity instance,
    and are responsible for setting the 'type' field appropriately.
    """
    ...

  @property
  @abc.abstractmethod
  def bbox(self) -> BBox:
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

  def ocr_words(self) -> Iterable['WordEntity']:
    """Yields all OcrWordEntity's among this entity's children.

    Can be seen as returning an iterator over the leaves of this
    Entity's DAG.

    If this Entity is a WORD, yields itself.

    STRONGLY RECOMMENDED not to override this.
    """
    yield from chain.from_iterable(e.ocr_words() for e in self.children)


@dataclass(frozen=True)
class WordEntity(Entity):
  text: str
  bbox: BBox
  origin: Optional[InputWord] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'WordEntity':
    assert isinstance(msg, entity_pb2.Word)
    text = msg.text
    bbox = unwrap(BBox.from_proto(msg.bbox))  # TODO: what does None mean here?
    input_word = None
    if msg.HasField('origin'):
      input_word = InputWord.from_proto(msg.origin)
    return WordEntity(text, bbox, input_word)

  def to_proto(self) -> entity_pb2.Word:
    msg = entity_pb2.Word(text=self.text,
                          bbox=self.bbox.to_proto())
    if self.origin is not None:
      msg.origin.CopyFrom(self.origin.to_proto())
    return msg

  @property
  def children(self) -> Iterable[E]:
    """ WordEntity has no children. """
    yield from []

  def ocr_words(self) -> Iterable['WordEntity']:
    """ Yields itself.

    This provides the base case for Entity.ocr_words.
    """
    yield self


@dataclass(frozen=True)
class LineEntity(Entity):
  _ocr_words: List[WordEntity]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'LineEntity':
    assert isinstance(msg, entity_pb2.Line)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    ocr_words = [WordEntity.from_proto(w) for w in msg.words]
    return LineEntity(ocr_words, bbox)

  def to_proto(self) -> entity_pb2.Line:
    msg = entity_pb2.Line(bbox=self.bbox.to_proto())
    msg.words.extend(w.to_proto() for w in self._ocr_words)
    return msg

  @property
  def children(self) -> Iterable[WordEntity]:
    """ A LineEntity's children are its OCR words. """
    yield from self._ocr_words


@dataclass(frozen=True)
class ParagraphEntity(Entity):
  lines: List[LineEntity]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'ParagraphEntity':
    assert isinstance(msg, entity_pb2.Paragraph)
    lines = [LineEntity.from_proto(l) for l in msg.lines]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return ParagraphEntity(lines, bbox)

  def to_proto(self) -> entity_pb2.Paragraph:
    msg = entity_pb2.Paragraph(bbox=self.bbox.to_proto())
    msg.lines.extend(l.to_proto() for l in self.lines)
    return msg

  @property
  def children(self) -> Iterable[LineEntity]:
    """ A ParagraphEntity's children are its Lines. """
    yield from self.lines


@dataclass(frozen=True)
class TableCellEntity(Entity):
  content: List[Entity]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableCellEntity':
    assert isinstance(msg, entity_pb2.TableCell)
    content = [proto_to_entity(e) for e in msg.content]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return TableCellEntity(content, bbox)

  def to_proto(self) -> entity_pb2.TableCell:
    msg = entity_pb2.TableCell(bbox=self.bbox.to_proto())
    msg.content.extend(entity_to_proto(e) for e in self.content)
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A TableCellEntity's children are its contents. """
    yield from self.content


@dataclass(frozen=True)
class TableRowEntity(Entity):
  cells: List[TableCellEntity]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableRowEntity':
    assert isinstance(msg, entity_pb2.TableRow)
    cells = [TableCellEntity.from_proto(c) for c in msg.cells]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return TableRowEntity(cells, bbox)

  def to_proto(self) -> entity_pb2.TableRow:
    msg = entity_pb2.TableRow(bbox=self.bbox.to_proto())
    msg.cells.extend(c.to_proto() for c in self.cells)
    return msg

  @property
  def children(self) -> Iterable[TableCellEntity]:
    """ A TableRowEntity's children are its cells. """
    yield from self.cells


@dataclass(frozen=True)
class TableEntity(Entity):
  rows: List[TableRowEntity]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableEntity':
    assert isinstance(msg, entity_pb2.Table)
    rows = [TableRowEntity.from_proto(r) for r in msg.rows]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return TableEntity(rows, bbox)

  def to_proto(self) -> entity_pb2.Table:
    msg = entity_pb2.Table(bbox=self.bbox.to_proto())
    msg.rows.extend(r.to_proto() for r in self.rows)
    return msg

  @property
  def children(self) -> Iterable[TableRowEntity]:
    """ A Table's children are its rows. """
    yield from self.rows


@dataclass(frozen=True)
class TokenEntity(Entity):
  span: List[WordEntity]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TokenEntity':
    assert isinstance(msg, entity_pb2.Token)
    span = [WordEntity.from_proto(w) for w in msg.span]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return TokenEntity(span, bbox)

  def to_proto(self) -> entity_pb2.Token:
    msg = entity_pb2.Token(bbox=self.bbox.to_proto())
    msg.span.extend(s.to_proto() for s in self.span)
    return msg

  @property
  def children(self) -> Iterable[WordEntity]:
    """ A TokenEntity's children are its span of OcrWordEntities. """
    yield from self.span


@dataclass(frozen=True)
class PhraseEntity(Entity):
  words: List[TokenEntity]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'PhraseEntity':
    assert isinstance(msg, entity_pb2.Phrase)
    words = [TokenEntity.from_proto(t) for t in msg.words]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return PhraseEntity(words, bbox)

  def to_proto(self) -> entity_pb2.Phrase:
    msg = entity_pb2.Phrase(bbox=self.bbox.to_proto())
    msg.words.extend(w.to_proto() for w in self.words)
    return msg

  @property
  def children(self) -> Iterable[TokenEntity]:
    """ A PhraseEntity's children are its tokens. """
    yield from self.words


@dataclass(frozen=True)
class NumberEntity(Entity):
  token: TokenEntity
  bbox: BBox
  value: Optional[float]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'NumberEntity':
    assert isinstance(msg, entity_pb2.Number)
    token = TokenEntity.from_proto(msg.token)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return NumberEntity(token, bbox, value)

  def to_proto(self) -> entity_pb2.Number:
    msg = entity_pb2.Number(bbox=self.bbox.to_proto())
    msg.token.CopyFrom(self.token.to_proto())
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A NumberEntity's child is its token. """
    yield self.token


@dataclass(frozen=True)
class IntegerEntity(Entity):
  token: TokenEntity
  bbox: BBox
  value: Optional[int]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'IntegerEntity':
    assert isinstance(msg, entity_pb2.Integer)
    token = TokenEntity.from_proto(msg.token)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return IntegerEntity(token, bbox, value)

  def to_proto(self) -> entity_pb2.Integer:
    msg = entity_pb2.Integer(bbox=self.bbox.to_proto())
    msg.token.CopyFrom(self.token.to_proto())
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ An IntegerEntity's child is its token. """
    yield self.token


@dataclass(frozen=True)
class DateEntity(Entity):
  token: TokenEntity
  bbox: BBox
  value: Optional[str]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'DateEntity':
    assert isinstance(msg, entity_pb2.Date)
    token = TokenEntity.from_proto(msg.token)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return DateEntity(token, bbox, value)

  def to_proto(self) -> entity_pb2.Date:
    msg = entity_pb2.Date(bbox=self.bbox.to_proto())
    msg.token.CopyFrom(self.token.to_proto())
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A DateEntity's child is its token. """
    yield self.token


@dataclass(frozen=True)
class TimeEntity(Entity):
  token: TokenEntity
  bbox: BBox
  value: Optional[int]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TimeEntity':
    assert isinstance(msg, entity_pb2.Time)
    token = TokenEntity.from_proto(msg.token)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return TimeEntity(token, bbox, value)

  def to_proto(self) -> entity_pb2.Time:
    msg = entity_pb2.Time(bbox=self.bbox.to_proto())
    msg.token.CopyFrom(self.token.to_proto())
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A TimeEntity's child is its token. """
    yield self.token


@dataclass(frozen=True)
class CurrencyEntity(Entity):
  token: TokenEntity
  bbox: BBox
  # TODO: wrap FixedDecimal
  value: Optional[Currency_pb2.FixedDecimal]
  units: Optional[str]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'CurrencyEntity':
    assert isinstance(msg, entity_pb2.Currency)
    token = TokenEntity.from_proto(msg.token)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    units = None
    if msg.HasField('units'):
      units = msg.units
    value = None
    if msg.HasField('value'):
      value = msg.value
    return CurrencyEntity(token, bbox, value, units)

  def to_proto(self) -> entity_pb2.Currency:
    msg = entity_pb2.Currency(bbox=self.bbox.to_proto())
    msg.token.CopyFrom(self.token.to_proto())
    if self.value is not None:
      msg.value.CopyFrom(self.value)
    if self.units is not None:
      msg.units = self.units
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A CurrencyEntity's child is its token. """
    yield self.token


@dataclass(frozen=True)
class NameEntity(Entity):
  name_parts: PhraseEntity
  bbox: BBox
  value: Optional[str]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'NameEntity':
    assert isinstance(msg, entity_pb2.Name)
    name_parts = PhraseEntity.from_proto(msg.name_parts)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return NameEntity(name_parts, bbox, value)

  def to_proto(self) -> entity_pb2.Name:
    msg = entity_pb2.Name(bbox=self.bbox.to_proto())
    msg.name_parts.CopyFrom(self.name_parts.to_proto())
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[PhraseEntity]:
    """ A NameEntity's child is the PhraseEntity of its name parts. """
    yield self.name_parts


@dataclass(frozen=True)
class AddressEntity(Entity):
  lines: List[PhraseEntity]
  bbox: BBox
  value: Optional[str]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'AddressEntity':
    assert isinstance(msg, entity_pb2.Address)
    lines = [PhraseEntity.from_proto(l) for l in msg.lines]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return AddressEntity(lines, bbox, value)

  def to_proto(self) -> entity_pb2.Address:
    msg = entity_pb2.Address(bbox=self.bbox.to_proto())
    msg.lines.extend(l.to_proto() for l in self.lines)
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[PhraseEntity]:
    """ A AddressEntity's children are the PhraseEntities of its line parts. """
    yield from self.lines


@dataclass(frozen=True)
class ClusterEntity(Entity):
  token_span: PhraseEntity
  bbox: BBox
  label: Optional[str]

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'ClusterEntity':
    assert isinstance(msg, entity_pb2.Cluster)
    token_span = PhraseEntity.from_proto(msg.token_span)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    label = None
    if msg.HasField('label'):
      label = msg.label
    return ClusterEntity(token_span, bbox, label)

  def to_proto(self) -> entity_pb2.Cluster:
    msg = entity_pb2.Cluster(bbox=self.bbox.to_proto())
    msg.token_span.CopyFrom(self.token_span.to_proto())
    if self.label is not None:
      msg.label = self.label
    return msg

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
    ValueError: If msg is a GenericEntity and no custom Entity class is
                found in entity_registry for the 'msg.custom.type' field.
    AssertionError: If not all payload types (defined in the .proto spec) are
                    cased in this function.
  """
  payload_type = msg.WhichOneof('payload')
  if payload_type == 'word':
    return WordEntity.from_proto(msg.word)
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
    return PhraseEntity.from_proto(msg.phrase)
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

  assert_exhaustive(payload_type)


def entity_to_proto(entity: Entity) -> entity_pb2.Entity:
  """Handles dispatching Entity serialization to subclasses of Entity.

  In the proto definition, entity_pb2.Entity is a message containing a payload
  which is any of the possible Entity types. This function wraps the result of
  Entity.to_proto in the payload of entity_pb2.Entity.

  Args:
    entity: A Foundation Entity instance.
  Returns:
    A protobuf entity_pb2.Entity message.
  Raises:
    AssertionError: If not all payload types (defined in the .proto spec) are
                    cased in this function.
  """
  payload = entity.to_proto()
  if isinstance(payload, entity_pb2.Word):
    return entity_pb2.Entity(word=payload)
  elif isinstance(payload, entity_pb2.Line):
    return entity_pb2.Entity(line=payload)
  elif isinstance(payload, entity_pb2.Paragraph):
    return entity_pb2.Entity(paragraph=payload)
  elif isinstance(payload, entity_pb2.TableCell):
    return entity_pb2.Entity(table_cell=payload)
  elif isinstance(payload, entity_pb2.TableRow):
    return entity_pb2.Entity(table_row=payload)
  elif isinstance(payload, entity_pb2.Table):
    return entity_pb2.Entity(table=payload)
  elif isinstance(payload, entity_pb2.Token):
    return entity_pb2.Entity(token=payload)
  elif isinstance(payload, entity_pb2.Phrase):
    return entity_pb2.Entity(phrase=payload)
  elif isinstance(payload, entity_pb2.Number):
    return entity_pb2.Entity(number=payload)
  elif isinstance(payload, entity_pb2.Integer):
    return entity_pb2.Entity(integer=payload)
  elif isinstance(payload, entity_pb2.Date):
    return entity_pb2.Entity(date=payload)
  elif isinstance(payload, entity_pb2.Time):
    return entity_pb2.Entity(time=payload)
  elif isinstance(payload, entity_pb2.Currency):
    return entity_pb2.Entity(currency=payload)
  elif isinstance(payload, entity_pb2.Name):
    return entity_pb2.Entity(name=payload)
  elif isinstance(payload, entity_pb2.Address):
    return entity_pb2.Entity(address=payload)
  elif isinstance(payload, entity_pb2.Cluster):
    return entity_pb2.Entity(cluster=payload)
  elif isinstance(payload, entity_pb2.GenericEntity):
    return entity_pb2.Entity(custom=payload)

  assert_exhaustive(payload)
