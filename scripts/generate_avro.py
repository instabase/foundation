from typing import Type, Dict, Optional, Tuple, List
from collections.abc import Iterable
import inspect

from foundation.entity import Entity
from foundation.meta import foundation_types, FoundationType
from foundation.typing_utils import assert_exhaustive

def cumulative_annots(cls: Type) -> Optional[Dict[str, Type]]:
  if inspect.isabstract(cls):
    return None
  classes = type.mro(cls)[:-1][::-1]
  attributes = {k:v for c in classes for k,v in c.__annotations__.items()}
  return attributes

TYPE_LOOKUP = [
  (str, "string"),
  (int, "int"),
  (float, "float"),
  (Iterable, "list"),
  (Entity, "str")
]
def annot_to_type(annot: Type) -> str:
  if annot is str:
    return "string"
  if annot is int:
    return "int"
  if annot is float:
    return "float"
  if type(annot) is FoundationType:
    return annot.__name__
  return "list"

def get_type_def(cls: Type) -> Optional[Dict[str, str]]:
  annots = cumulative_annots(cls)
  if annots is None:
    return None
  return {field: annot_to_type(annot) for field, annot in annots.items()}

if __name__ == "__main__":
  for k,t in foundation_types.items():
    o = get_type_def(t)
    if o is not None:
      print(k)
      print(o)