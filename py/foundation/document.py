""" Foundation document structures. """

from dataclasses import dataclass, field
from itertools import chain
from typing import Tuple, Iterable, Type, TypeVar

from .entity import Entity


E = TypeVar('E', bound=Entity)


@dataclass(frozen=True)
class Document:
  """A Foundation Document is a collection of Entity.
  """
  entities: Tuple[Entity, ...] = field(default_factory=tuple)

  def with_entities(self, entities: Iterable[Entity]) -> 'Document':
    """Returns a copy of this Document with given entities added. """
    return Document(tuple(chain(self.entities, entities)))

  def filter_entities(self, entity_type: Type[E]) -> Iterable[E]:
    yield from (e for e in self.entities if isinstance(e, entity_type))
