from unittest import TestCase

from typing import Tuple, Union

from foundation.interfaces import Word, Whitespace, Text
from foundation.in_memory import InMemoryWord, InMemoryWhitespace, InMemoryText
from foundation.geometry import BBox, Point

from foundation.typing_utils import unwrap


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
    words: Tuple[Union[Word, Whitespace], ...] = (self.ws, self.w1, self.w2)

    spatial: Text = InMemoryText('text-4', words) #'     helloworld'

    # Test slicing with ints
    self.assertEqual(str(spatial[0]), '     ')
    self.assertEqual(str(spatial[4]), '     ')
    self.assertEqual(str(spatial[5]), 'hello')
    self.assertEqual(str(spatial[9]), 'hello')
    self.assertEqual(str(spatial[10]), 'world')

    # Test with slices
    self.assertEqual(str(spatial[0:4]), '     ')
    self.assertEqual(str(spatial[0:10]), '     hello')
    self.assertEqual(str(spatial[0:11]), '     helloworld')
    self.assertEqual(str(spatial[4:11]), '     helloworld')
    self.assertEqual(str(spatial[8:11]), 'helloworld')
