
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from .proto import record_pb2

from .extraction import ExtractedValue
from .entity import Page
from .entity import Text
from .entity import Entity


@dataclass
class RecordContext:
  _proto: record_pb2.RecordContext
  _reference_map: Mapping[str, Any]

  @property
  def id(self) -> str:
    return self._proto.id
  @property
  def entitys(self) -> Iterable[Entity]:
    yield from (self._reference_map[i] for i in self._proto.entity_ids)

  @property
  def collections(self) -> Iterable[Entity]:
    yield from (self._reference_map[i] for i in self._proto.collection_ids)

  @property
  def pages(self) -> Iterable[Page]:
    yield from (self._reference_map[i] for i in self._proto.page_ids)

  @property
  def text(self) -> Text:
    return self._reference_map[self._proto.text_id]

  @property
  def extracted_values(self) -> Iterable[ExtractedValue]:
    yield from (self._reference_map[i] for i in self._proto.extracted_value_ids)


  def as_proto(self) -> record_pb2.RecordContext:
    return self._proto

  @staticmethod
  def from_proto(proto: record_pb2.RecordContext, reference_map: Mapping[str, Any]):
    return RecordContext(proto, reference_map)

