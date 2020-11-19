""" Entity wrappers. """

import abc
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from foundation.protos import geometry_pb2
from foundation.protos.doc import entity_pb2
from foundation.protos.doc.entity_pb2 import Currency as Currency_pb2

from .ocr import InputWord


@dataclass(frozen=True)
class Entity(abc.ABC):
  pass


@dataclass(frozen=True)
class OcrWordEntity(Entity):
  word: InputWord


@dataclass(frozen=True)
class LineEntity(Entity):
  ocr_words: List[OcrWordEntity]


@dataclass(frozen=True)
class Paragraph(Entity):
  lines: List[LineEntity]


@dataclass(frozen=True)
class TableCellEntity(Entity):
  content: List[Entity]


@dataclass(frozen=True)
class TableRowEntity(Entity):
  cells: List[TableCellEntity]


@dataclass(frozen=True)
class TableEntity(Entity):
  rows: List[TableCellEntity]


@dataclass(frozen=True)
class TokenEntity(Entity):
  span: List[InputWord]
  score: Optional[float]


@dataclass(frozen=True)
class PhraseEntity(Entity):
  words: List[TokenEntity]
  score: Optional[float]


_T = TypeVar('_T')


@dataclass(frozen=True)
class SemanticEntity(Entity, Generic[_T]):
  value: Optional[_T]
  score: Optional[float]


@dataclass(frozen=True)
class NumberEntity(SemanticEntity[float]):
  token: TokenEntity


@dataclass(frozen=True)
class IntegerEntity(SemanticEntity[int]):
  token: TokenEntity


@dataclass(frozen=True)
class DateEntity(SemanticEntity[str]):
  token: TokenEntity


@dataclass(frozen=True)
class TimeEntity(SemanticEntity[int]):
  token: TokenEntity


@dataclass(frozen=True)
class CurrencyEntity(SemanticEntity[Currency_pb2.FixedDecimal]):
  # TODO: wrap FixedDecimal
  token: TokenEntity
  units: Optional[str]


@dataclass(frozen=True)
class NameEntity(SemanticEntity[str]):
  name_parts: PhraseEntity


@dataclass(frozen=True)
class AddressEntity(SemanticEntity[str]):
  lines: List[PhraseEntity]


@dataclass(frozen=True)
class ClusterEntity(Entity):
  token_span: PhraseEntity
  label: Optional[str]
  score: Optional[float]
