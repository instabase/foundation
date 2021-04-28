from abc import abstractmethod
from typing import Dict, Optional, Iterable
from typing_extensions import Protocol

from itertools import chain

from .geometry import BBox

class Entity(Protocol):
  @property
  @abstractmethod
  def id(self) -> str: ...

  @property
  @abstractmethod
  def type(self) -> str: ...
  
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

class Image(Protocol):
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