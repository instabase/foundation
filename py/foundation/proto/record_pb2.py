# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: foundation/proto/record.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='foundation/proto/record.proto',
  package='foundation',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1d\x66oundation/proto/record.proto\x12\nfoundation\"\x87\x01\n\rRecordContext\x12\n\n\x02id\x18\x01 \x02(\t\x12\x12\n\nentity_ids\x18\x02 \x03(\t\x12\x16\n\x0e\x63ollection_ids\x18\x03 \x03(\t\x12\x10\n\x08page_ids\x18\x04 \x03(\t\x12\x0f\n\x07text_id\x18\x05 \x02(\t\x12\x1b\n\x13\x65xtracted_value_ids\x18\x06 \x03(\t'
)




_RECORDCONTEXT = _descriptor.Descriptor(
  name='RecordContext',
  full_name='foundation.RecordContext',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='foundation.RecordContext.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_ids', full_name='foundation.RecordContext.entity_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='collection_ids', full_name='foundation.RecordContext.collection_ids', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page_ids', full_name='foundation.RecordContext.page_ids', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text_id', full_name='foundation.RecordContext.text_id', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extracted_value_ids', full_name='foundation.RecordContext.extracted_value_ids', index=5,
      number=6, type=9, cpp_type=9, label=3,
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
  serialized_start=46,
  serialized_end=181,
)

DESCRIPTOR.message_types_by_name['RecordContext'] = _RECORDCONTEXT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RecordContext = _reflection.GeneratedProtocolMessageType('RecordContext', (_message.Message,), {
  'DESCRIPTOR' : _RECORDCONTEXT,
  '__module__' : 'foundation.proto.record_pb2'
  # @@protoc_insertion_point(class_scope:foundation.RecordContext)
  })
_sym_db.RegisterMessage(RecordContext)


# @@protoc_insertion_point(module_scope)
