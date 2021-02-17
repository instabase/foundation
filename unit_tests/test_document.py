from unittest import TestCase

from foundation.document import Document
from foundation.entity import Word, Page, Phrase
from foundation.geometry import BBox, Point

from foundation.typing_utils import unwrap


class TestDoc(TestCase):

  def test_bbox(self) -> None:
    w1 = Word(unwrap(BBox.spanning((Point(0, 0), Point(5, 1)))), 'hello')
    w2 = Word(unwrap(BBox.spanning((Point(6, 0), Point(11, 1)))), 'world')
    p1 = Page(unwrap(BBox.spanning((Point(0, 0), Point(11, 1)))), 1)

    words = (w1, w2)
    doc = Document.from_entities(words)

    assert doc.bbox == unwrap(BBox.union(w.bbox for w in words))
    assert doc.bbox == p1.bbox

    doc = doc.with_entities((p1,))
    assert doc.bbox == p1.bbox

  def test_constructwith(self) -> None:
    w1 = Word(unwrap(BBox.spanning((Point(0, 0), Point(5, 1)))), 'hello')
    w2 = Word(unwrap(BBox.spanning((Point(6, 0), Point(11, 1)))), 'world')

    words = (w1, w2)
    doc_words = Document.from_entities(words)

    phrase = Phrase.from_words(words)
    doc = doc_words.with_entities((phrase,))

    assert set(doc.entities) == set((w1, w2, phrase))

  def filter_entities(self) -> None:
    w1 = Word(unwrap(BBox.spanning((Point(0, 0), Point(5, 1)))), 'hello')
    w2 = Word(unwrap(BBox.spanning((Point(6, 0), Point(11, 1)))), 'world')

    p1 = Page(unwrap(BBox.spanning((Point(0, 0), Point(11, 1)))), 1)

    doc = Document.from_entities((w1, w2, p1))

    assert set(doc.filter_entities(Page)) == set((p1,))
    assert set(doc.filter_entities(Word)) == set((w1, w2))
