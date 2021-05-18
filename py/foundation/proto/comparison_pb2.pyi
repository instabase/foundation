# @generated by generate_proto_mypy_stubs.py.  Do not edit!
from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Optional as typing___Optional,
    Text as typing___Text,
)


class ComparedValue(google___protobuf___message___Message):
    id = ... # type: typing___Text
    target_value_id = ... # type: typing___Text
    extracted_value_id = ... # type: typing___Text
    score = ... # type: float
    message = ... # type: typing___Text

    def __init__(self,
        id : typing___Text,
        target_value_id : typing___Text,
        extracted_value_id : typing___Text,
        score : typing___Optional[float] = None,
        message : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ComparedValue: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class ComparedValueCollection(google___protobuf___message___Message):
    id = ... # type: typing___Text
    compared_value_ids = ... # type: typing___Text

    def __init__(self,
        id : typing___Text,
        compared_value_ids : typing___Text,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> ComparedValueCollection: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...