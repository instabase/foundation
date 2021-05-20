from unittest import TestCase
import json

from foundation import Word, Text, Page, RecordContext, BBox, Point, entity_pb2, geometry_pb2

class TestEntities(TestCase):

  def test_text(self) -> None:
    record = RecordContext.build()
    
    word_0: Word = Word(entity_pb2.Entity(id='word-0', word=entity_pb2.Word(bbox=None, text='hello')), record._reference_map)
    # text_0: Text = Text.build('text-0', (word_0,))
    # page_0: Page = Page.build('page-0', (word_0, text_0))

    # record_0: RecordContext = RecordContext(
    #   {
    #     e.id: e for e in [word_0, text_0, page_0]
    #   },
    #   (page_0.id,),
    #   (text_0.id, page_0.id,)
    # )

    # print(record_0.as_dict())

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
