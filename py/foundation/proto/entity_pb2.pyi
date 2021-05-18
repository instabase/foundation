# @generated by generate_proto_mypy_stubs.py.  Do not edit!
from foundation.proto.geometry_pb2 import (
    BBox as foundation___proto___geometry_pb2___BBox,
)

from google.protobuf.descriptor import (
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    List as typing___List,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    cast as typing___cast,
)


class EntityCollection(google___protobuf___message___Message):
    id = ... # type: typing___Text
    entity_ids = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]

    def __init__(self,
        id : typing___Text,
        entity_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> EntityCollection: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Entity(google___protobuf___message___Message):
    id = ... # type: typing___Text
    children_id = ... # type: typing___Text

    @property
    def word(self) -> Word: ...

    @property
    def filler_string(self) -> FillerString: ...

    @property
    def sub_word(self) -> SubWord: ...

    @property
    def page(self) -> Page: ...

    @property
    def text(self) -> Text: ...

    def __init__(self,
        id : typing___Text,
        children_id : typing___Optional[typing___Text] = None,
        word : typing___Optional[Word] = None,
        filler_string : typing___Optional[FillerString] = None,
        sub_word : typing___Optional[SubWord] = None,
        page : typing___Optional[Page] = None,
        text : typing___Optional[Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Entity: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Word(google___protobuf___message___Message):
    text = ... # type: typing___Text

    @property
    def bbox(self) -> foundation___proto___geometry_pb2___BBox: ...

    def __init__(self,
        bbox : foundation___proto___geometry_pb2___BBox,
        text : typing___Text,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Word: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class FillerString(google___protobuf___message___Message):
    text = ... # type: typing___Text

    def __init__(self,
        text : typing___Text,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> FillerString: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class SubWord(google___protobuf___message___Message):
    word_id = ... # type: typing___Text
    start_index = ... # type: int
    end_index = ... # type: int

    def __init__(self,
        word_id : typing___Text,
        start_index : int,
        end_index : int,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> SubWord: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Page(google___protobuf___message___Message):
    image_path = ... # type: typing___Text

    @property
    def bbox(self) -> foundation___proto___geometry_pb2___BBox: ...

    def __init__(self,
        bbox : foundation___proto___geometry_pb2___BBox,
        image_path : typing___Text,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Page: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Text(google___protobuf___message___Message):
    word_ids = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    likeness_score = ... # type: float

    @property
    def date(self) -> Date: ...

    @property
    def currency_amount(self) -> CurrencyAmount: ...

    @property
    def person_name(self) -> PersonName: ...

    @property
    def address(self) -> Address: ...

    def __init__(self,
        word_ids : typing___Optional[typing___Iterable[typing___Text]] = None,
        likeness_score : typing___Optional[float] = None,
        date : typing___Optional[Date] = None,
        currency_amount : typing___Optional[CurrencyAmount] = None,
        person_name : typing___Optional[PersonName] = None,
        address : typing___Optional[Address] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Text: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Date(google___protobuf___message___Message):
    year = ... # type: int
    month = ... # type: int
    day = ... # type: int

    def __init__(self,
        year : int,
        month : int,
        day : int,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Date: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class CurrencyAmount(google___protobuf___message___Message):
    class Currency(int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: int) -> str: ...
        @classmethod
        def Value(cls, name: str) -> CurrencyAmount.Currency: ...
        @classmethod
        def keys(cls) -> typing___List[str]: ...
        @classmethod
        def values(cls) -> typing___List[CurrencyAmount.Currency]: ...
        @classmethod
        def items(cls) -> typing___List[typing___Tuple[str, CurrencyAmount.Currency]]: ...
    USD = typing___cast(Currency, 840)

    currency = ... # type: CurrencyAmount.Currency
    amount = ... # type: int

    def __init__(self,
        currency : CurrencyAmount.Currency,
        amount : int,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> CurrencyAmount: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class PersonName(google___protobuf___message___Message):

    def __init__(self,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> PersonName: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class Address(google___protobuf___message___Message):

    def __init__(self,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: bytes) -> Address: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
