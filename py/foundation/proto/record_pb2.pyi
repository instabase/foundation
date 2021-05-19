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


class RecordContext(google___protobuf___message___Message):
    id = ... # type: typing___Text
    entity_ids = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    collection_ids = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    page_ids = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    text_id = ... # type: typing___Text
    extracted_value_ids = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    def __init__(self,
        id : typing___Optional[typing___Text] = None,
        entity_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        collection_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        page_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        text_id : typing___Optional[typing___Text] = None,
        extracted_value_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> RecordContext: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
