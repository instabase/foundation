from unittest import TestCase
import json

from foundation.document import Document
from foundation.entity import Word, Page, Phrase, Address, dump_to_json, load_entity_from_json
from foundation.geometry import BBox, Point

from foundation.typing_utils import unwrap


class TestEntities(TestCase):

  def test_address(self) -> None:

    w1 = Word(unwrap(BBox.spanning((Point(0, 0), Point(5, 1)))), 'hello', None)
    w2 = Word(unwrap(BBox.spanning((Point(6, 0), Point(11, 1)))), 'world', None)

    words = (w1, w2)
    phrases = tuple([Phrase.from_words(words)])
    bbox = unwrap(BBox.union(e.bbox for e in words))

    entity = Address(
      bbox=bbox,
      text='some address',
      lines=phrases,
      address_parts=(('street', '123 main street'), ('zip', '02116')),
      likeness_score=0.98
    )

    json_str = dump_to_json(entity)
    recreation = load_entity_from_json(json.loads(json_str))
    self.assertEqual(recreation, entity)