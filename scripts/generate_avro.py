import json
from typing import Type, Dict, Optional, Tuple, List
from collections.abc import Iterable
import inspect
import typing
from pprint import pprint

from foundation.entity import Entity
from foundation.meta import foundation_types, FoundationType
from foundation.typing_utils import assert_exhaustive

def cumulative_annots(cls: Type) -> Optional[Dict[str, Type]]:
  if inspect.isabstract(cls):
    return None
  classes = type.mro(cls)[:-2][::-1]
  attributes = {k:v for c in classes for k,v in c.__annotations__.items()}
  return attributes

def annot_to_type(annot: Type) -> str:
  if annot is str:
    return "string"
  if annot is int:
    return "int"
  if annot is float:
    return "double"
  if annot is bool:
    return "boolean"
  if annot is bytes:
    return "bytes"
  
  if inspect.isclass(annot):
    if issubclass(annot, Entity):
      return "string" # keys are strings
    else:
      return get_type_def(annot)

  origin = annot.__origin__
  if issubclass(origin, Iterable):
    # TODO(Erick): need to get element type too
    annot_args = annot.__args__
    if len(annot_args) == 1:
      # this is a list, set, etc.
      inner = annot_to_type(annot_args[0])
      return {
        "type": "array",
        "items": inner,
        "default": []
      }
    elif len(annot_args) == 2:
      arg0 = annot_args[0]
      arg1 = annot_args[1]
      if arg1 == ...:
        # this is a tuple
        assert origin is tuple

        inner = annot_to_type(arg0)
        return {
          "type": "array",
          "items": inner,
          "default": []
        }
      else:
        # this is a dict
        assert origin is dict
        innerkey = annot_to_type(arg0)
        assert innerkey == "string"
        innerval = annot_to_type(arg1)
        return {
          "type": "map",
          "values": innerval,
          "default": {}
        }
    raise ValueError(f"Invalid attribute args in: {annot}")

  raise ValueError(f"Invalid attribute type: {annot}")

def get_type_def(cls: Type) -> Optional[Dict[str, str]]:
  annots = cumulative_annots(cls)
  if annots is None:
    return None
  rtn = {
    "type": "record",
    "name": cls.__name__,
    "fields": [
      {
        "name": field,
        "type": annot_to_type(annot),
      } 
      for field, annot in annots.items()
    ],
  }
  return rtn

def get_schema() -> Dict:
  return {
    "namespace": "foundation",
    "type": "record",
    "name": "RecordContext",
    "fields": [
      {
        "name": "datastore",
        "type": {
          "name": "datastore",
          "type": "map",
          "values": [
            get_type_def(t) for t in foundation_types.values()
          ]
        }
      },
      {
        "name": "pages",
        "type": "array",
        "values": "string",
      }
    ]
  }

if __name__ == "__main__":
  # print(json.dumps(get_schema()))
  pprint(get_schema())