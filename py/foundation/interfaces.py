from abc import ABC, abstractmethod

from typing import Dict, Generic, Optional, Iterable, TypeVar, Any
from typing_extensions import Protocol

from .geometry import BBox
from .descriptors import FoundationAttribute

class Entity(Protocol):
  id: FoundationAttribute[str]
  bbox: FoundationAttribute[BBox]
  type: FoundationAttribute[str]
  def get_bboxes(self) -> Iterable[BBox]: ...
  def get_children(self) -> Iterable['Entity']: ...

class Word(Entity):
  text: FoundationAttribute[str]

  @property
  def char_width(self) -> float:
    return self.bbox.width/len(self)

  def __len__(self) -> int:
    return len(self.text)

class Text(Entity):
  def __len__(self) -> int: ...

class Image(Protocol):
  bbox: BBox
  input_filepath: str

class Page(Entity):
  page_index: int
  image: Image
