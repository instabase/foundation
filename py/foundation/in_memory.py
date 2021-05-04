from typing import Tuple, cast, Dict, Iterable, Any, Union, List
import uuid

import attr
from .geometry import BBox
from .interfaces import Page, RecordContext, Word, \
  Image, Entity, Text, Whitespace, Subword, SpatialText


@attr.s(auto_attribs=True)
class EntityReference(Entity):
  _id: str
  @property
  def id(self) -> str:
    return self._id

  def get_children(self) -> Iterable[Entity]:
    raise ValueError('Entity was not de-referenced')

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

  @staticmethod
  def from_dict(d: Dict[str, Any]) -> 'InMemoryWord':
    ...
    # return InMemoryWord(
    #   d['id'],
    #   BBox.from_dict(d['bbox']),
    #   d['text']
    # )

@attr.s(auto_attribs=True)
class InMemoryWhitespace(Whitespace):
  _text: str

  @property
  def type(self) -> str:
    return "Whitespace"

  @property
  def text(self) -> str:
    return self._text

  @staticmethod
  def from_dict(d: Dict[str, Any]) -> 'InMemoryWhitespace':
    ...

@attr.s(auto_attribs=True)
class InMemorySubword(Subword):
  _text: str
  _start: int
  _end: int

  @property
  def type(self) -> str:
    return "Subword"
  
  def id(self) -> str:
    return super().id
  
  @property
  def text(self) -> str:
    return self._text[self._start:self._end]

  @property
  def start(self) -> int:
    return self._start

  @property
  def end(self) -> int:
    return self._end

  def __len__(self) -> int:
    return len(self.text)

  def __str__(self) -> str:
    return self.text

  def get_children(self) -> Iterable[Entity]:
    yield from []
  
  @staticmethod
  def from_dict(d: Dict[str, Any]) -> 'InMemorySubword':
    ...

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
  
  def _get_children_with_spaces(self) -> Iterable[Union[Word, Whitespace]]:
    yield from (c for c in self._children if isinstance(c, Word) or isinstance(c, Whitespace))

  def __str__(self) -> str:
    return ''.join([word.text for word in self._children])

  def _get_word_index(self, key: int) -> Tuple[int, int]:
    # Gets the index of the appropriate word given a character index
    amount_remaining = key
    i = 0
    while len(self._children[i]) <= amount_remaining:
        amount_remaining -= len(self._children[i])
        i += 1
    return i, amount_remaining

  def __getitem__(self, key: Union[int, slice, Tuple[slice, slice]]) -> 'InMemoryText':
    if isinstance(key, int):
      # Gets a single character from the Text
      i, ar = self._get_word_index(key)
      word = self._children[i]
      subword = InMemorySubword(text=word.text, start=ar, end=ar+1)
      return self.__class__(str(uuid.uuid4()), (subword,))
    elif isinstance(key, slice):
      # Gets a substring from the Text
      i, ar1, ar2 = 0, 0, 0
      j = len(self._children) - 1
      if key.start:
        i, ar1 = self._get_word_index(key.start)
      if key.stop:
        j, ar2 = self._get_word_index(key.stop-1)
      
      if i == j:
        # Getting a single word or subword
        word = self._children[i]
        if word.type == 'Whitespace':
          text = ' ' * (ar2 - ar1 + 1)
          whitespace = InMemoryWhitespace(text)
          return self.__class__(str(uuid.uuid4()), (whitespace, ))
        subword = InMemorySubword(text=word.text, start=ar1, end=ar2+1)
        return self.__class__(str(uuid.uuid4()), (subword,))
      else:
        # Getting multiple words and/or subwords
        first_word, last_word = self._children[i], self._children[j]
        if ar1 > 0:
          if first_word.type == 'Whitespace':
            text = ' ' * (len(first_word) - ar1)
            first_word = InMemoryWhitespace(text)
          else:
            first_word = InMemorySubword(text=first_word.text, start=ar1, end=len(first_word.text))
        if ar2 < len(last_word)-1:
          if last_word.type == 'Whitespace':
            text = ' ' * ar2
            last_word = InMemoryWhitespace(text=text)
          else:
            last_word = InMemorySubword(text=last_word.text, start=0, end=ar2+1)
        
        new_list = [first_word]
        if j - i > 1:
          new_list.extend(self._children[i+1:j])
        
        new_list.append(last_word)
        return self.__class__(str(uuid.uuid4()), tuple(new_list))
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

  def strip(self) -> 'InMemoryText':
    # Removes whitespace from both sides
    return self.rstrip().lstrip()

  def __len__(self) -> int:
    return sum(len(c) for c in self._children)

  @staticmethod
  def from_dict(d: Dict[str, Any]) -> 'InMemoryText':
    ...

@attr.s(auto_attribs=True)
class InMemorySpatialText(SpatialText):
  _id: str
  _lines: List[InMemoryText]

  @property
  def type(self) -> str:
    return "SpatialText"
  
  @property
  def id(self) -> str:
    return self._id

  def _get_in_memory_text(self) -> 'InMemoryText':
    # Gets a one dimensional InMemoryText
    full_list: List[Union[Word, Whitespace]] = list(self._lines[0]._get_children_with_spaces())
    for i in range(1, len(self._lines)):
      full_list.append(InMemoryWhitespace(text='\n'))
      full_list.extend(self._lines[i]._get_children_with_spaces())
    
    return InMemoryText(str(uuid.uuid4()), tuple(full_list))

  def get_children(self) -> Iterable[Word]:
    return self._get_in_memory_text().get_children()
  
  def __len__(self) -> int:
    # +1 accounts for new line at each line, -1 because no new line at the end
    return sum([len(line) + 1 for line in self._lines]) - 1

  def __str__(self) -> str:
    return '\n'.join([str(line) for line in self._lines])

  def __getitem__(self, key: Union[int, slice, Tuple[slice, slice]]) -> Any:
    if isinstance(key, int) or isinstance(key, slice):
      return self._get_in_memory_text()[key]
    elif isinstance(key, tuple):
      if len(key) > 2:
        raise ValueError('Too many slices')
      x_key, y_key = key
      new_lines = [line[x_key.start:x_key.stop] for line in self._lines[y_key.start:y_key.stop]]
      return self.__class__(str(uuid.uuid4()), new_lines)
    else:
      raise ValueError('Invalid key argument')

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

  @staticmethod
  def from_dict(d: Dict[str, Any]) -> 'InMemoryImage':
    ...

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

  @staticmethod
  def from_dict(d: Dict[str, Any]) -> 'InMemoryPage':
    ...

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

  def add_collection_entity(self, entity: Entity) -> None:
    self._entities[entity.id] = entity
    self._collections += (entity.id,)

  @staticmethod
  def from_dict(d: Dict[str, Any]) -> 'InMemoryRecordContext':
    ...

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
