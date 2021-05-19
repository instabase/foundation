# from unittest import TestCase
# from typing import List, Union

# from typing import Tuple, Union

# from foundation.interfaces import Word, Whitespace, Text, Subword
# from foundation.in_memory import InMemoryWord, InMemoryWhitespace, \
#   InMemoryText, InMemorySubword, InMemorySpatialText
# from foundation.geometry import BBox, Point

# from foundation.typing_utils import unwrap

# class TestInMemorySpatialText(TestCase):
  
#   bbox = unwrap(BBox.spanning((Point(0, 0, 0), Point(5, 1, 0))))

#   w1: Word = InMemoryWord('word-0', bbox=bbox, text='hello')
#   w2: Word = InMemoryWord('word-1', bbox=bbox, text='world')
#   ws: Whitespace = InMemoryWhitespace(text='  ')

#   line1 = InMemoryText('text-1', (w1, w2))
#   line2 = InMemoryText('text-2', (w2, w1))
#   line3 = InMemoryText('text-3', (ws, w1))
#   line4 = InMemoryText('text-4', (w2, ws, w1))

#   def test_2d_splice(self) -> None:
#     spatial = InMemorySpatialText('spatial-1', [self.line1, self.line2, self.line3])
#     new_spatial = spatial[1:5, 1:3]
#     self.assertEqual(str(new_spatial), 'orld\n hel')

#     new_spatial = spatial[0:3, 0:3]
#     self.assertEqual(str(new_spatial), 'hel\nwor\n  h')

#     new_spatial = spatial[4:7, 0:3]
#     self.assertEqual(str(new_spatial), 'owo\ndhe\nllo')

#     # Type check
#     self.assertEqual(new_spatial.type, 'SpatialText')
  
#   def test_1d_splice(self) -> None:
#     spatial = InMemorySpatialText('spatial-1', [self.line1, self.line2, self.line3])
    
#     self.assertEqual(str(spatial[1]), 'e')
#     self.assertEqual(str(spatial[12]), 'o')
#     self.assertEqual(str(spatial[1:10]), 'elloworld')
#     self.assertEqual(str(spatial[1:11]), 'elloworld\n')
#     self.assertEqual(str(spatial[5:14]), 'world\nwor')
#     self.assertEqual(str(spatial[6:26]), 'orld\nworldhello\n  he')

#     # Type check
#     self.assertEqual(spatial[1:2].type, 'Text')


#   def test_len(self) -> None:
#     spatial = InMemorySpatialText('spatial-0', [self.line1, self.line2])
#     self.assertEqual(len(spatial), 21)

#     spatial = InMemorySpatialText('spatial-1', [self.line1, self.line2, self.line3])
#     self.assertEqual(len(spatial), 29)

#     spatial = InMemorySpatialText('spatial-2', [self.line4])
#     self.assertEqual(len(spatial), 12)

  
#   def test_str(self) -> None:
#     spatial = InMemorySpatialText('spatial-0', [self.line1, self.line2])
#     self.assertEqual(str(spatial), 'helloworld\nworldhello')

#     spatial = InMemorySpatialText('spatial-1', [self.line1, self.line2, self.line3])
#     self.assertEqual(str(spatial), 'helloworld\nworldhello\n  hello')

#     spatial = InMemorySpatialText('spatial-2', [self.line4])
#     self.assertEqual(str(spatial), 'world  hello')

# class TestSubword(TestCase):

#   bbox = unwrap(BBox.spanning((Point(0, 0, 0), Point(5, 1, 0))))

#   w = InMemoryWord('word-1', bbox=bbox, text='hello')
#   sw1 = InMemorySubword(text=w.text, start=1, end=4)
#   sw2 = InMemorySubword(text=w.text, start=2, end=3)

#   def test_constructor(self) -> None:
#     text = InMemoryText('text-1', (self.w, self.sw1))
#     self.assertEqual(str(text), 'helloell')

#     text = InMemoryText('text-2', (self.w, self.sw2))
#     self.assertEqual(str(text), 'hellol')

#     text = InMemoryText('text-3', (self.w, self.sw1, self.sw2))
#     self.assertEqual(str(text), 'helloelll')

#   def test_len(self) -> None:
#     text = InMemoryText('text-1', (self.sw1,))
#     self.assertEqual(len(text), 3)

#     text = InMemoryText('text-2', (self.sw2,))
#     self.assertEqual(len(text), 1)

#     text = InMemoryText('text-3', (self.sw1, self.sw2))
#     self.assertEqual(len(text), 4)

# class TestText(TestCase):

#   bbox = unwrap(BBox.spanning((Point(0, 0, 0), Point(5, 1, 0))))

#   w1: Word = InMemoryWord('word-0', bbox=bbox, text='hello')
#   w2: Word = InMemoryWord('word-1', bbox=bbox, text='world')
#   ws: Whitespace = InMemoryWhitespace(text='     ')

#   def test_len(self) -> None:

#     words: Tuple[Union[Word, Whitespace], ...] = (self.w1, self.ws, self.w2)

#     text: Text = InMemoryText('text-0', words)
#     self.assertEqual(len(text), len('hello     world'))

#   def test_strip(self) -> None:

#     words: Tuple[Union[Word, Whitespace], ...] = (self.w1, self.ws, self.w2)

#     text: Text = InMemoryText('text-1', words)
#     text.lstrip()

#     self.assertEqual(str(text), 'hello     world')

#     words = (self.w1, self.w2, self.ws, self.ws)

#     text = InMemoryText('text-2', words)
#     text.rstrip()

#     self.assertEqual(str(text), 'helloworld')

#     words = (self.ws, self.ws, self.w1, self.w2, self.ws)

#     text = InMemoryText('text-3', words)
#     text.strip()

#     self.assertEqual(str(text), 'helloworld')
  
#   def test_slice(self) -> None:
#     words: Tuple[Union[Word, Whitespace], ...] = (self.ws, self.w1, self.w2, self.ws)

#     text: Text = InMemoryText('text-4', words) #'     helloworld'

#     # Test slicing with ints
#     self.assertEqual(str(text[0]), ' ')
#     self.assertEqual(str(text[4]), ' ')
#     self.assertEqual(str(text[5]), 'h')
#     self.assertEqual(str(text[9]), 'o')
#     self.assertEqual(str(text[10]), 'w')

#     # Test with slices
#     self.assertEqual(str(text[0:4]), '    ')
#     self.assertEqual(str(text[0:10]), '     hello')
#     self.assertEqual(str(text[0:11]), '     hellow')
#     self.assertEqual(str(text[4:11]), ' hellow')
#     self.assertEqual(str(text[8:11]), 'low')

#     # Test strip after slice
#     new_text = text[3:17]
#     new_text.strip()
#     self.assertEqual(str(new_text), 'helloworld')
