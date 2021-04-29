from typing import Tuple, cast, Dict, Iterable, Any, Union

import attr
from .geometry import BBox
from .interfaces import Page, RecordContext, Word, Image, Entity, Text, Whitespace

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

  def as_dict(self) -> Dict[str, Any]:
    return {
      'id': self._id,
      'bbox': self.bbox.as_dict(),
      'text': self._text,
    }

@attr.s(auto_attribs=True)
class InMemoryWhitespace(Whitespace):
  _text: str

  @property
  def type(self) -> str:
    return "Whitespace"

  @property
  def text(self) -> str:
    return self._text

@attr.s(auto_attribs=True)
class InMemoryText(Text):
  _id: str
  _children: Tuple[Union[Word, Whitespace], ...]

  @property
  def type(self) -> str:
    return "Text"
  
  @property
  def id(self) -> str:
    return self._id

  def get_children(self) -> Iterable[Word]:
    yield from (c for c in self._children if isinstance(c, Word))

  def __str__(self) -> str:
    return ''.join([word.text for word in self._children])

  def _get_word_index(self, key: int) -> int:
    # Gets the index of the appropriate word given a character index
    amount_remaining = key
    i = 0
    while len(self._children[i]) <= amount_remaining:
        amount_remaining -= len(self._children[i])
        i += 1
    return i

  def __getitem__(self, key: Union[int, slice, Tuple[slice, slice]]) -> 'InMemoryText':
    if isinstance(key, int):
      # Gets the word at that character index
      i = self._get_word_index(key)
      return self.__class__('TODO', (self._children[i],))
    elif isinstance(key, slice):
      i = 0
      j = len(self._children) - 1
      if key.start:
        i = self._get_word_index(key.start)
      if key.stop:
        j = self._get_word_index(key.stop-1)
      return self.__class__('TODO', tuple(self._children[i:j+1]))
    elif isinstance(key, tuple):
      raise NotImplementedError
    else:
      raise ValueError('Invalid key argument')
  
  def lstrip(self) -> 'InMemoryText':
    # Removes whitespace from the left side
    i = 0
    for c in self._children:
      if not c.type == "Whitespace":
        break
      i += 1
    
    self._children = self._children[i:]
    return self

  def rstrip(self) -> 'InMemoryText':
    # Removes whitespace from right side
    i = len(self._children) - 1
    while self._children[i].type == "Whitespace" and i >= 0:
      i -= 1
    
    self._children = self._children[:(i+1)]
    return self

  def __len__(self) -> int:
    return sum(len(c) for c in self._children)

@attr.s(auto_attribs=True)
class InMemoryImage(Image):
  _bbox: BBox
  _input_filepath: str

  @property
  def type(self) -> str:
    return "Image"

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

@attr.s(auto_attribs=True)
class InMemoryRecordContext(RecordContext):
  _entities: Dict[str, Entity] # maps all entity IDs to entities
  _pages: Tuple[str, ...] # list of page IDs
  _collections: Tuple[str, ...] # list of collection IDs

  @property
  def type(self) -> str:
    return "RecordContext"

  def get_entities(self) -> Iterable[Entity]:
    yield from self._entities.values()

  def get_pages(self) -> Iterable[Page]:
    for id in self._pages:
      yield cast(Page, self._entities[id])

  def get_collection_entities(self) -> Iterable[Entity]:
    for id in self._collections:
      yield self._entities[id]

  # def as_dict(self) -> Dict:
  #   rtn = {
  #     'entities': {
  #       id: entity.as_dict() for id, entity in self._entities.items()
  #     },
  #     'pages': list(self._pages),
  #     'collections': list(self._collections),
  #   }
  #   return rtn

  # @staticmethod
  # def from_dict(record_dict: Dict) -> 'InMemoryRecordContext':
  #   return InMemoryRecordContext({}, ('h',), ('h',))