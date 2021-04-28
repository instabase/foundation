from dataclasses import dataclass
from .interfaces import *
from .descriptors import *

class InMemoryWord(Word):
  id: DataDescriptor[str] = DataDescriptor[str]()
  bbox: DataDescriptor[BBox] = DataDescriptor[BBox]()
  text: DataDescriptor[str] = DataDescriptor[str]()
  def __init__(self, id: str, bbox: BBox, text: str):
    self.id = id
    self.bbox = bbox
    self.text = text
    self.type = "Word"
  
  def get_bboxes(self) -> Iterable[BBox]:
    yield from []

  def get_children(self) -> Iterable[Entity]:
    yield from []