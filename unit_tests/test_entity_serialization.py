from itertools import chain
from typing import Iterable
from unittest import TestCase

from foundation.entity import (Word, Line, Paragraph, TableCell, TableRow,
                               Table, Number, Integer, Date, Time, Currency,
                               PersonName, Address, Cluster)
from foundation.geometry import BBox, Point
from foundation.ocr import InputWord
from foundation.protos.doc import entity_pb2
from foundation.protos.ocr import types_pb2
from foundation.typing_utils import unwrap


class TestWord(TestCase):

  def test_to_proto(self) -> None:
    bbox = unwrap(BBox.spanning((Point(0, 0), Point(5, 1))))
    w = Word('hello', bbox)
    pb = w.to_proto()

    assert w == Word.from_proto(pb)


class TestLine(TestCase):

  def test_to_proto(self) -> None:
    w1 = Word('hello', unwrap(BBox.spanning((Point(0, 0), Point(5, 1)))))
    w2 = Word('world', unwrap(BBox.spanning((Point(6, 0), Point(11, 1)))))

    words = [w1, w2]
    line = Line(words, BBox.union(w.bbox for w in words))

    pb = line.to_proto()
    assert line == Line.from_proto(pb)


# TODO: Full test coverage. Let's finish stabilizing Entity types first.
