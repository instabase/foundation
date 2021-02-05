""" OCR types wrappers. """

from dataclasses import dataclass
from typing import Optional, Iterable, Tuple

from .geometry import BBox


@dataclass(frozen=True)
class CharConfidence:
  percentage: float
  unsure: Optional[bool]


@dataclass(frozen=True)
class WordConfidence:
  word_confidence: Optional[float]
  low_confidence: Optional[bool]
  char_confidences: Optional[Tuple[CharConfidence, ...]]


@dataclass(frozen=True)
class InputWord:
  bbox: BBox
  text: str
  confidence: Optional[WordConfidence] = None

  char_width: Optional[float] = None
  rotation_angle: Optional[float] = None

  def height(self) -> float:
    return self.bbox.height

  def __str__(self) -> str:
    return 'InputWord("{}", bbox={})'.format(self.text, self.bbox)

  @staticmethod
  def median_word_height(words: Iterable['InputWord']) -> float:
    L = sorted(words, key=InputWord.height)
    if not L:
      return 0
    n = len(L)
    if n % 2 == 0:
      return 0.5 * (L[n // 2 - 1].height() + L[n // 2].height())
    return L[(n - 1) // 2].height()
