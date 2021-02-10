"""Entity types."""

from dataclasses import dataclass
from itertools import chain
from typing import Dict, Generic, Iterable, Optional, Tuple, Type

from .geometry import BBox
from .ocr import InputWord
from .typing_utils import assert_exhaustive, unwrap


@dataclass(frozen=True)
class Entity:
  bbox: BBox
  type: str = 'Entity'

  @property
  def text(self) -> str:
    raise NotImplementedError

  def height(self) -> float:
    return self.bbox.height

  @property
  def children(self) -> Iterable['Entity']:
    """Yields all sub-entities of this entity.

    See implementing subclass methods for entity-specific definitions.
    Can be seen as returning the adjacent entities in a document's Entity
    DAG.

    This method CANNOT call words().
    """
    raise NotImplementedError

  def words(self) -> Iterable['Word']:
    """Yields all Word entities among this entity's children.

    Can be seen as returning an iterator over the leaves of this
    Entity's DAG.

    If this Entity is a Word, yields itself.

    STRONGLY RECOMMENDED not to override this.
    """
    yield from chain.from_iterable(E.words() for E in self.children)


@dataclass(frozen=True)
class Page(Entity):
  """A Page is defined by an image region, or region in a document.

  Its bounding box is its dimensions, translated by its offset within the
  document. For example, a document with 3 pages, each 50x100, "stacking"
  pages on top of each other would put page 2's bbox as:
      top_left: (0, 100), bottom_right: (50, 200)
  """
  index: int
  type: str = 'Page'

  @property
  def children(self) -> Iterable['Entity']:
    """A page has no children.

    It is simply a region.
    """
    yield from []


@dataclass(frozen=True)
class Word(Entity):
  _text: str
  origin: Optional[InputWord] = None
  type: str = 'Word'

  @property
  def text(self) -> str:
    return self._text

  @staticmethod
  def from_input_word(origin: InputWord) -> 'Word':
    text = origin.text or ''
    return Word(origin.bbox, text, origin)

  @property
  def children(self) -> Iterable[Entity]:
    """Words have no children."""
    yield from []

  def words(self) -> Iterable['Word']:
    """Yields itself.

    This provides the base case for Entity.words.
    """
    yield self


@dataclass(frozen=True)
class Line(Entity):
  """A horizontal line of text.

  In most cases, this would originate from an OCR line.
  """
  _words: Tuple[Word, ...]
  type: str = 'Line'

  @property
  def text(self) -> str:
    return ' '.join(word.text for word in self._words)

  @staticmethod
  def from_phrase(phrase: 'Phrase') -> 'Line':
    """Cast/reinterpret a Phrase as a Line."""
    return Line(phrase.bbox, tuple(phrase.words()))

  @property
  def children(self) -> Iterable[Word]:
    """A Line's children are its OCR words."""
    yield from self._words


@dataclass(frozen=True)
class Phrase(Entity):
  """A sequence of words contiguous on the same line."""
  _text: str
  _words: Tuple[Word, ...]
  type: str = 'Phrase'

  @property
  def text(self) -> str:
    return self._text

  @staticmethod
  def from_line(line: Line) -> 'Phrase':
    """Cast/reinterpret a Line as a Phrase."""
    words = tuple(line.words())
    text = ' '.join(word.text for word in words)
    return Phrase(line.bbox, text, words)

  @staticmethod
  def from_words(words: Tuple[Word, ...]) -> 'Phrase':
    if not all(isinstance(word, Word) for word in words):
      raise ValueError('Phrase must be built from Words')
    bbox = unwrap(BBox.union(word.bbox for word in words))
    text = ' '.join(word.text for word in words)
    return Phrase(bbox, text, words)

  @property
  def children(self) -> Iterable[Word]:
    yield from self._words


@dataclass(frozen=True)
class Cluster(Entity):
  lines: Tuple[Phrase, ...]
  label: Optional[str] = None
  type: str = 'Cluster'

  @property
  def text(self) -> str:
    return '\n'.join(line.text for line in self.lines)

  @property
  def children(self) -> Iterable[Phrase]:
    """A Cluster's children are Phrases that it spans."""
    yield from self.lines


@dataclass(frozen=True)
class Date(Entity):
  span: Tuple[Word, ...]
  value: Optional[str] = None
  likeness_score: Optional[float] = None
  type: str = 'Date'

  @property
  def text(self) -> str:
    return self.value if self.value else ''

  @property
  def children(self) -> Iterable[Entity]:
    """A Date's children are the words it spans."""
    yield from self.span


@dataclass(frozen=True)
class Currency(Entity):
  span: Tuple[Word, ...]
  value: Optional[str] = None
  units: Optional[str] = None
  likeness_score: Optional[float] = None
  type: str = 'Currency'

  @property
  def text(self) -> str:
    return self.value if self.value else ''

  @property
  def children(self) -> Iterable[Entity]:
    """A Currency's children are the words it spans."""
    yield from self.span


@dataclass(frozen=True)
class Paragraph(Entity):
  lines: Tuple[Line, ...]
  type: str = 'Paragraph'

  @property
  def text(self) -> str:
    return '\n'.join(line.text for line in self.lines)

  @property
  def children(self) -> Iterable[Line]:
    """A Paragraph's children are its Lines."""
    yield from self.lines


@dataclass(frozen=True)
class TableCell(Entity):
  content: Tuple[Entity, ...]
  type: str = 'TableCell'

  @property
  def text(self) -> str:
    return ' '.join(entity.text for entity in self.content)

  @property
  def children(self) -> Iterable[Entity]:
    """A TableCell's children are its contents."""
    yield from self.content


@dataclass(frozen=True)
class TableRow(Entity):
  cells: Tuple[TableCell, ...]
  type: str = 'TableRow'

  @property
  def text(self) -> str:
    return ' '.join(cell.text for cell in self.cells)

  @property
  def children(self) -> Iterable[TableCell]:
    """A TableRow's children are its cells."""
    yield from self.cells


@dataclass(frozen=True)
class Table(Entity):
  rows: Tuple[TableRow, ...]
  type: str = 'Table'

  @property
  def text(self) -> str:
    return '\n'.join(row.text for row in self.rows)

  @property
  def children(self) -> Iterable[TableRow]:
    """A Table's children are its rows."""
    yield from self.rows


@dataclass(frozen=True)
class Number(Entity):
  span: Tuple[Word, ...]
  value: Optional[float] = None
  type: str = 'Number'

  @property
  def text(self) -> str:
    return str(self.value) if self.value else ''

  @property
  def children(self) -> Iterable[Entity]:
    """A Number's children are the words it spans."""
    yield from self.span


@dataclass(frozen=True)
class Integer(Entity):
  span: Tuple[Word, ...]
  value: Optional[int] = None
  type: str = 'Number'

  @property
  def text(self) -> str:
    return str(self.value) if self.value else ''

  @property
  def children(self) -> Iterable[Entity]:
    """An Integer's children are the words it spans."""
    yield from self.span


@dataclass(frozen=True)
class Time(Entity):
  span: Tuple[Word, ...]
  value: Optional[int] = None
  likeness_score: Optional[float] = None
  type: str = 'Time'

  @property
  def text(self) -> str:
    return str(self.value) if self.value else ''

  @property
  def children(self) -> Iterable[Entity]:
    """A Time's children are the words it spans."""
    yield from self.span


@dataclass(frozen=True)
class PersonName(Entity):
  name_parts: Tuple[Line, ...]
  value: Optional[str] = None
  likeness_score: Optional[float] = None
  type: str = 'PersonName'

  @property
  def text(self) -> str:
    return self.value if self.value else ''

  @property
  def children(self) -> Iterable[Line]:
    """A PersonName's children are the Lines of its name parts."""
    yield from self.name_parts


@dataclass(frozen=True)
class Address(Entity):
  lines: Tuple[Line, ...]
  value: Optional[str] = None
  likeness_score: Optional[float] = None
  type: str = 'Address'

  @property
  def text(self) -> str:
    return self.value if self.value else ''

  @property
  def children(self) -> Iterable[Line]:
    """An Address's children are the Lines it's composed of."""
    yield from self.lines


@dataclass(frozen=True)
class NamedEntity(Entity):
  span: Tuple[Word, ...]
  value: Optional[str] = None
  label: Optional[str] = None
  type: str = 'NamedEntity'

  @property
  def text(self) -> str:
    return self.value if self.value else ''

  @property
  def children(self) -> Iterable[Entity]:
    """An entities children are the words it spans."""
    yield from self.span


"""
Associates a string entity type name to a custom class that inherits from
Entity.
"""
CustomEntityRegistry = Dict[str, Type[Entity]]

entity_registry = {
  'Address': Address,
  'Cluster': Cluster,
  'Currency': Currency,
  'Date': Date,
  'Integer': Integer,
  'Line': Line,
  'NamedEntity': NamedEntity,
  'Number': Number,
  'Page': Page,
  'Paragraph': Paragraph,
  'PersonName': PersonName,
  'Phrase': Phrase,
  'Table': Table,
  'TableCell': TableCell,
  'TableRow': TableRow,
  'Time': Time,
  'Word': Word,
}
