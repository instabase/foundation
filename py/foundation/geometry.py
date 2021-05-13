"""Geometry."""

from dataclasses import dataclass
from itertools import chain
from math import sqrt
from typing import Dict, FrozenSet, Generator, Iterable, Optional

from .proto import geometry_pb2

@dataclass
class Interval:
  """Represents a closed interval."""
  _proto: geometry_pb2.Interval

  @property
  def a(self) -> float:
    return self._proto.a
  
  @property
  def b(self) -> float:
    return self._proto.b

  @staticmethod
  def build(a: float, b: float) -> 'Interval':
    assert a <= b, "a must be less than or equal to b"
    return Interval(geometry_pb2.Interval(a=a, b=b))

  @property
  def length(self) -> float:
    return self.b - self.a

  @property
  def center(self) -> float:
    return (self.b + self.a) / 2

  @property
  def ends(self) -> FrozenSet[float]:
    return frozenset({self.a, self.b})

  @property
  def valid(self) -> bool:
    return self.a <= self.b

  @property
  def non_empty(self) -> bool:
    return self.length > 0

  def __contains__(self, x: float) -> bool:
    return self.a <= x <= self.b

  def contains_interval(self, other: 'Interval') -> bool:
    return self.a <= other.a <= other.b <= self.b

  def intersects_interval(self, other: 'Interval') -> bool:
    return not (self.b < other.a or other.b < self.a)

  def percentages_overlapping(self, other: 'Interval') -> Optional['Interval']:
    """The percentage ranges of self which other overlaps."""
    intersection = Interval.intersection([self, other])
    if intersection is None:
      return None
    if self.length == 0:
      return Interval.build(0, 1)
    return Interval.build(
        (intersection.a - self.a) / self.length,
        (intersection.b - self.a) / self.length)

  def contains_percentage_of(self, other: 'Interval') -> float:
    """Returns the percentage of other contained in self."""
    if other.length == 0:
      return other.a in self
    intersection = Interval.intersection([self, other])
    return intersection.length / other.length if intersection else 0.0

  def eroded(self, amount: float) -> Optional['Interval']:
    result = Interval.build(self.a + amount, self.b - amount)
    return result if result.non_empty else None

  def expanded(self, amount: float) -> 'Interval':
    return Interval.build(self.a - amount, self.b + amount)

  @staticmethod
  def spanning(xs: Iterable[float]) -> 'Interval':
    xs = tuple(xs)
    if not xs:
      # Actually, the empty intersection is defined to be the ambient space --
      # in this case the real line -- so it's not really right to return `None`.
      raise RuntimeError('cannot take the spanning interval '
        'of an empty list of points')
    return Interval.build(min(xs), max(xs))

  @staticmethod
  def spanning_intervals(Is: Iterable['Interval']) -> 'Interval':
    return Interval.spanning(chain.from_iterable(I.ends for I in Is))

  @staticmethod
  def intersection(Is: Iterable['Interval']) -> Optional['Interval']:
    Is = tuple(Is)
    if not Is:
      # Actually, the empty intersection is defined to be the ambient space --
      # in this case the real line -- so it's not really right to return `None`.
      raise RuntimeError('cannot take the intersection '
        'of an empty list of intervals')
    return Interval.build(max(I.a for I in Is), min(I.b for I in Is))

@dataclass
class Point:
  _proto: geometry_pb2.Point

  @property
  def x(self) -> float:
    return self._proto.x
  
  @property
  def y(self) -> float:
    return self._proto.y

  @staticmethod
  def build(self, x: float, y: float) -> 'Point':
    return Point(geometry_pb2.Point(x=x, y=y))

  def __str__(self) -> str:
    return "Point({}, {})".format(self.x, self.y)

  @staticmethod
  def distance(p1: 'Point', p2: 'Point') -> float:
    return sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

  @staticmethod
  def min_x(points: Iterable['Point']) -> float:
    return min(p.x for p in points)

  @staticmethod
  def min_y(points: Iterable['Point']) -> float:
    return min(p.y for p in points)

  @staticmethod
  def max_x(points: Iterable['Point']) -> float:
    return max(p.x for p in points)

  @staticmethod
  def max_y(points: Iterable['Point']) -> float:
    return max(p.y for p in points)

@dataclass
class Rectangle:
  _proto: geometry_pb2.Rectangle

  @property
  def ix(self) -> Interval:
    return Interval(self._proto.ix)

  @property
  def iy(self) -> Interval:
    return Interval(self._proto.iy)

  @property
  def center(self) -> Point:
    return Point.build(self.ix.center, self.iy.center, self.page_index)

  @property
  def width(self) -> float:
    return self.ix.length

  @property
  def height(self) -> float:
    return self.iy.length

  @property
  def area(self) -> float:
    return self.width * self.height

  @property
  def valid(self) -> bool:
    return self.ix.valid and self.iy.valid

  @property
  def non_empty(self) -> bool:
    return self.ix.non_empty and self.iy.non_empty

  def __contains__(self, p: Point) -> bool:
    return p.x in self.ix and p.y in self.iy

  def __str__(self) -> str:
    return "Rectangle(ix={}, iy={})".format(self.ix, self.iy)

  def corners(self) -> Generator[Point, None, None]:
    yield Point.build(self.ix.a, self.iy.a, self.page_index)
    yield Point.build(self.ix.a, self.iy.b, self.page_index)
    yield Point.build(self.ix.b, self.iy.b, self.page_index)
    yield Point.build(self.ix.b, self.iy.a, self.page_index)

  def contains_rectangle(self, other: 'Rectangle') -> bool:
    return self.ix.contains_interval(other.ix) and self.iy.contains_interval(
        other.iy)

  def intersects_rectangle(self, other: 'Rectangle') -> bool:
    return self.ix.intersects_interval(
        other.ix) and self.iy.intersects_interval(other.iy)

  def percentages_overlapping(self, other: 'Rectangle') -> Optional['Rectangle']:
    """The percentage ranges of self which other overlaps.
    Example:
      box1 = Rectangle.build(Interval.build(1, 3), Interval.build(2, 6))
      box2 = Rectangle.build(Interval.build(0, 2), Interval.build(3, 5))
      result = Rectangle.build(Interval.build(0, 0.5), Interval.build(0.25, 0.75))
      assert box1.percentages_overlapping(box2) == result
    """
    return Rectangle.build(
        self.ix.percentages_overlapping(other.ix),
        self.iy.percentages_overlapping(other.iy),
        self.page_index)

  @staticmethod
  def build(ix: Interval, iy: Interval) -> 'Rectangle':
    return Rectangle(geometry_pb2.Rectangle(ix._proto, iy._proto))

  @staticmethod
  def spanning(ps: Iterable[Point]) -> 'Rectangle':
    ps = tuple(ps)
    if not ps:
      raise ValueError('Cannot get spanning of an empty iterrable')
    ix = Interval.build(min(p.x for p in ps), max(p.x for p in ps))
    iy = Interval.build(min(p.y for p in ps), max(p.y for p in ps))
    return Rectangle.build(ix, iy)

  @staticmethod
  def intersection(bs: Iterable['Rectangle']) -> Optional['Rectangle']:
    bs = tuple(bs)
    if not bs:
      return None
    ix = Interval.intersection(b.ix for b in bs)
    iy = Interval.intersection(b.iy for b in bs)
    if ix is None or iy is None:
      return None
    return Rectangle.build(ix, iy)

  @staticmethod
  def union(bs: Iterable['Rectangle']) -> 'Rectangle':
    """Returns the smallest rectangle containing all bs (their union).

    Returns:
      None if bs is an empty iterator.
    """
    b = Rectangle.spanning(
      chain.from_iterable([b.corners() for b in bs]))
    return b

  @staticmethod
  def distance(b1: 'Rectangle', b2: 'Rectangle') -> float:
    ix = Interval.build(min(b1.ix.a, b2.ix.a), max(b1.ix.b, b2.ix.b))
    iy = Interval.build(min(b1.iy.a, b2.iy.a), max(b1.iy.b, b2.iy.b))
    inner_width = max(0, ix.length - b1.ix.length - b2.ix.length)
    inner_height = max(0, iy.length - b1.iy.length - b2.iy.length)
    return sqrt(inner_width**2 + inner_height**2)

@dataclass
class BBox:
  _proto: geometry_pb2.BBox

  @property
  def rectangle(self) -> Rectangle:
    return Rectangle(self._proto.rectangle)

  @property
  def page_index(self) -> int:
    return self._proto.page_index