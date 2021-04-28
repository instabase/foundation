from typing import Dict, Optional, Iterable
from typing_extensions import Protocol

from .geometry import BBox

class Entity(Protocol):
  @property
  def id(self) -> str: ...

  @property
  def type(self) -> str: ...
  
  @property
  def bbox(self) -> BBox: ...

  def get_bboxes(self) -> Iterable[BBox]: ...
  
  def get_children(self) -> Iterable['Entity']: ...

class Word(Entity):
  @property
  def text(self) -> str: ...

  @property
  def char_width(self) -> float:
    return self.bbox.width/len(self)

  def __len__(self) -> int:
    return len(self.text)

class Text(Entity):
  def __len__(self) -> int: ...

class Image(Protocol):
  @property
  def bbox(self) -> BBox: ...

  @property
  def input_filepath(self) -> str: ...

class Page(Entity):
  @property
  def page_index(self) -> int: ...

  @property
  def image(self) -> Image: ...