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
                            entity_pb2.Number, entity_pb2.Integer,
                            entity_pb2.Date, entity_pb2.Time,
                            entity_pb2.Currency, entity_pb2.PersonName,
                            entity_pb2.Address, entity_pb2.Cluster,
                            entity_pb2.GenericEntity]

E = TypeVar('E', bound='Entity')


class Entity(abc.ABC, Generic[E]):
  bbox: BBox

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
  def children(self) -> Iterable['Entity']:
    """Yields all sub-entities of this entity.

    See implementing subclass methods for entity-specific definitions.
    Can be seen as returning the adjacent entities in a document's Entity
    DAG.

    This method CANNOT call ocr_words().
    """
    ...

  def ocr_words(self) -> Iterable['Word']:
    """Yields all OcrWordEntity's among this entity's children.

    Can be seen as returning an iterator over the leaves of this
    Entity's DAG.

    If this Entity is a WORD, yields itself.

    STRONGLY RECOMMENDED not to override this.
    """
    yield from chain.from_iterable(e.ocr_words() for e in self.children)


@dataclass(frozen=True)
class Word(Entity):
  text: str
  bbox: BBox
  origin: Optional[InputWord] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Word':
    assert isinstance(msg, entity_pb2.Word)
    text = msg.text
    bbox = unwrap(BBox.from_proto(msg.bbox))  # TODO: what does None mean here?
    input_word = None
    if msg.HasField('origin'):
      input_word = InputWord.from_proto(msg.origin)
    return Word(text, bbox, input_word)

  def to_proto(self) -> entity_pb2.Word:
    msg = entity_pb2.Word(text=self.text, bbox=self.bbox.to_proto())
    if self.origin is not None:
      msg.origin.CopyFrom(self.origin.to_proto())
    return msg

  @property
  def children(self) -> Iterable[E]:
    """ Word has no children. """
    yield from []

  def ocr_words(self) -> Iterable['Word']:
    """ Yields itself.

    This provides the base case for Entity.ocr_words.
    """
    yield self


@dataclass(frozen=True)
class Line(Entity):
  _ocr_words: List[Word]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Line':
    assert isinstance(msg, entity_pb2.Line)
    bbox = unwrap(BBox.from_proto(msg.bbox))
    ocr_words = [Word.from_proto(w) for w in msg.words]
    return Line(ocr_words, bbox)

  def to_proto(self) -> entity_pb2.Line:
    msg = entity_pb2.Line(bbox=self.bbox.to_proto())
    msg.words.extend(w.to_proto() for w in self._ocr_words)
    return msg

  @property
  def children(self) -> Iterable[Word]:
    """ A Line's children are its OCR words. """
    yield from self._ocr_words


@dataclass(frozen=True)
class Paragraph(Entity):
  lines: List[Line]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Paragraph':
    assert isinstance(msg, entity_pb2.Paragraph)
    lines = [Line.from_proto(l) for l in msg.lines]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return Paragraph(lines, bbox)

  def to_proto(self) -> entity_pb2.Paragraph:
    msg = entity_pb2.Paragraph(bbox=self.bbox.to_proto())
    msg.lines.extend(l.to_proto() for l in self.lines)
    return msg

  @property
  def children(self) -> Iterable[Line]:
    """ A Paragraph's children are its Lines. """
    yield from self.lines


@dataclass(frozen=True)
class TableCell(Entity):
  content: List[Entity]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableCell':
    assert isinstance(msg, entity_pb2.TableCell)
    content = [proto_to_entity(e) for e in msg.content]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return TableCell(content, bbox)

  def to_proto(self) -> entity_pb2.TableCell:
    msg = entity_pb2.TableCell(bbox=self.bbox.to_proto())
    msg.content.extend(entity_to_proto(e) for e in self.content)
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A TableCell's children are its contents. """
    yield from self.content


@dataclass(frozen=True)
class TableRow(Entity):
  cells: List[TableCell]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'TableRow':
    assert isinstance(msg, entity_pb2.TableRow)
    cells = [TableCell.from_proto(c) for c in msg.cells]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return TableRow(cells, bbox)

  def to_proto(self) -> entity_pb2.TableRow:
    msg = entity_pb2.TableRow(bbox=self.bbox.to_proto())
    msg.cells.extend(c.to_proto() for c in self.cells)
    return msg

  @property
  def children(self) -> Iterable[TableCell]:
    """ A TableRow's children are its cells. """
    yield from self.cells


@dataclass(frozen=True)
class Table(Entity):
  rows: List[TableRow]
  bbox: BBox

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Table':
    assert isinstance(msg, entity_pb2.Table)
    rows = [TableRow.from_proto(r) for r in msg.rows]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    return Table(rows, bbox)

  def to_proto(self) -> entity_pb2.Table:
    msg = entity_pb2.Table(bbox=self.bbox.to_proto())
    msg.rows.extend(r.to_proto() for r in self.rows)
    return msg

  @property
  def children(self) -> Iterable[TableRow]:
    """ A Table's children are its rows. """
    yield from self.rows


@dataclass(frozen=True)
class Number(Entity):
  span: List[Word]
  bbox: BBox
  value: Optional[float] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Number':
    assert isinstance(msg, entity_pb2.Number)
    span = [Word.from_proto(w) for w in msg.span]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return Number(span, bbox, value)

  def to_proto(self) -> entity_pb2.Number:
    msg = entity_pb2.Number(bbox=self.bbox.to_proto())
    msg.span.extend(w.to_proto() for w in self.span)
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A Number's children are the words it spans. """
    yield from self.span


@dataclass(frozen=True)
class Integer(Entity):
  span: List[Word]
  bbox: BBox
  value: Optional[int] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Integer':
    assert isinstance(msg, entity_pb2.Integer)
    span = [Word.from_proto(w) for w in msg.span]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return Integer(span, bbox, value)

  def to_proto(self) -> entity_pb2.Integer:
    msg = entity_pb2.Integer(bbox=self.bbox.to_proto())
    msg.span.extend(w.to_proto() for w in self.span)
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ An Integer's children are the words it spans. """
    yield from self.span


@dataclass(frozen=True)
class Date(Entity):
  span: List[Word]
  bbox: BBox
  value: Optional[str] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Date':
    assert isinstance(msg, entity_pb2.Date)
    span = [Word.from_proto(w) for w in msg.span]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return Date(span, bbox, value)

  def to_proto(self) -> entity_pb2.Date:
    msg = entity_pb2.Date(bbox=self.bbox.to_proto())
    msg.span.extend(w.to_proto() for w in self.span)
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A Date's children are the words it spans. """
    yield from self.span


@dataclass(frozen=True)
class Time(Entity):
  span: List[Word]
  bbox: BBox
  value: Optional[int] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Time':
    assert isinstance(msg, entity_pb2.Time)
    span = [Word.from_proto(w) for w in msg.span]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return Time(span, bbox, value)

  def to_proto(self) -> entity_pb2.Time:
    msg = entity_pb2.Time(bbox=self.bbox.to_proto())
    msg.span.extend(w.to_proto() for w in self.span)
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A Time's children are the words it spans. """
    yield from self.span


@dataclass(frozen=True)
class Currency(Entity):
  span: List[Word]
  bbox: BBox
  # TODO: wrap FixedDecimal
  value: Optional[Currency_pb2.FixedDecimal] = None
  units: Optional[str] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Currency':
    assert isinstance(msg, entity_pb2.Currency)
    span = [Word.from_proto(w) for w in msg.span]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    units = None
    if msg.HasField('units'):
      units = msg.units
    value = None
    if msg.HasField('value'):
      value = msg.value
    return Currency(span, bbox, value, units)

  def to_proto(self) -> entity_pb2.Currency:
    msg = entity_pb2.Currency(bbox=self.bbox.to_proto())
    msg.span.extend(w.to_proto() for w in self.span)
    if self.value is not None:
      msg.value.CopyFrom(self.value)
    if self.units is not None:
      msg.units = self.units
    return msg

  @property
  def children(self) -> Iterable[Entity]:
    """ A Currency's children are the words it spans. """
    yield from self.span


@dataclass(frozen=True)
class PersonName(Entity):
  name_parts: List[Line]
  bbox: BBox
  value: Optional[str] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'PersonName':
    assert isinstance(msg, entity_pb2.PersonName)
    name_parts = [Line.from_proto(n) for n in msg.name_parts]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return PersonName(name_parts, bbox, value)

  def to_proto(self) -> entity_pb2.PersonName:
    msg = entity_pb2.PersonName(bbox=self.bbox.to_proto())
    msg.name_parts.extend(p.to_proto() for p in self.name_parts)
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Line]:
    """ A PersonName's children are the Lines of its name parts. """
    yield from self.name_parts


@dataclass(frozen=True)
class Address(Entity):
  lines: List[Line]
  bbox: BBox
  value: Optional[str] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Address':
    assert isinstance(msg, entity_pb2.Address)
    lines = [Line.from_proto(l) for l in msg.lines]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    value = None
    if msg.HasField('value'):
      value = msg.value
    return Address(lines, bbox, value)

  def to_proto(self) -> entity_pb2.Address:
    msg = entity_pb2.Address(bbox=self.bbox.to_proto())
    msg.lines.extend(l.to_proto() for l in self.lines)
    if self.value is not None:
      msg.value = self.value
    return msg

  @property
  def children(self) -> Iterable[Line]:
    """ A Address's children are the Lines it's composed of. """
    yield from self.lines


@dataclass(frozen=True)
class Cluster(Entity):
  span: List[Line]
  bbox: BBox
  label: Optional[str] = None

  @staticmethod
  def from_proto(msg: PbEntityPayloadType) -> 'Cluster':
    assert isinstance(msg, entity_pb2.Cluster)
    span = [Line.from_proto(l) for l in msg.span]
    bbox = unwrap(BBox.from_proto(msg.bbox))
    label = None
    if msg.HasField('label'):
      label = msg.label
    return Cluster(span, bbox, label)

  def to_proto(self) -> entity_pb2.Cluster:
    msg = entity_pb2.Cluster(bbox=self.bbox.to_proto())
    msg.span.extend(l.to_proto() for l in self.span)
    if self.label is not None:
      msg.label = self.label
    return msg

  @property
  def children(self) -> Iterable[Line]:
    """ A Cluster's children are Lines that it spans. """
    yield from self.span


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
    return Word.from_proto(msg.word)
  elif payload_type == 'line':
    return Line.from_proto(msg.line)
  elif payload_type == 'paragraph':
    return Paragraph.from_proto(msg.paragraph)
  elif payload_type == 'table_cell':
    return TableCell.from_proto(msg.table_cell)
  elif payload_type == 'table_row':
    return TableRow.from_proto(msg.table_row)
  elif payload_type == 'table':
    return Table.from_proto(msg.table)
  elif payload_type == 'number':
    return Number.from_proto(msg.number)
  elif payload_type == 'integer':
    return Integer.from_proto(msg.integer)
  elif payload_type == 'date':
    return Date.from_proto(msg.date)
  elif payload_type == 'time':
    return Time.from_proto(msg.time)
  elif payload_type == 'currency':
    return Currency.from_proto(msg.currency)
  elif payload_type == 'name':
    return PersonName.from_proto(msg.name)
  elif payload_type == 'address':
    return Address.from_proto(msg.address)
  elif payload_type == 'cluster':
    return Cluster.from_proto(msg.cluster)
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
  elif isinstance(payload, entity_pb2.PersonName):
    return entity_pb2.Entity(name=payload)
  elif isinstance(payload, entity_pb2.Address):
    return entity_pb2.Entity(address=payload)
  elif isinstance(payload, entity_pb2.Cluster):
    return entity_pb2.Entity(cluster=payload)
  elif isinstance(payload, entity_pb2.GenericEntity):
    return entity_pb2.Entity(custom=payload)

  assert_exhaustive(payload)
