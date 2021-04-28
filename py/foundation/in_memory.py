from dataclasses import dataclass
from .interfaces import *

class InMemoryWord(Word):
  _id: str
  _bbox: BBox
  _text: str
  _type: str = "Word"

  def __init__(self, id: str, bbox: BBox, text: str):
    self._id = id
    self._bbox = bbox
    self._text = text

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