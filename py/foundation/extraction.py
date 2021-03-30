"""Data structures describing extraction results.

Typically an extraction is represented as a dictionary from some fields to some
document entities.
"""

from dataclasses import asdict, dataclass, replace
from typing import Any, Collection, Dict, FrozenSet, Generator, Optional, Tuple

from foundation.entity import Entity
from foundation.geometry import BBox

from .document import DocRegion
from .functional import arg_max, arg_min, comma_sep, pairwise_disjoint


"""An ID for "something we wish to extract" in a document.

If you want to extract a thing from a document (a numeric value, an anchor, some
text, whatever), you need to represent it as an extraction field. An extraction
field is just a name for a thing-to-be-extracted. You can think of a field as
the analog of a variable in another modeling language. A Blueprint extraction
consists of assignments from a set of fields to entities in a document.
"""
Field = str


Assignment = Optional[Entity]


class MissingFieldsError(KeyError):
  """A function or operation was passed a collection of fields that was missing
  required fields."""
  pass


class OverlappingFieldsError(KeyError):
  """A function or operation was passed collections of fields that overlap
  unexpectedly."""
  pass


class UnrecognizedFieldsError(KeyError):
  """A function or operation was passed unrecognized fields."""
  pass


@dataclass(frozen=True)
class ExtractionPoint:
  """A (field, entity) pair."""
  field: Field
  entity: Optional[Entity]

  @property
  def assignment_text(self) -> Optional[str]:
    """The entity text, or None."""
    return self.entity.entity_text if self.entity else None

  @property
  def assignment_str(self) -> str:
    """The entity text in quotes, or 'None'."""
    return f'"{self.entity}"' if self.entity else 'None'

  def __str__(self) -> str:
    return f'{self.field} -> {self.entity}'


@dataclass(frozen=True)
class Extraction:
  """An assignment from some fields to some entities in some document.

  When we say we "want to extract the net and gross pay", another way of framing
  the problem is that we want something like this:

    {
      'net_pay': <something in the document>,
      'gross_pay': <something in the document>,
    }

  We call such a dictionary an *extraction*. Extractions can be good or bad,
  "right" or "wrong". The goal of a Blueprint model is to find good
  extractions. Blueprint's library of rules enable you to describe good
  extractions look and behave, by listing rules that the fields should follow.
  """

  assignments: Tuple[ExtractionPoint, ...]

  @property
  def fields(self) -> FrozenSet[Field]:
    """The fields for which this extraction has entity assignments."""
    return frozenset(self.dictionary.keys())

  @property
  def entities(self) -> FrozenSet[Entity]:
    """The entity assignments for this extraction."""
    return frozenset(self.dictionary.values())

  @property
  def is_empty(self) -> bool:
    return self.dictionary == {}

  def __bool__(self) -> bool:
    return not self.is_empty

  def __getitem__(self, field: Field) -> Entity:
    """The entity this field is assigned to under this extraction.

    Args:
      field: A field. This must be present in the extraction. Check whether the
        field is in the extraction before calling this method.
    """
    if field not in self:
      raise UnrecognizedFieldsError(f'{field} not found in {self}')
    return self.dictionary[field]

  def __eq__(self, other: Any) -> bool:
    return isinstance(other, Extraction) and \
            self.dictionary == other.dictionary

  def __contains__(self, field: Field) -> bool:
    return field in self.dictionary

  def __len__(self) -> int:
    return len(self.dictionary)

  def point(self, field: Field) -> ExtractionPoint:
    """The (field, entity) pair for this field in this extraction.

    May return (field, None).

    This is mostly used for logging/printing.

    Args:
      field: A field. If this field is not present in the extraction, this
        function returns (field, None).
    """
    return ExtractionPoint(field, self[field] if field in self else None)

  def points(self) -> Generator[ExtractionPoint, None, None]:
    """The points in this extraction, sorted by field name."""
    for field in sorted(self.fields):
      yield self.point(field)

  @staticmethod
  def merge(extractions: Collection['Extraction']) -> 'Extraction':
    """Combine several extractions into one.

    Args:
      extractions: Input extractions. These must not have any fields in common.
    """

    if not pairwise_disjoint(extraction.fields for extraction in extractions):
      raise OverlappingFieldsError(f'cannot merge extractions {extractions}')

    dictionary: Dict[Field, Entity] = {}
    for extraction in extractions:
      dictionary.update(extraction.dictionary)
    return Extraction(dictionary)

  def __str__(self) -> str:
    return f'[{comma_sep(self.points())}]'

  def __repr__(self) -> str:
    return f'<Extraction({comma_sep(self.points())})>'
