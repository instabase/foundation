from foundation.proto import geometry_pb2, entity_pb2, extraction_pb2, targets_pb2, record_pb2, comparison_pb2, serialization_pb2
from typing import Set


modules = {
  "geometry": geometry_pb2,
  "entity": entity_pb2,
  "extraction": extraction_pb2,
  "targets": targets_pb2,
  "record": record_pb2,
  "comparison": comparison_pb2,
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

INHERITANCE = {
  "Entity": ["Page", "SubWord", "FillerString", "Word", "Text"],
  "Text": ["Date", "CurrencyAmount", "PersonName", "Address"]
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

filenames_by_type = {
  name: filename
  for filename, fields_by_type in rtn.items()
  for name in fields_by_type
}
filenames_by_type.update({
  t: None for t in ["int", "str", "float", "bool", "bytes", "Mapping[str, Any]"]
})

def snakecase_to_titlecase(s):
  return s.replace("_", " ").title().replace(" ", "")


SPECIAL_CASES = {
  "Children": "Entity",
  "Collection": "Entity",
  "Root": "SerializedTypeOneOf",
  "DataEntry": "Mapping[str, Any]"
}

def get_field_type(s):
  guess_field_type = snakecase_to_titlecase(s)
  return SPECIAL_CASES.get(guess_field_type, guess_field_type)

# def attribute_definition(fieldname: str, fieldtype: str):
#   if fieldname.endswith("_id"):
#     id_free_field_name = fieldname[:-3]
#     field_type = get_field_type(id_free_field_name)
#     return f"  _{id_free_field_name}: {field_type}"
#   elif fieldname.endswith("_ids"):
#     id_free_field_name = fieldname[:-4]
#     field_type = get_field_type(id_free_field_name)
#     return f"  _{id_free_field_name}s: Tuple[{field_type}]"
#   else:
#     return f"  _{fieldname}: {fieldtype}"


def property_definition(fieldname: str, fieldtype: str, mutable_imports: Set[str], current_module: str):
  if fieldname.endswith("_id"):
    id_free_field_name = fieldname[:-3]
    field_type = get_field_type(id_free_field_name)
    try:
      import_from = filenames_by_type[field_type]
      if import_from != current_module and import_from is not None:
        mutable_imports.add(f"from foundation.{import_from} import {field_type}")
      else:
        field_type = f"'{field_type}'"
    except KeyError as e:
      print(fieldname, fieldtype)
      raise(e)
    return f'''  @property
  def {id_free_field_name}(self) -> {field_type}:
    return self._reference_map[self._proto.{fieldname}]
'''
  elif fieldname.endswith("_ids"):
    id_free_field_name = fieldname[:-4]
    field_type = get_field_type(id_free_field_name)
    try:
      import_from = filenames_by_type[field_type]
    except KeyError as e:
      print(fieldname, fieldtype)
      raise(e)
    if import_from != current_module and import_from is not None:
      mutable_imports.add(f"from foundation.{import_from} import {field_type}")
    else:
      field_type = f"'{field_type}'"
    return f'''  @property
  def {id_free_field_name}s(self) -> Iterable[{field_type}]:
    yield from (self._reference_map[i] for i in self._proto.{fieldname})
'''
  else:
    field_type = SPECIAL_CASES.get(fieldtype, fieldtype)
    try:
      import_from = filenames_by_type[field_type]
      return_line = f"self._proto.{fieldname}"
      if import_from is not None:
        return_line = f"{field_type}(self._proto.{fieldname}, self._reference_map)"
      if import_from != current_module and import_from is not None:
        mutable_imports.add(f"from foundation.{import_from} import {field_type}")
      else:
        field_type = f"'{field_type}'"
    except KeyError as e:
      print(fieldname, fieldtype)
      raise(e)

    return f'''  @property
  def {fieldname}(self) -> {field_type}:
    return {return_line}'''

for filename, module in rtn.items():
  classes = []
  imports = set()
  for name, fields in module.items():
    # field_strs = [
    #   attribute_definition(fieldname, fieldtype)
    #   for fieldname, fieldtype in fields.items()
    # ]
    method_strs = [
      property_definition(fieldname, fieldtype, imports, filename)
      for fieldname, fieldtype in fields.items()
    ]
    print(imports)
    # fields_str = '\n'.join(field_strs)
    methods_str = '\n'.join(method_strs)
    classes.append(\
f'''
@dataclass
class {name}:
  _proto: {filename}_pb2.{name}
  _reference_map: Mapping[str, Any]

{methods_str}

  def as_proto(self) -> {filename}_pb2.{name}:
    return self._proto

  @staticmethod
  def from_proto(proto: {filename}_pb2.{name}, reference_map: Mapping[str, Any]) -> '{name}':
    return {name}(proto, reference_map)
''')
  class_str = '\n\n'.join(classes)
  imports_str = '\n'.join(imports)
  out_str = \
f'''
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from foundation.proto import {filename}_pb2

{imports_str}

{class_str}
'''
  with open(f'./py/foundation/{filename}.py', 'w') as f:
    f.write(out_str)