# @generated by generate_proto_mypy_stubs.py.  Do not edit!
from google.protobuf.internal.containers import (
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
    Text as typing___Text,
)


class ExtractedValue(google___protobuf___message___Message):
    id = ... # type: typing___Text
    field_name = ... # type: typing___Text
    type = ... # type: typing___Text
    serialized_value = ... # type: bytes
    entity_ids = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    def __init__(self,
        id : typing___Optional[typing___Text] = None,
        field_name : typing___Optional[typing___Text] = None,
        type : typing___Optional[typing___Text] = None,
        serialized_value : typing___Optional[bytes] = None,
        entity_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ExtractedValue: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class ExtractedValueCollection(google___protobuf___message___Message):
    id = ... # type: typing___Text
    extracted_value_ids = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    def __init__(self,
        id : typing___Optional[typing___Text] = None,
        extracted_value_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ExtractedValueCollection: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
