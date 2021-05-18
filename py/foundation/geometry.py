
from typing import Optional, Iterable, Any, Mapping
from dataclasses import dataclass

from .proto import geometry_pb2




@dataclass
class BBox:
  _proto: geometry_pb2.BBox
  _reference_map: Mapping[str, Any]

  @property
  def rectangle(self) -> Rectangle:
    return self._proto.rectangle
  @property
  def page_index(self) -> int:
    return self._proto.page_index

  def as_proto(self) -> geometry_pb2.BBox:
    return self._proto

  @staticmethod
  def from_proto(proto: geometry_pb2.BBox, reference_map: Mapping[str, Any]):
    return BBox(proto, reference_map)



@dataclass
class Interval:
  _proto: geometry_pb2.Interval
  _reference_map: Mapping[str, Any]

  @property
  def a(self) -> float:
    return self._proto.a
  @property
  def b(self) -> float:
    return self._proto.b

  def as_proto(self) -> geometry_pb2.Interval:
    return self._proto

  @staticmethod
  def from_proto(proto: geometry_pb2.Interval, reference_map: Mapping[str, Any]):
    return Interval(proto, reference_map)



@dataclass
class Point:
  _proto: geometry_pb2.Point
  _reference_map: Mapping[str, Any]

  @property
  def x(self) -> float:
    return self._proto.x
  @property
  def y(self) -> float:
    return self._proto.y

  def as_proto(self) -> geometry_pb2.Point:
    return self._proto

  @staticmethod
  def from_proto(proto: geometry_pb2.Point, reference_map: Mapping[str, Any]):
    return Point(proto, reference_map)



@dataclass
class Rectangle:
  _proto: geometry_pb2.Rectangle
  _reference_map: Mapping[str, Any]

  @property
  def ix(self) -> Interval:
    return self._proto.ix
  @property
  def iy(self) -> Interval:
    return self._proto.iy

  def as_proto(self) -> geometry_pb2.Rectangle:
    return self._proto

  @staticmethod
  def from_proto(proto: geometry_pb2.Rectangle, reference_map: Mapping[str, Any]):
    return Rectangle(proto, reference_map)

