"""Spatial Text"""
from typing import List, Iterable, Union, Optional, Any, Tuple

from .entity import Entity, Word, Whitespace, Subword

class Text:
  words: List[Union[Word, Whitespace, Subword]]
  length: Optional[int]

  def __init__(self, words: List[Union[Word, Whitespace, Subword]]):
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
  
  def debug_string(self) -> str:
    output = "["
    for word in self.words:
      if isinstance(word, Whitespace):
        output += f'Whitespace: {word.text}, '
      elif isinstance(word, Subword):
        output += f'Subword: {word.text}, '
      elif isinstance(word, Word):
        output += f'Word: {word.text}, '
    return output + ']'

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

  def _get_word_index(self, key: int) -> Tuple[int, int]:
    # Gets the index of the appropriate word given a character index
    amount_remaining = key
    i = 0
    while len(self.words[i]) <= amount_remaining:
        amount_remaining -= len(self.words[i])
        i += 1
    return i, amount_remaining
  
  def __getitem__(self, key: Union[int, slice]) -> Any:

    if isinstance(key, int):
      # Gets a single character from the Text
      i, ar = self._get_word_index(key)
      word = self.words[i]
      subword = Subword('TODO', bbox = word.bbox, text=word.text, start=ar, end=ar+1)
      return self.__class__([subword])
    elif isinstance(key, slice):
      # Gets a substring from the Text
      i, ar1, ar2 = 0, 0, 0
      j = len(self.words) - 1
      if key.start:
        i, ar1 = self._get_word_index(key.start)
      if key.stop:
        j, ar2 = self._get_word_index(key.stop-1)
      
      if i == j:
        # Getting a single word or subword
        word = self.words[i]
        if isinstance(word, Whitespace):
          text = ' ' * (ar2 - ar1 + 1)
          whitespace = Whitespace('TODO', bbox=word.bbox, text=text)
          return self.__class__([whitespace])
        subword = Subword('TODO', bbox = word.bbox, text=word.text, start=ar1, end=ar2+1)
        return self.__class__([subword])
      else:
        # Getting multiple words and/or subwords
        first_word, last_word = self.words[i], self.words[j]
        if ar1 > 0:
          if isinstance(first_word, Whitespace):
            text = ' ' * (len(first_word) - ar1)
            first_word = Whitespace('TODO', bbox=first_word.bbox, text=text)
          else:
            first_word = Subword('TODO', bbox=first_word.bbox, text=first_word.text, start=ar1, end=len(first_word.text))
        if ar2 < len(last_word)-1:
          if isinstance(last_word, Whitespace):
            text = ' ' * ar2
            last_word = Whitespace('TODO', bbox=last_word.bbox, text=text)
          else:
            last_word = Subword('TODO', bbox=last_word.bbox, text=last_word.text, start=0, end=ar2+1)
        
        new_list = [first_word]
        if j - i > 1:
          new_list.extend(self.words[i+1:j])
        
        new_list.append(last_word)
        return self.__class__(new_list)


