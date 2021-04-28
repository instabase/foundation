from typing import TypeVar, Generic, Any, Optional
from abc import ABC, abstractmethod
T = TypeVar('T')

class FoundationAttribute(ABC, Generic[T]):
  @abstractmethod
  def __get__(self, obj: Any, obj_type: Any = None) -> T: ...
  @abstractmethod
  def __set__(self, obj: Any, value: T) -> None: ...

class DataDescriptor(FoundationAttribute[T]):
  val: Optional[T]
  def __init__(self, val: T = None):
    self.val = val

  def __get__(self, obj: Any, obj_type: Any = None) -> T:
    if self.val is None:
      raise AttributeError
    return self.val
    
  def __set__(self, obj: Any, value: T) -> None:
    self.val = value