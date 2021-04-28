from unittest import TestCase

from foundation.entity import Word, Whitespace
from foundation.geometry import BBox, Point
from foundation.spatial_text import SpatialText

from foundation.typing_utils import unwrap


class TestSpatialText(TestCase):

  bbox = unwrap(BBox.spanning((Point(0, 0, 0), Point(5, 1, 0))))

  w1 = Word('word-0', bbox=bbox, text='hello')
  w2 = Word('word-1', bbox=bbox, text='world')
  ws = Whitespace('whitespace-1', bbox=bbox, text='     ')

  def test_len(self) -> None:

    words = [self.w1, self.ws, self.w2]

    spatial = SpatialText(words)
    self.assertEqual(len(spatial), len('hello     world'))

  def test_strip(self) -> None:

    words = [self.ws, self.ws, self.w1, self.w2]

    spatial = SpatialText(words)
    spatial.lstrip()

    self.assertEqual(str(spatial), 'helloworld')

    words = [self.w1, self.w2, self.ws, self.ws]

    spatial = SpatialText(words)
    spatial.rstrip()

    self.assertEqual(str(spatial), 'helloworld')

    words = [self.ws, self.ws, self.w1, self.w2, self.ws]

    spatial = SpatialText(words)
    spatial.strip()

    self.assertEqual(str(spatial), 'helloworld')
  
  def test_slice(self) -> None:
    words = [self.ws, self.w1, self.w2]

    spatial = SpatialText(words) #'     helloworld'

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
