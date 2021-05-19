
from typing import Mapping, Union, Iterable, Dict
from dataclasses import dataclass

from foundation.proto import serialization_pb2

from foundation.record import RecordContext
from foundation.targets import TargetValueCollection
from foundation.entity import Entity
from foundation.entity import EntityCollection
from foundation.comparison import ComparedValue
from foundation.extraction import ExtractedValue
from foundation.targets import TargetValue
from foundation.extraction import ExtractedValueCollection
from foundation.comparison import ComparedValueCollection

SerializedTypeOneOf = Union[
  RecordContext,
  ExtractedValue,
  TargetValue,
  ComparedValue,
  Entity,
  ExtractedValueCollection,
  TargetValueCollection,
  ComparedValueCollection,
  EntityCollection
]

CLASS_MAPPING = {
  "record_context": RecordContext,
  "extracted_value": ExtractedValue,
  "target_value": TargetValue,
  "compared_value": ComparedValue,
  "entity": Entity,
  "extracted_value_collection": ExtractedValueCollection,
  "target_value_collection": TargetValueCollection,
  "compared_value_collection": ComparedValueCollection,
  "entity_collection": EntityCollection,
}

@dataclass
class Serialized(Mapping[str, SerializedTypeOneOf]):
  _proto: serialization_pb2.Serialized

  @property
  def root(self) -> 'SerializedTypeOneOf':
    return self[self._proto.root_id]

  @property
  def foundation_type_version(self) -> 'str':
    return '.'.join(str(i) for i in self._proto.foundation_type_version)

  def __getitem__(self, k: str) -> SerializedTypeOneOf:
      item = self._proto.data[k]
      item_type = item.WhichOneof("serialized_type_one_of")
      item_class = CLASS_MAPPING[item_type]
      return item_class(item, self)

  def __iter__(self) -> Iterable[str]: # type: ignore
    yield from self._proto.data

  def __len__(self) -> int:
    return len(self._proto.data)

  def as_proto(self) -> serialization_pb2.Serialized:
    return self._proto

  @staticmethod
  def from_reference_map(reference_map: Mapping[str, SerializedTypeOneOf], root_id: str) -> 'Serialized':
    proto = serialization_pb2.Serialized(
      root_id=root_id,
      foundation_type_version=[0,1,0],
    )
    for k, v in reference_map.items():
      oneof = serialization_pb2.SerializedTypeOneOf()
      for type_str, cls in CLASS_MAPPING.items():
        if isinstance(v, cls):
          setattr(oneof, type_str, v.as_proto())
      assert oneof.WhichOneof is not None, f"Instance of {type(v)} was not recognized for serialization"
      proto.data[k] = oneof
    return Serialized(proto)

def dumps(obj: SerializedTypeOneOf) -> bytes:
  root_id = obj.id
  reference_map: Dict[str, SerializedTypeOneOf] = {}
  serialized = Serialized.from_reference_map(reference_map, root_id)
  return serialized.as_proto().SerializeToString()

def loads(bytestring: bytes) -> SerializedTypeOneOf:
  proto = serialization_pb2.Serialized.ParseFromString(bytestring)
  serialized = Serialized(proto)
  return serialized.root