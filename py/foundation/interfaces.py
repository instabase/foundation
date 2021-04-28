from abc import abstractmethod
from typing import Any, Dict, Optional, Iterable
from typing_extensions import Protocol

from itertools import chain

from .meta import FoundationType
from .geometry import BBox

class Entity(FoundationType):
  @property
  @abstractmethod
  def id(self) -> str: ...
  
  @property
  def bbox(self) -> BBox:
    return BBox.union(self.get_bboxes())
  
  @abstractmethod
  def get_children(self) -> Iterable['Entity']: ...

  def get_bboxes(self) -> Iterable[BBox]:
    yield from chain.from_iterable(c.get_bboxes() for c in self.get_children())

class Word(Entity):
  @property
  @abstractmethod
  def text(self) -> str: ...

  @property
  def char_width(self) -> float:
    return self.bbox.width/len(self)

  def __len__(self) -> int:
    return len(self.text)

class Text(Entity):
  @abstractmethod
  def get_children(self) -> Iterable[Word]: ...

  def __len__(self) -> int:
    return sum(len(c) for c in self.get_children())

class Image(FoundationType):
  @property
  @abstractmethod
  def bbox(self) -> BBox: ...

  @property
  @abstractmethod
  def input_filepath(self) -> str: ...

class Page(Entity):
  @property
  @abstractmethod
  def page_index(self) -> int: ...

  @property
  @abstractmethod
  def image(self) -> Image: ...


class RecordContext(FoundationType):
  @abstractmethod
  def get_entities(self) -> Iterable[Entity]: 
    """
    Returns all entities associated with this record (including Words)
    """
    ...

  @abstractmethod
  def get_pages(self) -> Iterable[Page]: 
    """
    Returns the page entities associated with this record in order
    """
    ...

  @abstractmethod
  def get_collection_entities(self) -> Iterable[Entity]:
    """
    Returns the non-word entities associated with this Record
    """
    ...

  # @abstractmethod
  # def as_dict(self) -> Dict:
  #   """
  #   Serializes this RecordContext to JSON
  #   """
  #   ...

  # @staticmethod
  # @abstractmethod
  # def from_dict(record_dict: Dict) -> 'RecordContext':
  #   ...