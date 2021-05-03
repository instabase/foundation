from typing import Dict, Set, Type, Any, cast, Iterable, Union
from typing_extensions import Protocol

import inspect

from abc import ABC, abstractmethod

foundation_types: Dict[str, Type['FoundationType']] = {}

PRIMITIVES = [str, int, float, bool, bytes]
class FoundationType(Protocol):
  @property
  @abstractmethod
  def type(self) -> str: ...

  def __init_subclass__(cls) -> None:
    foundation_types[cls.__name__] = cls

  def as_dict(self) -> Dict[str, Any]:
    return as_dict_helper(self, True)



def as_dict_helper(val: FoundationType, is_root: bool) -> Dict[str, Any]:
  my_type_name = 'InMemory' + val.type
  my_type = foundation_types.get(my_type_name) or foundation_types[val.type]
  rtn: Dict[str, Any] = {}
  for field_name, annot_type in my_type.__annotations__.items():
    rtn[field_name.strip('_')] = serialize_field(annot_type, getattr(val, field_name), is_root)
  rtn['type'] = val.type
  return rtn

def serialize_annot_class(val: Any, is_root: bool) -> Any:
  annot = type(val)
  if annot in foundation_types.values():
    if not is_root and hasattr(val, 'id'):
      return {
        'type': 'id',
        'value': val.id
      }
    else:
      return as_dict_helper(val, False)
  else:
    raise ValueError(f"Invalid annotation {annot}")

def serialize_field(annot: Type, val: Any, is_root: bool) -> Any:

  # id and map are special types

  if annot in PRIMITIVES:
    return val
  if inspect.isclass(annot):
    return serialize_annot_class(val, is_root)

  origin = annot.__origin__
  if origin is Union:
    return serialize_annot_class(val, is_root)
  if issubclass(origin, Iterable):
    annot_args = annot.__args__
    if len(annot_args) == 1:
      # this is a list, set, etc.
      return [serialize_field(annot_args[0], i, False) for i in val]
    elif len(annot_args) == 2:
      arg0 = annot_args[0]
      arg1 = annot_args[1]
      if arg1 == ...:
        # this is a tuple
        assert origin is tuple
        return [serialize_field(arg0, i, False) for i in val]
      else:
        # this is a dict
        assert origin is dict
        assert arg0 is str
        return {
          'type': 'map',
          'value': {
            k: serialize_field(arg1, v, False)
            for k, v in val.items()
          }
        }
    raise ValueError(f"Invalid attribute args in: {annot}")

  raise ValueError(f"Invalid attribute type: {annot}")

# def deserialize_field_helper(annot: Type, field: Any) -> Any:
#   if annot in PRIMITIVES:
#     return annot(field)
  
#   assert type(field) is dict
#   entity_type = field['type']
#   if entity_type == 'id':
#     return foundation_types['EntityReference'](field['value'])
#   if entity_type == 'map'
  

# def deserialize_field(entity_dict: Dict) -> Any:
#   entity_type = entity_dict['type']
  
  
#   cls = foundation_types.get('InMemory' + entity_type) or foundation_types[entity_type]
#   annots = cls.__annotations__
#   kwargs = {
#     field_name: deserialize_field_helper(annot, entity_dict[field_name.strip('_')])
#     for field_name, annot in annots.items()
#   }
#   return cls(**kwargs)

# def deserialize_entities(entity_dicts: Dict[str, Dict[str, Any]], existing_entities: Dict[str, Any]=None) -> Dict[str, Any]:
#   entities: Dict[str, Any] = {}
#   if existing_entities:
#     entities.update(existing_entities)
  
#   entities_to_revisit: Set[str] = {}
#   for id, entity_dict in entity_dicts.items():
#     entity_type = entity_dict['type']
#     entities[id] = ...



  # @staticmethod
  # @abstractmethod
  # def from_dict(type_as_dict: Dict) -> 'FoundationType': ...

# class DataGetter(ABC):
#   @abstractmethod
#   def get(self, key: str) -> Any:
#     ...
# class FoundationType(ABC):
#   """
#   A superclass that registers foundation types
#   (including non-entity types) that might show up
#   in the "data" k/v store
#   """
#   id: str
#   _data: DataGetter

#   def __init_subclass__(cls) -> None:
#     foundation_types[cls.__name__] = cls
