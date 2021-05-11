""" Foundation document structures. """

import json

from dataclasses import asdict, dataclass, field, replace
from functools import lru_cache
from itertools import chain
from pathlib import Path
from typing import Dict, Optional, Iterable, Tuple, Type, TypeVar

from .entity import Entity, Word, entity_resolver
from .geometry import BBox
from .instantiate import instantiate
from .typing_utils import unwrap


E = TypeVar('E', bound=Entity)


@dataclass(frozen=True)
class Document:
  """A Foundation Document is a collection of Entities of varying type."""
  bbox: BBox
  entities: Tuple[Entity, ...] = field(default_factory=tuple)
  name: Optional[str] = None

  @staticmethod
  def from_entities(
    entities: Iterable[Entity], name: Optional[str] = None) -> 'Document':
    """Construct a Document from entities."""
    entities = tuple(entities)
    bbox = unwrap(BBox.union(e.bbox for e in entities))
    return Document(bbox, entities, name)

  def with_entities(self, entities: Iterable[Entity]) -> 'Document':
    """Returns a copy of this Document with given entities added and bbox
    adjusted to include the new entities."""
    return Document.from_entities(
      tuple(chain(self.entities, entities)), self.name)

  def filter_entities(self, entity_type: Type[E]) -> Iterable[E]:
    yield from (e for e in self.entities if isinstance(e, entity_type))

  @lru_cache(maxsize=None)
  def median_line_height(self) -> float:
    return median_word_height(
      chain.from_iterable(
        E.entity_words() for E in self.entities))


def median_word_height(words: Iterable[Word]) -> float:
  L = sorted(words, key=lambda W: W.height)
  if not L:
    return 0
  n = len(L)
  if n % 2 == 0:
    return 0.5 * (L[n // 2 - 1].height + L[n // 2].height)
  return L[(n - 1) // 2].height


def load_fnd_doc_from_json(blob: Dict) -> Document:
  return instantiate(
    Document,
    blob,
    base_classes={Entity},
    derived_class_resolver=entity_resolver)


def load_document(path: Path) -> Document:
  with path.open() as f:
    return load_fnd_doc_from_json(json.load(f))


def dump_to_json(root: Document) -> str:
  return json.dumps(asdict(root))


def save_document(root: Document, path: Path) -> None:
  with path.open('w') as f:
    f.write(dump_to_json(root) + '\n')
