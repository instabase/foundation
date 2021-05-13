from foundation.proto import geometry_pb2, entity_pb2, extraction_pb2, targets_pb2, record_pb2, comparison_pb2, serialization_pb2

modules = {
  "geometry": geometry_pb2,
  "entity": entity_pb2,
  "extraction": extraction_pb2,
  "targets": targets_pb2,
  "record": record_pb2,
  "comparison": comparison_pb2,
  "serialization": serialization_pb2
}

rtn = {}

TYPE_ENUM_LKP = {
  8: bool,
  12: bytes,
  1: float,
  14: int,
  7: int,
  6: int,
  2: float,
  10: None, # GROUP
  5: int,
  3: int,
  11: None, # MESSAGE
  15: int,
  16: int,
  17: int,
  18: int,
  9: str,
  13: int,
  4: int,
}


for filename, module in modules.items():
  message_type_names = [i for i in dir(module) if not i.startswith('_') and i != 'DESCRIPTOR']
  message_types = {
    name: getattr(module, name)
    for name in message_type_names
  }

  fields_by_type = {
    name: {field.name: field.message_type.name if field.message_type else TYPE_ENUM_LKP[field.type].__name__ for field in message_type.DESCRIPTOR.fields}
    for name, message_type in message_types.items()
    if hasattr(message_type.DESCRIPTOR, 'fields')
  }

  rtn[filename] = fields_by_type

from pprint import pprint
pprint(rtn)