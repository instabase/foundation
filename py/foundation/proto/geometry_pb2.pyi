# @generated by generate_proto_mypy_stubs.py.  Do not edit!
from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)


class Interval(google___protobuf___message___Message):
    a = ... # type: float
    b = ... # type: float

    def __init__(self,
        a : float,
        b : float,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Interval: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Point(google___protobuf___message___Message):
    x = ... # type: float
    y = ... # type: float

    def __init__(self,
        x : float,
        y : float,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Point: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Rectangle(google___protobuf___message___Message):

    @property
    def ix(self) -> Interval: ...

    @property
    def iy(self) -> Interval: ...

    def __init__(self,
        ix : Interval,
        iy : Interval,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Rectangle: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class BBox(google___protobuf___message___Message):
    page_index = ... # type: int

    @property
    def rectangle(self) -> Rectangle: ...

    def __init__(self,
        rectangle : Rectangle,
        page_index : int,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> BBox: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...