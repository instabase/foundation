from typing import FrozenSet, Sequence, Tuple, Iterable, Optional

from abc import abstractmethod

from .geometry import BBox, Interval
from .meta import FoundationType, foundation_types

class Entity(metaclass=FoundationType):
  id: str
  
  @property
  def type(self) -> str:
    return self.__class__.__name__

  def __repr__(self) -> str:
    return "default repr"
  
  @property
  def bbox(self) -> Optional[BBox]:
    return BBox.union(self.get_bboxes())

  def get_bboxes(self) -> Iterable[BBox]:
    yield from (c.bbox for c in self.get_children() if c.bbox is not None)

  @property
  def children_ids(self) -> FrozenSet[str]:
    return frozenset(c.id for c in self.get_children())

  # get_children is now a function instead of a property to handle
  # the case where:
  #
  # t = Text(...)
  # word1 = next(t.children) <- this would be the first child
  # word2 = next(t.children) <- this would be also be the first child
  @abstractmethod
  def get_children(self) -> Iterable['Entity']: ...

class Word(Entity):
  _bbox: BBox
  text: str

  def __init__(self, id: str, *, text: str, bbox: BBox):
    self.id = id
    self.text = text
    self._bbox = bbox

  @property
  def bbox(self) -> BBox:
    return self._bbox

  @property
  def char_width(self) -> float:
    return self.bbox.width / float(len(self.text))

  def get_children(self) -> Iterable[Entity]:
    yield from ()

class Text(Entity):
  _children: Tuple[Word, ...]

  def __init__(self, id: str, *, children: Sequence[Word]):
    self.id = id
    self._children = tuple(children)

  def get_children(self) -> Iterable[Word]:
    yield from self._children

class Image:
  input_filepath: str
  bbox: BBox

  def __init__(self, *, input_filepath: str, bbox: BBox):
    self.input_filepath = input_filepath
    self.bbox = bbox

class Page(Entity):
  _children: FrozenSet[Word]
  index: int
  image: Image
  
  def __init__(self, id: str, *, index: int, children: Iterable[Word], image: Image):
    self.id = id
    self.index = index
    self._children = frozenset(children)
    self.image = image

  def get_children(self) -> Iterable[Word]:
    yield from self._children