# @generated by generate_proto_mypy_stubs.py.  Do not edit!
from comparison_pb2 import (
    ComparedValue as comparison_pb2___ComparedValue,
    ComparedValueCollection as comparison_pb2___ComparedValueCollection,
)

from entity_pb2 import (
    Entity as entity_pb2___Entity,
    EntityCollection as entity_pb2___EntityCollection,
)

from extraction_pb2 import (
    ExtractedValue as extraction_pb2___ExtractedValue,
    ExtractedValueCollection as extraction_pb2___ExtractedValueCollection,
)

from google.protobuf.internal.containers import (
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from record_pb2 import (
    RecordContext as record_pb2___RecordContext,
)

from targets_pb2 import (
    TargetValue as targets_pb2___TargetValue,
    TargetValueCollection as targets_pb2___TargetValueCollection,
)

from typing import (
    Iterable as typing___Iterable,
    Mapping as typing___Mapping,
    MutableMapping as typing___MutableMapping,
    Optional as typing___Optional,
    Text as typing___Text,
)


class Serialized(google___protobuf___message___Message):
    class DataEntry(google___protobuf___message___Message):
        key = ... # type: typing___Text

        @property
        def value(self) -> SerializedTypeOneOf: ...

        def __init__(self,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[SerializedTypeOneOf] = None,
            ) -> None: ...
        @classmethod
        def FromString(cls, s: bytes) -> Serialized.DataEntry: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

    root_id = ... # type: typing___Text
    foundation_type_version = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[int]

    @property
    def data(self) -> typing___MutableMapping[typing___Text, SerializedTypeOneOf]: ...

    def __init__(self,
        root_id : typing___Text,
        data : typing___Optional[typing___Mapping[typing___Text, SerializedTypeOneOf]] = None,
        foundation_type_version : typing___Optional[typing___Iterable[int]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Serialized: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class SerializedTypeOneOf(google___protobuf___message___Message):

    @property
    def record_context(self) -> record_pb2___RecordContext: ...

    @property
    def extracted_value(self) -> extraction_pb2___ExtractedValue: ...

    @property
    def target_value(self) -> targets_pb2___TargetValue: ...

    @property
    def compared_value(self) -> comparison_pb2___ComparedValue: ...

    @property
    def entity(self) -> entity_pb2___Entity: ...

    @property
    def extracted_value_collection(self) -> extraction_pb2___ExtractedValueCollection: ...

    @property
    def target_value_collection(self) -> targets_pb2___TargetValueCollection: ...

    @property
    def compared_value_collection(self) -> comparison_pb2___ComparedValueCollection: ...

    @property
    def entity_collection(self) -> entity_pb2___EntityCollection: ...

    def __init__(self,
        record_context : typing___Optional[record_pb2___RecordContext] = None,
        extracted_value : typing___Optional[extraction_pb2___ExtractedValue] = None,
        target_value : typing___Optional[targets_pb2___TargetValue] = None,
        compared_value : typing___Optional[comparison_pb2___ComparedValue] = None,
        entity : typing___Optional[entity_pb2___Entity] = None,
        extracted_value_collection : typing___Optional[extraction_pb2___ExtractedValueCollection] = None,
        target_value_collection : typing___Optional[targets_pb2___TargetValueCollection] = None,
        compared_value_collection : typing___Optional[comparison_pb2___ComparedValueCollection] = None,
        entity_collection : typing___Optional[entity_pb2___EntityCollection] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> SerializedTypeOneOf: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
