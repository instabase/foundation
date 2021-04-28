from abc import abstractmethod
from typing import FrozenSet, Iterable, Optional, Sequence, Set, Tuple, Dict

from .geometry import BBox
from .meta import FoundationType

class Entity(FoundationType):
  id: str
  
  @property
  def type(self) -> str:
    return self.__class__.__name__

  def __repr__(self) -> str:
    classes = type.mro(self.__class__)[:-1][::-1]
    attributes = [k for c in classes for k in c.__annotations__]
    attr_vals = [getattr(self, k) for k in attributes]
    str_vals = [f"\"{v}\"" if isinstance(v, str) else str(v) for v in attr_vals]
    vals = [f"{k}={v}" for k, v in zip(attributes, str_vals)]
    attr_str = ", ".join(vals)
    return f"{self.type}({attr_str})"
  
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
    yield from []

  def __len__(self) -> int:
    return len(self.text)

class Whitespace(Word):

  def __init__(self, id: str, *, text: str, bbox: BBox):
    super().__init__(id, bbox=bbox, text=text)
  
  def is_valid(self) -> bool:
    return self.text.isspace()

class Text(Entity):
  _children: Tuple[Word, ...]

  def __init__(self, id: str, *, children: Sequence[Word]):
    self.id = id
    self._children = tuple(children)

  def get_children(self) -> Iterable[Word]:
    yield from self._children

class Image(FoundationType):
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
