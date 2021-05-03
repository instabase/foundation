from unittest import TestCase
from typing import List, Union

from typing import Tuple, Union

from foundation.interfaces import Word, Whitespace, Text, Subword
from foundation.in_memory import InMemoryWord, InMemoryWhitespace, InMemoryText, InMemorySubword
from foundation.geometry import BBox, Point

from foundation.typing_utils import unwrap

class TestSubword(TestCase):

  bbox = unwrap(BBox.spanning((Point(0, 0, 0), Point(5, 1, 0))))

  w = InMemoryWord('word-1', bbox=bbox, text='hello')
  sw1 = InMemorySubword(text=w.text, start=1, end=4)
  sw2 = InMemorySubword(text=w.text, start=2, end=3)

  def test_constructor(self) -> None:
    spatial = InMemoryText('text-1', (self.w, self.sw1))
    self.assertEqual(str(spatial), 'helloell')

    spatial = InMemoryText('text-2', (self.w, self.sw2))
    self.assertEqual(str(spatial), 'hellol')

    spatial = InMemoryText('text-3', (self.w, self.sw1, self.sw2))
    self.assertEqual(str(spatial), 'helloelll')

  def test_len(self) -> None:
    spatial = InMemoryText('text-1', (self.sw1,))
    self.assertEqual(len(spatial), 3)

    spatial = InMemoryText('text-2', (self.sw2,))
    self.assertEqual(len(spatial), 1)

    spatial = InMemoryText('text-3', (self.sw1, self.sw2))
    self.assertEqual(len(spatial), 4)

class TestText(TestCase):

  bbox = unwrap(BBox.spanning((Point(0, 0, 0), Point(5, 1, 0))))

  w1: Word = InMemoryWord('word-0', bbox=bbox, text='hello')
  w2: Word = InMemoryWord('word-1', bbox=bbox, text='world')
  ws: Whitespace = InMemoryWhitespace(text='     ')

  def test_len(self) -> None:

    words: Tuple[Union[Word, Whitespace], ...] = (self.w1, self.ws, self.w2)

    spatial: Text = InMemoryText('text-0', words)
    self.assertEqual(len(spatial), len('hello     world'))

  def test_strip(self) -> None:

    words: Tuple[Union[Word, Whitespace], ...] = (self.w1, self.ws, self.w2)

    spatial: Text = InMemoryText('text-1', words)
    spatial.lstrip()

    self.assertEqual(str(spatial), 'hello     world')

    words = (self.w1, self.w2, self.ws, self.ws)

    spatial = InMemoryText('text-2', words)
    spatial.rstrip()

    self.assertEqual(str(spatial), 'helloworld')

    words = (self.ws, self.ws, self.w1, self.w2, self.ws)

    spatial = InMemoryText('text-3', words)
    spatial.strip()

    self.assertEqual(str(spatial), 'helloworld')
  
  def test_slice(self) -> None:
    words: Tuple[Union[Word, Whitespace], ...] = (self.ws, self.w1, self.w2, self.ws)

    spatial: Text = InMemoryText('text-4', words) #'     helloworld'

    # Test slicing with ints
    # self.assertEqual(str(spatial[0]), ' ')
    # self.assertEqual(str(spatial[4]), ' ')
    # self.assertEqual(str(spatial[5]), 'h')
    # self.assertEqual(str(spatial[9]), 'o')
    # self.assertEqual(str(spatial[10]), 'w')

    # # Test with slices
    # self.assertEqual(str(spatial[0:4]), '    ')
    # self.assertEqual(str(spatial[0:10]), '     hello')
    self.assertEqual(str(spatial[0:11]), '     hellow')
    # self.assertEqual(str(spatial[4:11]), ' hellow')
    # self.assertEqual(str(spatial[8:11]), 'low')

    # Test strip after slice
    new_spatial = spatial[3:17]
    new_spatial.strip()
    self.assertEqual(str(new_spatial), 'helloworld')
