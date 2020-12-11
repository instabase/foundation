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

  def to_proto(self) -> types_pb2.CharConfidence:
    msg = types_pb2.CharConfidence()
    msg.percentage = self.percentage
    if self.unsure is not None:
      msg.unsure = self.unsure
    return msg


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
    char_confidences = None
    if len(msg.char_confidences) > 0:
      char_confidences = [
          CharConfidence.from_proto(c) for c in msg.char_confidences
      ]
    return WordConfidence(word_confidence, low_confidence, char_confidences)

  def to_proto(self) -> types_pb2.WordConfidence:
    msg = types_pb2.WordConfidence()
    if self.word_confidence is not None:
      msg.word_confidence = self.word_confidence
    if self.low_confidence is not None:
      msg.low_confidence = self.low_confidence
    if self.char_confidences is not None:
      for char_confidence in self.char_confidences:
        msg.char_confidences.append(char_confidence.to_proto())
    return msg


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

  def to_proto(self) -> types_pb2.InputWord:
    msg = types_pb2.InputWord()
    msg.bounding_box.CopyFrom(self.bounding_box.to_proto())
    if self.text is not None:
      msg.text = self.text
    if self.confidence is not None:
      msg.confidence.CopyFrom(self.confidence.to_proto())
    if self.char_width is not None:
      msg.char_width = self.char_width
    if self.rotation_angle is not None:
      msg.rotation_angle = self.rotation_angle

    return msg
