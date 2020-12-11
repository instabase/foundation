from typing import Iterable
from unittest import TestCase

from foundation.entity import (
  OcrWordEntity, LineEntity, ParagraphEntity,
  TableCellEntity, TableRowEntity, TableEntity,
  TokenEntity, PhraseEntity, NumberEntity, IntegerEntity,
  DateEntity, TimeEntity, CurrencyEntity, NameEntity,
  AddressEntity, ClusterEntity
)
from foundation.geometry import BBox, Point
from foundation.ocr import InputWord
from foundation.protos.doc import entity_pb2
from foundation.protos.ocr import types_pb2


def _input_word(text: str, spanning: Iterable[Point]) -> InputWord:
  return InputWord(BBox.spanning(spanning), 'hello', None, None, None)


class TestOcrWordEntity(TestCase):

  def test_x_proto(self) -> None:
    input_word = _input_word('hello', (Point(0,0), Point(5, 1)))
    w = OcrWordEntity(input_word)
    pb = w.to_proto()

    assert w == OcrWordEntity.from_proto(pb)


class TestLineEntity(TestCase):

  def test_to_proto(self) -> None:
    w1 = OcrWordEntity(_input_word('hello', (Point(0,0), Point(5, 1))))
    w2 = OcrWordEntity(_input_word('world', (Point(6, 0), Point(11, 1))))

    line = LineEntity([w1, w2])
    pb = line.to_proto()

    assert line == LineEntity.from_proto(pb)

# TODO: Full test coverage. Let's finish stabilizing Entity types first.
