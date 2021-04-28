from typing import Tuple

import attr
from .interfaces import *

@attr.s(auto_attribs=True)
class InMemoryWord(Word):
  _id: str
  _bbox: BBox
  _text: str

  @property
  def type(self) -> str:
    return "Word"

  @property
  def id(self) -> str:
    return self._id

  @property
  def bbox(self) -> BBox:
    return self._bbox

  @property
  def text(self) -> str:
    return self._text
  
  def get_bboxes(self) -> Iterable[BBox]:
    yield from [self.bbox]

  def get_children(self) -> Iterable[Entity]:
    yield from []

@attr.s(auto_attribs=True)
class InMemoryText(Text):
  _id: str
  _children: Tuple[Word, ...]

  @property
  def type(self) -> str:
    return "Text"
  
  @property
  def id(self) -> str:
    return self._id

  def get_children(self) -> Iterable[Word]:
    yield from self._children

@attr.s(auto_attribs=True)
class InMemoryImage(Image):
  _bbox: BBox
  _input_filepath: str

  @property
  def bbox(self) -> BBox:
    return self._bbox

  @property
  def input_filepath(self) -> str:
    return self._input_filepath

@attr.s(auto_attribs=True)
class InMemoryPage(Page):
  _id: str
  _image: Image
  _children: Tuple[Entity, ...]

  @property
  def type(self) -> str:
    return "Page"

  @property
  def id(self) -> str:
    return self._id

  @property
  def image(self) -> Image:
    return self._image

  @property
  def bbox(self) -> BBox:
    return self._image.bbox

  @property
  def page_index(self) -> int:
    return self.bbox.page_index

  def get_children(self) -> Iterable[Entity]:
    yield from self._children