""" Foundation document structures. """

import json

from dataclasses import asdict, dataclass, field
from functools import lru_cache
from itertools import chain
from pathlib import Path
from typing import Dict, Iterable, List, Type, TypeVar

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
  entities: Tuple[Entity, ...] = field(default_factory=tuple)
  name: Optional[str] = None

  @staticmethod
  def from_entities(
    entities: Iterable[Entity], name: Optional[str] = None) -> 'Document':
    """Construct a Document with bbox from entities."""
    entities = tuple(entities)
    bbox = unwrap(BBox.union(e.bbox for e in entities))
    return Document(bbox, entities, name)

  def with_entities(self, entities: Iterable[Entity]) -> 'Document':
    """Returns a copy of this Document with given entities added. """
    return Document.from_entities(tuple(chain(self.entities, entities)))

  def filter_entities(self, entity_type: Type[E]) -> Iterable[E]:
    yield from (e for e in self.entities if isinstance(e, entity_type))

  @lru_cache(maxsize=None)
  def median_line_height(self) -> float:
    return InputWord.median_word_height(word.origin for word in filter( # type: ignore
      lambda W: W.origin is not None, chain.from_iterable(E.words()
        for E in self.entities)))


# Work in progress
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
