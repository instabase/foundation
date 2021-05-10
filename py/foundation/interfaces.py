from abc import abstractmethod
from typing import Any, Dict, Optional, Iterable, Union, Tuple

from itertools import chain

from .meta import FoundationType
from .geometry import BBox

class Entity(FoundationType):
  @property
  @abstractmethod
  def id(self) -> str: ...
  
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

class Whitespace(FoundationType):
  @property
  @abstractmethod
  def text(self) -> str: ...

  def __str__(self) -> str:
    return self.text

  def __len__(self) -> int:
    return len(self.text)

class Subword(Word):

  @property
  def start(self) -> int: ...

  @property
  def end(self) -> int: ...

class Text(Entity):
  @abstractmethod
  def get_children(self) -> Iterable[Word]: ...

  @abstractmethod
  def __len__(self) -> int: ...

  def __bool__(self) -> bool:
    return len(self) != 0

  @abstractmethod
  def __str__(self) -> str: ...

  @abstractmethod
  def lstrip(self) -> 'Text':
    """
    Removes whitespace from the left side
    """
    ...

  @abstractmethod
  def rstrip(self) -> 'Text':
    """
    Removes whitespace from right side
    """
    ...
  
  def strip(self) -> 'Text':
    """
    Removes whitespace from both sides
    """
    return self.rstrip().lstrip()

  @abstractmethod
  def __getitem__(self, key: Union[int, slice, Tuple[slice, slice]]) -> Any:
    ...

class SpatialText(Entity):
  @abstractmethod
  def get_children(self) -> Iterable[Word]: ...

  @abstractmethod
  def __len__(self) -> int: ...

  def __bool__(self) -> bool:
    return len(self) != 0

  @abstractmethod
  def __str__(self) -> str: ...

  @abstractmethod
  def __getitem__(self, key: Union[int, slice, Tuple[slice, slice]]) -> Any:
    ...

class Image(FoundationType):
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

class Date(Text):
  @property
  @abstractmethod
  def year(self) -> Optional[int]: ...

  @property
  @abstractmethod
  def month(self) -> Optional[int]: ...

  @property
  @abstractmethod
  def day(self) -> Optional[int]: ...

  @property
  def is_complete(self) -> bool:
    """
    Returns true if the date contains all date elements (year, month, and day)
    """
    return all(
      i is not None 
      for i in [self.year, self.month, self.day]
    )

  @property
  @abstractmethod
  def likeness_score(self) -> float: ...

class CurrencyAmount(Text):
  @property
  @abstractmethod
  def likeness_score(self) -> float: ...

class PersonName(Text):
  @property
  @abstractmethod
  def likeness_score(self) -> float: ...

class Address(Text):
  @property
  @abstractmethod
  def likeness_score(self) -> float: ...

class RecordContext(FoundationType):
  @abstractmethod
  def get_entities(self) -> Iterable[Entity]: 
    """
    Returns all entities associated with this record (including Words)
    """
    ...

  @abstractmethod
  def get_pages(self) -> Iterable[Page]: 
    """
    Returns the page entities associated with this record in order
    """
    ...

  @abstractmethod
  def get_collection_entities(self) -> Iterable[Entity]:
    """
    Returns the non-word entities associated with this Record
    """
    ...

  def as_dict(self) -> Dict[str, Any]:
    """
    Serializes this RecordContext to JSON
    """
    return {
      'entities': {
        e.id: e.as_dict() for e in self.get_entities()
      },
      'pages': [p.id for p in self.get_pages()],
      'collections': [c.id for c in self.get_collection_entities()]
    }

  # @staticmethod
  # @abstractmethod
  # def from_dict(record_dict: Dict) -> 'RecordContext':
  #   ...
