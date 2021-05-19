# from unittest import TestCase
# import json

# from foundation.entity
# from foundation.geometry import BBox, Point
# from foundation.interfaces import *

# from foundation.typing_utils import unwrap


# class TestEntities(TestCase):

#   def test_text(self) -> None:
    
#     word_0: Word = Word('word-0', bbox=unwrap(BBox.spanning((Point(0, 0, 0), Point(5, 1, 0)))), text='hello')
#     text_0: Text = InMemoryText('text-0', (word_0,))
#     image_0: Image = InMemoryImage(text_0.bbox, 'path/to/image/0')
#     page_0: Page = InMemoryPage('page-0', image_0, (word_0, text_0))

#     record_0: RecordContext = InMemoryRecordContext(
#       {
#         e.id: e for e in [word_0, text_0, page_0]
#       },
#       (page_0.id,),
#       (text_0.id, page_0.id,)
#     )

#     print(record_0.as_dict())

#     # self.assertTrue(isinstance(w1, Word))
#     # w2 = Word('word-1', bbox=unwrap(BBox.spanning((Point(6, 0, 0), Point(11, 1, 0)))), text='world')

#     # words = (w1, w2)
#     # text = Text('text-id', children=words)

#     # text_bbox = unwrap(text.bbox)

#     # self.assertEqual(text_bbox.ix.a, 0)
#     # self.assertEqual(text_bbox.ix.b, 11)
#     # self.assertEqual(text_bbox.iy.a, 0)
#     # self.assertEqual(text_bbox.iy.b, 1)

#     # self.assertEqual(text_bbox.page_index, 0)
