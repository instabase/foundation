""" OCR types wrappers. """

from dataclasses import dataclass
from typing import Optional, List

from foundation.protos.ocr import types_pb2

from .geometry import BBox


@dataclass(frozen=True)
class CharConfidence:
  percentage: float
  unsure: Optional[bool]

  @staticmethod
  def from_proto(msg: types_pb2.CharConfidence) -> 'CharConfidence':
    unsure = None
    if msg.HasField('unsure'):
      unsure = msg.unsure
    return CharConfidence(msg.percentage, unsure)


@dataclass(frozen=True)
class WordConfidence:
  word_confidence: Optional[float]
  low_confidence: Optional[bool]
  char_confidences: Optional[List[CharConfidence]]

  @staticmethod
  def from_proto(msg: types_pb2.WordConfidence) -> 'WordConfidence':
    word_confidence = None
    if msg.HasField('word_confidence'):
      word_confidence = msg.word_confidence
    low_confidence = None
    if msg.HasField('low_confidence'):
      low_confidence = msg.low_confidence
    char_confidences = [
        CharConfidence.from_proto(c) for c in msg.char_confidences
    ]
    return WordConfidence(word_confidence, low_confidence, char_confidences)


@dataclass(frozen=True)
class InputWord:
  bounding_box: BBox
  text: Optional[str]
  confidence: Optional[WordConfidence]

  char_width: Optional[float]
  rotation_angle: Optional[float]

  @staticmethod
  def from_proto(msg: types_pb2.InputWord) -> 'InputWord':
    bbox = BBox.from_proto(msg.bounding_box)
    assert bbox is not None  # TODO: how do we handle this?

    text = None
    if msg.HasField('text'):
      text = msg.text
    confidence = None
    if msg.HasField('confidence'):
      confidence = WordConfidence.from_proto(msg.confidence)
    char_width = None
    if msg.HasField('char_width'):
      char_width = msg.char_width
    rotation_angle = None
    if msg.HasField('rotation_angle'):
      rotation_angle = msg.rotation_angle
    return InputWord(bbox, text, confidence, char_width, rotation_angle)
