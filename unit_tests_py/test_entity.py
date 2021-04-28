from unittest import TestCase
import json

from foundation.in_memory import InMemoryWord
from foundation.geometry import BBox, Point
from foundation.interfaces import Word

from foundation.typing_utils import unwrap


class TestEntities(TestCase):

  def test_text(self) -> None:

    w1: Word = InMemoryWord('word-0', bbox=unwrap(BBox.spanning((Point(0, 0, 0), Point(5, 1, 0)))), text='hello')
    print(w1.text)
    # self.assertTrue(isinstance(w1, Word))
    # w2 = Word('word-1', bbox=unwrap(BBox.spanning((Point(6, 0, 0), Point(11, 1, 0)))), text='world')

    # words = (w1, w2)
    # text = Text('text-id', children=words)

    # text_bbox = unwrap(text.bbox)

    # self.assertEqual(text_bbox.ix.a, 0)
    # self.assertEqual(text_bbox.ix.b, 11)
    # self.assertEqual(text_bbox.iy.a, 0)
    # self.assertEqual(text_bbox.iy.b, 1)

    # self.assertEqual(text_bbox.page_index, 0)
