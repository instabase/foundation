"""Spatial Text"""
from typing import List, Iterable, Union, Optional, Any

from .entity import Entity, Word, Whitespace

class SpatialText:
  words: List[Union[Word, Whitespace]]
  length: Optional[int]

  def __init__(self, words: List[Union[Word, Whitespace]]):
    self.words = words
    self.length = None
  
  def __len__(self) -> int:
    if self.length:
      return self.length
    length = sum([len(word) for word in self.words])
    self.length = sum([len(word) for word in self.words])
    return length

  def __bool__(self) -> bool:
    return len(self.words) != 0

  def __str__(self) -> str:
    return ''.join([word.text for word in self.words])

  def lstrip(self) -> None:
    # Removes whitespace from the left side
    i = 0
    while isinstance(self.words[i], Whitespace):
      i += 1
    
    self.words = self.words[i:]

  def rstrip(self) -> None:
    # Removes whitespace from right side
    i = len(self.words) - 1
    while isinstance(self.words[i], Whitespace):
      i -= 1
    
    self.words = self.words[:(i+1)]
  
  def strip(self) -> None:
    # Removes whitespace from both sides
    self.rstrip()
    self.lstrip()

  def _get_word_index(self, key: int) -> int:
    # Gets the index of the appropriate word given a character index
    amount_remaining = key
    i = 0
    while len(self.words[i]) <= amount_remaining:
        amount_remaining -= len(self.words[i])
        i += 1
    return i
  
  def __getitem__(self, key: Union[int, slice]) -> Any:
    # return self.__class__(self.words)

    if isinstance(key, int):
      # Gets the word at that character index
      i = self._get_word_index(key)
      return self.__class__([self.words[i]])
    elif isinstance(key, slice):
      i = 0
      j = len(self.words) - 1
      if key.start:
        i = self._get_word_index(key.start)
      if key.stop:
        j = self._get_word_index(key.stop-1)
      return self.__class__(self.words[i:j+1])

