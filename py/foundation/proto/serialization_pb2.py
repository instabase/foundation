# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: serialization.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import entity_pb2 as entity__pb2
import extraction_pb2 as extraction__pb2
import targets_pb2 as targets__pb2
import comparison_pb2 as comparison__pb2
import record_pb2 as record__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='serialization.proto',
  package='foundation',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13serialization.proto\x12\nfoundation\x1a\x0c\x65ntity.proto\x1a\x10\x65xtraction.proto\x1a\rtargets.proto\x1a\x10\x63omparison.proto\x1a\x0crecord.proto\"\xbc\x01\n\nSerialized\x12.\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32 .foundation.Serialized.DataEntry\x12\x0f\n\x07root_id\x18\x02 \x02(\t\x12\x1f\n\x17\x66oundation_type_version\x18\x03 \x03(\r\x1aL\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12.\n\x05value\x18\x02 \x01(\x0b\x32\x1f.foundation.SerializedTypeOneOf:\x02\x38\x01\"\xbe\x04\n\x13SerializedTypeOneOf\x12\x33\n\x0erecord_context\x18\x01 \x01(\x0b\x32\x19.foundation.RecordContextH\x00\x12\x35\n\x0f\x65xtracted_value\x18\x02 \x01(\x0b\x32\x1a.foundation.ExtractedValueH\x00\x12/\n\x0ctarget_value\x18\x03 \x01(\x0b\x32\x17.foundation.TargetValueH\x00\x12\x33\n\x0e\x63ompared_value\x18\x04 \x01(\x0b\x32\x19.foundation.ComparedValueH\x00\x12$\n\x06\x65ntity\x18\x05 \x01(\x0b\x32\x12.foundation.EntityH\x00\x12J\n\x1a\x65xtracted_value_collection\x18\x06 \x01(\x0b\x32$.foundation.ExtractedValueCollectionH\x00\x12\x44\n\x17target_value_collection\x18\x07 \x01(\x0b\x32!.foundation.TargetValueCollectionH\x00\x12H\n\x19\x63ompared_value_collection\x18\x08 \x01(\x0b\x32#.foundation.ComparedValueCollectionH\x00\x12\x39\n\x11\x65ntity_collection\x18\t \x01(\x0b\x32\x1c.foundation.EntityCollectionH\x00\x42\x18\n\x16serialized_type_one_of'
  ,
  dependencies=[entity__pb2.DESCRIPTOR,extraction__pb2.DESCRIPTOR,targets__pb2.DESCRIPTOR,comparison__pb2.DESCRIPTOR,record__pb2.DESCRIPTOR,])




_SERIALIZED_DATAENTRY = _descriptor.Descriptor(
  name='DataEntry',
  full_name='foundation.Serialized.DataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='foundation.Serialized.DataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='foundation.Serialized.DataEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=227,
  serialized_end=303,
)

_SERIALIZED = _descriptor.Descriptor(
  name='Serialized',
  full_name='foundation.Serialized',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='foundation.Serialized.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='root_id', full_name='foundation.Serialized.root_id', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='foundation_type_version', full_name='foundation.Serialized.foundation_type_version', index=2,
      number=3, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_SERIALIZED_DATAENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=115,
  serialized_end=303,
)


_SERIALIZEDTYPEONEOF = _descriptor.Descriptor(
  name='SerializedTypeOneOf',
  full_name='foundation.SerializedTypeOneOf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='record_context', full_name='foundation.SerializedTypeOneOf.record_context', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extracted_value', full_name='foundation.SerializedTypeOneOf.extracted_value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='target_value', full_name='foundation.SerializedTypeOneOf.target_value', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compared_value', full_name='foundation.SerializedTypeOneOf.compared_value', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity', full_name='foundation.SerializedTypeOneOf.entity', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extracted_value_collection', full_name='foundation.SerializedTypeOneOf.extracted_value_collection', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='target_value_collection', full_name='foundation.SerializedTypeOneOf.target_value_collection', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compared_value_collection', full_name='foundation.SerializedTypeOneOf.compared_value_collection', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_collection', full_name='foundation.SerializedTypeOneOf.entity_collection', index=8,
      number=9, type=11, cpp_type=10, label=1,
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
      name='serialized_type_one_of', full_name='foundation.SerializedTypeOneOf.serialized_type_one_of',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=306,
  serialized_end=880,
)

_SERIALIZED_DATAENTRY.fields_by_name['value'].message_type = _SERIALIZEDTYPEONEOF
_SERIALIZED_DATAENTRY.containing_type = _SERIALIZED
_SERIALIZED.fields_by_name['data'].message_type = _SERIALIZED_DATAENTRY
_SERIALIZEDTYPEONEOF.fields_by_name['record_context'].message_type = record__pb2._RECORDCONTEXT
_SERIALIZEDTYPEONEOF.fields_by_name['extracted_value'].message_type = extraction__pb2._EXTRACTEDVALUE
_SERIALIZEDTYPEONEOF.fields_by_name['target_value'].message_type = targets__pb2._TARGETVALUE
_SERIALIZEDTYPEONEOF.fields_by_name['compared_value'].message_type = comparison__pb2._COMPAREDVALUE
_SERIALIZEDTYPEONEOF.fields_by_name['entity'].message_type = entity__pb2._ENTITY
_SERIALIZEDTYPEONEOF.fields_by_name['extracted_value_collection'].message_type = extraction__pb2._EXTRACTEDVALUECOLLECTION
_SERIALIZEDTYPEONEOF.fields_by_name['target_value_collection'].message_type = targets__pb2._TARGETVALUECOLLECTION
_SERIALIZEDTYPEONEOF.fields_by_name['compared_value_collection'].message_type = comparison__pb2._COMPAREDVALUECOLLECTION
_SERIALIZEDTYPEONEOF.fields_by_name['entity_collection'].message_type = entity__pb2._ENTITYCOLLECTION
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['record_context'])
_SERIALIZEDTYPEONEOF.fields_by_name['record_context'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['extracted_value'])
_SERIALIZEDTYPEONEOF.fields_by_name['extracted_value'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['target_value'])
_SERIALIZEDTYPEONEOF.fields_by_name['target_value'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['compared_value'])
_SERIALIZEDTYPEONEOF.fields_by_name['compared_value'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['entity'])
_SERIALIZEDTYPEONEOF.fields_by_name['entity'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['extracted_value_collection'])
_SERIALIZEDTYPEONEOF.fields_by_name['extracted_value_collection'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['target_value_collection'])
_SERIALIZEDTYPEONEOF.fields_by_name['target_value_collection'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['compared_value_collection'])
_SERIALIZEDTYPEONEOF.fields_by_name['compared_value_collection'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
_SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of'].fields.append(
  _SERIALIZEDTYPEONEOF.fields_by_name['entity_collection'])
_SERIALIZEDTYPEONEOF.fields_by_name['entity_collection'].containing_oneof = _SERIALIZEDTYPEONEOF.oneofs_by_name['serialized_type_one_of']
DESCRIPTOR.message_types_by_name['Serialized'] = _SERIALIZED
DESCRIPTOR.message_types_by_name['SerializedTypeOneOf'] = _SERIALIZEDTYPEONEOF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Serialized = _reflection.GeneratedProtocolMessageType('Serialized', (_message.Message,), {

  'DataEntry' : _reflection.GeneratedProtocolMessageType('DataEntry', (_message.Message,), {
    'DESCRIPTOR' : _SERIALIZED_DATAENTRY,
    '__module__' : 'serialization_pb2'
    # @@protoc_insertion_point(class_scope:foundation.Serialized.DataEntry)
    })
  ,
  'DESCRIPTOR' : _SERIALIZED,
  '__module__' : 'serialization_pb2'
  # @@protoc_insertion_point(class_scope:foundation.Serialized)
  })
_sym_db.RegisterMessage(Serialized)
_sym_db.RegisterMessage(Serialized.DataEntry)

SerializedTypeOneOf = _reflection.GeneratedProtocolMessageType('SerializedTypeOneOf', (_message.Message,), {
  'DESCRIPTOR' : _SERIALIZEDTYPEONEOF,
  '__module__' : 'serialization_pb2'
  # @@protoc_insertion_point(class_scope:foundation.SerializedTypeOneOf)
  })
_sym_db.RegisterMessage(SerializedTypeOneOf)


_SERIALIZED_DATAENTRY._options = None
# @@protoc_insertion_point(module_scope)