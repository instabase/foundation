# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: entity.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import geometry_pb2 as geometry__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='entity.proto',
  package='foundation',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0c\x65ntity.proto\x12\nfoundation\x1a\x0egeometry.proto\"2\n\x10\x45ntityCollection\x12\n\n\x02id\x18\x01 \x02(\t\x12\x12\n\nentity_ids\x18\x02 \x03(\t\"\x9a\x02\n\x06\x45ntity\x12\n\n\x02id\x18\x01 \x02(\t\x12\x31\n\x0b\x63hildren_id\x18\x02 \x01(\x0b\x32\x1c.foundation.EntityCollection\x12 \n\x04word\x18\x03 \x01(\x0b\x32\x10.foundation.WordH\x00\x12\x31\n\rfiller_string\x18\x04 \x01(\x0b\x32\x18.foundation.FillerStringH\x00\x12\'\n\x08sub_word\x18\x05 \x01(\x0b\x32\x13.foundation.SubWordH\x00\x12 \n\x04page\x18\x06 \x01(\x0b\x32\x10.foundation.PageH\x00\x12 \n\x04text\x18\x07 \x01(\x0b\x32\x10.foundation.TextH\x00\x42\x0f\n\rtype_specific\"4\n\x04Word\x12\x1e\n\x04\x62\x62ox\x18\x01 \x02(\x0b\x32\x10.foundation.BBox\x12\x0c\n\x04text\x18\x02 \x02(\t\"\x1c\n\x0c\x46illerString\x12\x0c\n\x04text\x18\x01 \x02(\t\"B\n\x07SubWord\x12\x0f\n\x07word_id\x18\x01 \x02(\t\x12\x13\n\x0bstart_index\x18\x02 \x02(\r\x12\x11\n\tend_index\x18\x03 \x02(\r\":\n\x04Page\x12\x1e\n\x04\x62\x62ox\x18\x01 \x03(\x0b\x32\x10.foundation.BBox\x12\x12\n\nimage_path\x18\x02 \x02(\t\"\x8f\x02\n\x04Text\x12.\n\x08words_id\x18\x01 \x01(\x0b\x32\x1c.foundation.EntityCollection\x12\x16\n\x0elikeness_score\x18\x02 \x01(\x01\x12 \n\x04\x64\x61te\x18\x03 \x01(\x0b\x32\x10.foundation.DateH\x00\x12\x35\n\x0f\x63urrency_amount\x18\x04 \x01(\x0b\x32\x1a.foundation.CurrencyAmountH\x00\x12-\n\x0bperson_name\x18\x05 \x01(\x0b\x32\x16.foundation.PersonNameH\x00\x12&\n\x07\x61\x64\x64ress\x18\x06 \x01(\x0b\x32\x13.foundation.AddressH\x00\x42\x0f\n\rtype_specific\"0\n\x04\x44\x61te\x12\x0c\n\x04year\x18\x01 \x02(\r\x12\r\n\x05month\x18\x02 \x02(\r\x12\x0b\n\x03\x64\x61y\x18\x03 \x02(\r\"m\n\x0e\x43urrencyAmount\x12\x35\n\x08\x63urrency\x18\x01 \x02(\x0e\x32#.foundation.CurrencyAmount.Currency\x12\x0e\n\x06\x61mount\x18\x02 \x02(\x03\"\x14\n\x08\x43urrency\x12\x08\n\x03USD\x10\xc8\x06\"\x0c\n\nPersonName\"\t\n\x07\x41\x64\x64ress'
  ,
  dependencies=[geometry__pb2.DESCRIPTOR,])



_CURRENCYAMOUNT_CURRENCY = _descriptor.EnumDescriptor(
  name='Currency',
  full_name='foundation.CurrencyAmount.Currency',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='USD', index=0, number=840,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1006,
  serialized_end=1026,
)
_sym_db.RegisterEnumDescriptor(_CURRENCYAMOUNT_CURRENCY)


_ENTITYCOLLECTION = _descriptor.Descriptor(
  name='EntityCollection',
  full_name='foundation.EntityCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='foundation.EntityCollection.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_ids', full_name='foundation.EntityCollection.entity_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=94,
)


_ENTITY = _descriptor.Descriptor(
  name='Entity',
  full_name='foundation.Entity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='foundation.Entity.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='children_id', full_name='foundation.Entity.children_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='word', full_name='foundation.Entity.word', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filler_string', full_name='foundation.Entity.filler_string', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sub_word', full_name='foundation.Entity.sub_word', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page', full_name='foundation.Entity.page', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='foundation.Entity.text', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='type_specific', full_name='foundation.Entity.type_specific',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=97,
  serialized_end=379,
)


_WORD = _descriptor.Descriptor(
  name='Word',
  full_name='foundation.Word',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bbox', full_name='foundation.Word.bbox', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='foundation.Word.text', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=381,
  serialized_end=433,
)


_FILLERSTRING = _descriptor.Descriptor(
  name='FillerString',
  full_name='foundation.FillerString',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='foundation.FillerString.text', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=435,
  serialized_end=463,
)


_SUBWORD = _descriptor.Descriptor(
  name='SubWord',
  full_name='foundation.SubWord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='word_id', full_name='foundation.SubWord.word_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_index', full_name='foundation.SubWord.start_index', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_index', full_name='foundation.SubWord.end_index', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=465,
  serialized_end=531,
)


_PAGE = _descriptor.Descriptor(
  name='Page',
  full_name='foundation.Page',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bbox', full_name='foundation.Page.bbox', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='image_path', full_name='foundation.Page.image_path', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=533,
  serialized_end=591,
)


_TEXT = _descriptor.Descriptor(
  name='Text',
  full_name='foundation.Text',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='words_id', full_name='foundation.Text.words_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='likeness_score', full_name='foundation.Text.likeness_score', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date', full_name='foundation.Text.date', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='currency_amount', full_name='foundation.Text.currency_amount', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='person_name', full_name='foundation.Text.person_name', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='address', full_name='foundation.Text.address', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='type_specific', full_name='foundation.Text.type_specific',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=594,
  serialized_end=865,
)


_DATE = _descriptor.Descriptor(
  name='Date',
  full_name='foundation.Date',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='year', full_name='foundation.Date.year', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='month', full_name='foundation.Date.month', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='day', full_name='foundation.Date.day', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=867,
  serialized_end=915,
)


_CURRENCYAMOUNT = _descriptor.Descriptor(
  name='CurrencyAmount',
  full_name='foundation.CurrencyAmount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='currency', full_name='foundation.CurrencyAmount.currency', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=840,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='amount', full_name='foundation.CurrencyAmount.amount', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CURRENCYAMOUNT_CURRENCY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=917,
  serialized_end=1026,
)


_PERSONNAME = _descriptor.Descriptor(
  name='PersonName',
  full_name='foundation.PersonName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1028,
  serialized_end=1040,
)


_ADDRESS = _descriptor.Descriptor(
  name='Address',
  full_name='foundation.Address',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1042,
  serialized_end=1051,
)

_ENTITY.fields_by_name['children_id'].message_type = _ENTITYCOLLECTION
_ENTITY.fields_by_name['word'].message_type = _WORD
_ENTITY.fields_by_name['filler_string'].message_type = _FILLERSTRING
_ENTITY.fields_by_name['sub_word'].message_type = _SUBWORD
_ENTITY.fields_by_name['page'].message_type = _PAGE
_ENTITY.fields_by_name['text'].message_type = _TEXT
_ENTITY.oneofs_by_name['type_specific'].fields.append(
  _ENTITY.fields_by_name['word'])
_ENTITY.fields_by_name['word'].containing_oneof = _ENTITY.oneofs_by_name['type_specific']
_ENTITY.oneofs_by_name['type_specific'].fields.append(
  _ENTITY.fields_by_name['filler_string'])
_ENTITY.fields_by_name['filler_string'].containing_oneof = _ENTITY.oneofs_by_name['type_specific']
_ENTITY.oneofs_by_name['type_specific'].fields.append(
  _ENTITY.fields_by_name['sub_word'])
_ENTITY.fields_by_name['sub_word'].containing_oneof = _ENTITY.oneofs_by_name['type_specific']
_ENTITY.oneofs_by_name['type_specific'].fields.append(
  _ENTITY.fields_by_name['page'])
_ENTITY.fields_by_name['page'].containing_oneof = _ENTITY.oneofs_by_name['type_specific']
_ENTITY.oneofs_by_name['type_specific'].fields.append(
  _ENTITY.fields_by_name['text'])
_ENTITY.fields_by_name['text'].containing_oneof = _ENTITY.oneofs_by_name['type_specific']
_WORD.fields_by_name['bbox'].message_type = geometry__pb2._BBOX
_PAGE.fields_by_name['bbox'].message_type = geometry__pb2._BBOX
_TEXT.fields_by_name['words_id'].message_type = _ENTITYCOLLECTION
_TEXT.fields_by_name['date'].message_type = _DATE
_TEXT.fields_by_name['currency_amount'].message_type = _CURRENCYAMOUNT
_TEXT.fields_by_name['person_name'].message_type = _PERSONNAME
_TEXT.fields_by_name['address'].message_type = _ADDRESS
_TEXT.oneofs_by_name['type_specific'].fields.append(
  _TEXT.fields_by_name['date'])
_TEXT.fields_by_name['date'].containing_oneof = _TEXT.oneofs_by_name['type_specific']
_TEXT.oneofs_by_name['type_specific'].fields.append(
  _TEXT.fields_by_name['currency_amount'])
_TEXT.fields_by_name['currency_amount'].containing_oneof = _TEXT.oneofs_by_name['type_specific']
_TEXT.oneofs_by_name['type_specific'].fields.append(
  _TEXT.fields_by_name['person_name'])
_TEXT.fields_by_name['person_name'].containing_oneof = _TEXT.oneofs_by_name['type_specific']
_TEXT.oneofs_by_name['type_specific'].fields.append(
  _TEXT.fields_by_name['address'])
_TEXT.fields_by_name['address'].containing_oneof = _TEXT.oneofs_by_name['type_specific']
_CURRENCYAMOUNT.fields_by_name['currency'].enum_type = _CURRENCYAMOUNT_CURRENCY
_CURRENCYAMOUNT_CURRENCY.containing_type = _CURRENCYAMOUNT
DESCRIPTOR.message_types_by_name['EntityCollection'] = _ENTITYCOLLECTION
DESCRIPTOR.message_types_by_name['Entity'] = _ENTITY
DESCRIPTOR.message_types_by_name['Word'] = _WORD
DESCRIPTOR.message_types_by_name['FillerString'] = _FILLERSTRING
DESCRIPTOR.message_types_by_name['SubWord'] = _SUBWORD
DESCRIPTOR.message_types_by_name['Page'] = _PAGE
DESCRIPTOR.message_types_by_name['Text'] = _TEXT
DESCRIPTOR.message_types_by_name['Date'] = _DATE
DESCRIPTOR.message_types_by_name['CurrencyAmount'] = _CURRENCYAMOUNT
DESCRIPTOR.message_types_by_name['PersonName'] = _PERSONNAME
DESCRIPTOR.message_types_by_name['Address'] = _ADDRESS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EntityCollection = _reflection.GeneratedProtocolMessageType('EntityCollection', (_message.Message,), {
  'DESCRIPTOR' : _ENTITYCOLLECTION,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.EntityCollection)
  })
_sym_db.RegisterMessage(EntityCollection)

Entity = _reflection.GeneratedProtocolMessageType('Entity', (_message.Message,), {
  'DESCRIPTOR' : _ENTITY,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.Entity)
  })
_sym_db.RegisterMessage(Entity)

Word = _reflection.GeneratedProtocolMessageType('Word', (_message.Message,), {
  'DESCRIPTOR' : _WORD,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.Word)
  })
_sym_db.RegisterMessage(Word)

FillerString = _reflection.GeneratedProtocolMessageType('FillerString', (_message.Message,), {
  'DESCRIPTOR' : _FILLERSTRING,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.FillerString)
  })
_sym_db.RegisterMessage(FillerString)

SubWord = _reflection.GeneratedProtocolMessageType('SubWord', (_message.Message,), {
  'DESCRIPTOR' : _SUBWORD,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.SubWord)
  })
_sym_db.RegisterMessage(SubWord)

Page = _reflection.GeneratedProtocolMessageType('Page', (_message.Message,), {
  'DESCRIPTOR' : _PAGE,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.Page)
  })
_sym_db.RegisterMessage(Page)

Text = _reflection.GeneratedProtocolMessageType('Text', (_message.Message,), {
  'DESCRIPTOR' : _TEXT,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.Text)
  })
_sym_db.RegisterMessage(Text)

Date = _reflection.GeneratedProtocolMessageType('Date', (_message.Message,), {
  'DESCRIPTOR' : _DATE,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.Date)
  })
_sym_db.RegisterMessage(Date)

CurrencyAmount = _reflection.GeneratedProtocolMessageType('CurrencyAmount', (_message.Message,), {
  'DESCRIPTOR' : _CURRENCYAMOUNT,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.CurrencyAmount)
  })
_sym_db.RegisterMessage(CurrencyAmount)

PersonName = _reflection.GeneratedProtocolMessageType('PersonName', (_message.Message,), {
  'DESCRIPTOR' : _PERSONNAME,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.PersonName)
  })
_sym_db.RegisterMessage(PersonName)

Address = _reflection.GeneratedProtocolMessageType('Address', (_message.Message,), {
  'DESCRIPTOR' : _ADDRESS,
  '__module__' : 'entity_pb2'
  # @@protoc_insertion_point(class_scope:foundation.Address)
  })
_sym_db.RegisterMessage(Address)


# @@protoc_insertion_point(module_scope)
