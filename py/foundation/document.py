""" Foundation document structures. """

from dataclasses import dataclass, field
from itertools import chain
from typing import Tuple, Iterable, Type, TypeVar

from .entity import Entity
from .geometry import BBox
from .typing_utils import unwrap

E = TypeVar('E', bound=Entity)


@dataclass(frozen=True)
class Document:
  """A Foundation Document is a collection of Entity.
  """
  bbox: BBox
  entities: Tuple[Entity, ...] = field(default_factory=tuple)

  @staticmethod
  def from_entities(entities: Iterable[Entity]) -> 'Document':
    """Construct a Document with bbox from entities."""
    entities = tuple(entities)
    bbox = unwrap(BBox.union(e.bbox for e in entities))
    return Document(bbox, entities)

  def with_entities(self, entities: Iterable[Entity]) -> 'Document':
    """Returns a copy of this Document with given entities added. """
    return Document.from_entities(tuple(chain(self.entities, entities)))

  def filter_entities(self, entity_type: Type[E]) -> Iterable[E]:
    yield from (e for e in self.entities if isinstance(e, entity_type))
