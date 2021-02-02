""" Foundation document structures. """

import json

from dataclasses import asdict, dataclass, field
from itertools import chain
from pathlib import Path
from typing import Dict, Tuple, Iterable, Type, TypeVar

from .entity import *
from .geometry import BBox
from .typing_utils import unwrap
from ._instantiate import _instantiate


E = TypeVar('E', bound=Entity)


@dataclass(frozen=True)
class Document:
  """A Foundation Document is a collection of Entities of varying type.
  """
  bbox: BBox
  pages: Tuple[Page, ...] = field(default_factory=tuple)
  words: Tuple[Word, ...] = field(default_factory=tuple)
  phrases: Tuple[Phrase, ...] = field(default_factory=tuple)
  paragraphs: Tuple[Paragraph, ...] = field(default_factory=tuple)
  tables: Tuple[Table, ...] = field(default_factory=tuple)
  numbers: Tuple[Number, ...] = field(default_factory=tuple)
  integers: Tuple[Integer, ...] = field(default_factory=tuple)
  dates: Tuple[Date, ...] = field(default_factory=tuple)
  times: Tuple[Time, ...] = field(default_factory=tuple)
  currencies: Tuple[Currency, ...] = field(default_factory=tuple)
  person_names: Tuple[PersonName, ...] = field(default_factory=tuple)
  addresses: Tuple[Address, ...] = field(default_factory=tuple)
  clusters: Tuple[Cluster, ...] = field(default_factory=tuple)
  named_entities: Tuple[NamedEntity, ...] = field(default_factory=tuple)

  @property
  def entities(self) -> Tuple[Entity, ...]:
    return tuple(chain(self.pages, self.words, self.phrases, self.paragraphs,
                  self.tables, self.numbers, self.integers, self.dates,
                  self.times, self.currencies, self.person_names,
                  self.addresses, self.clusters, self.named_entities))

  # @staticmethod
  # def from_entities(entities: Iterable[Entity]) -> 'Document':
  #   """Construct a Document with bbox from entities."""
  #   entities = tuple(entities)
  #   bbox = unwrap(BBox.union(e.bbox for e in entities))
  #   return Document(bbox, entities)

  # def with_entities(self, entities: Iterable[Entity]) -> 'Document':
  #   """Returns a copy of this Document with given entities added. """
  #   return Document.from_entities(tuple(chain(self.entities, entities)))

  def filter_entities(self, entity_type: Type[E]) -> Iterable[E]:
    yield from (e for e in self.entities if isinstance(e, entity_type))


def load_fnd_doc_from_json(blob: Dict) -> Document:
  forward_ref_resolver = {
    'BBox': BBox,
    'Entity': Entity,
  }
  # return validate(_instantiate(Document, blob, forward_ref_resolver))
  return _instantiate(Document, blob, forward_ref_resolver)


def load_document(path: Path) -> Document:
  with path.open() as f:
    return load_fnd_doc_from_json(json.load(f))


def dump_to_json(root: Document) -> str:
  # return json.dumps(asdict(validate(root)), indent=2, sort_keys=True)
  return json.dumps(asdict(root), indent=2, sort_keys=True)


def save_document(root: Document, path: Path) -> None:
  with path.open('w') as f:
    f.write(dump_to_json(root) + '\n')
