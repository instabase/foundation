
from typing import Optional, Iterable, Any, Mapping, Dict
from dataclasses import dataclass
import itertools

from foundation.proto import geometry_pb2




@dataclass
class BBox:
  _proto: geometry_pb2.BBox
  _reference_map: Dict[str, Any]

  @property
  def rectangle(self) -> 'Rectangle':
    return Rectangle(self._proto.rectangle, self._reference_map)
  @rectangle.setter
  def rectangle(self, new_obj: 'Rectangle') -> None:
    self._proto.rectangle.ix.a = new_obj.ix.a
    self._proto.rectangle.ix.b = new_obj.ix.b
    self._proto.rectangle.iy.a = new_obj.iy.a
    self._proto.rectangle.iy.b = new_obj.iy.b
    self._reference_map.update(new_obj._reference_map)
  @property
  def page_index(self) -> int:
    return self._proto.page_index
  @page_index.setter
  def page_index(self, new_obj: int) -> None:
    self._proto.page_index = new_obj
    

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from []

  def as_proto(self) -> geometry_pb2.BBox:
    return self._proto

  @staticmethod
  def from_proto(proto: geometry_pb2.BBox, reference_map: Dict[str, Any]) -> 'BBox':
    return BBox(proto, reference_map)



@dataclass
class Interval:
  _proto: geometry_pb2.Interval
  _reference_map: Dict[str, Any]

  @property
  def a(self) -> 'float':
    return self._proto.a
  @a.setter
  def a(self, new_obj: 'float') -> None:
    self._proto.a = new_obj
    
  @property
  def b(self) -> 'float':
    return self._proto.b
  @b.setter
  def b(self, new_obj: 'float') -> None:
    self._proto.b = new_obj
    

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from []

  def as_proto(self) -> geometry_pb2.Interval:
    return self._proto

  @staticmethod
  def from_proto(proto: geometry_pb2.Interval, reference_map: Dict[str, Any]) -> 'Interval':
    return Interval(proto, reference_map)



@dataclass
class Point:
  _proto: geometry_pb2.Point
  _reference_map: Dict[str, Any]

  @property
  def x(self) -> 'float':
    return self._proto.x
  @x.setter
  def x(self, new_obj: 'float') -> None:
    self._proto.x = new_obj
    
  @property
  def y(self) -> 'float':
    return self._proto.y
  @y.setter
  def y(self, new_obj: 'float') -> None:
    self._proto.y = new_obj
    

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from []

  def as_proto(self) -> geometry_pb2.Point:
    return self._proto

  @staticmethod
  def from_proto(proto: geometry_pb2.Point, reference_map: Dict[str, Any]) -> 'Point':
    return Point(proto, reference_map)



@dataclass
class Rectangle:
  _proto: geometry_pb2.Rectangle
  _reference_map: Dict[str, Any]

  @property
  def ix(self) -> 'Interval':
    return Interval(self._proto.ix, self._reference_map)
  @ix.setter
  def ix(self, new_obj: 'Interval') -> None:
    self._proto.ix = new_obj.as_proto()
    self._reference_map.update(new_obj._reference_map)
  @property
  def iy(self) -> 'Interval':
    return Interval(self._proto.iy, self._reference_map)
  @iy.setter
  def iy(self, new_obj: 'Interval') -> None:
    self._proto.iy = new_obj.as_proto()
    self._reference_map.update(new_obj._reference_map)

  def _get_dependent_ids(self) -> Iterable[str]:
    yield from []

  def as_proto(self) -> geometry_pb2.Rectangle:
    return self._proto

  @staticmethod
  def from_proto(proto: geometry_pb2.Rectangle, reference_map: Dict[str, Any]) -> 'Rectangle':
    return Rectangle(proto, reference_map)

