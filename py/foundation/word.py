from dataclasses import dataclass
from typing import Callable, List

from foundation.geometry import BBox

from .python_pb.word_pb2 import Word as PBWord


WordID = str


@dataclass(frozen=True)
class Word:
  """A word.

  Attributes:
    word_id: A string to uniquely identify the word.
    text: The text. The word itself.
    bbox: The bounding box of the word.
  """

  word_id: WordID
  text: str
  bbox: BBox

  @staticmethod
  def from_proto(proto: PBWord) -> 'Word':
    return Word(proto.word_id, proto.text, proto.bbox)

  def to_proto(self) -> PBWord:
    return PBWord(word_id=self.word_id, text=self.text, bbox=self.bbox)
