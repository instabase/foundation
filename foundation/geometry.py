"""Geometry."""

from dataclasses import dataclass
from itertools import chain
from typing import FrozenSet, Generator, Iterable, Optional

from .python_out.geometry_pb2 import BBox, Interval, Point


# Point(x: float, y: float)

def _point_string(self) -> str:
  return "Point({}, {})".format(self.x, self.y)

@staticmethod
def _point_distance(p1: 'Point', p2: 'Point') -> float:
  return sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

@staticmethod
def _point_min_x(points: Iterable['Point']) -> float:
  return min(p.x for p in points)

@staticmethod
def _point_min_y(points: Iterable['Point']) -> float:
  return min(p.y for p in points)

@staticmethod
def _point_max_x(points: Iterable['Point']) -> float:
  return max(p.x for p in points)

@staticmethod
def _point_max_y(points: Iterable['Point']) -> float:
  return max(p.y for p in points)

Point.__str__ = _point_string
Point.distance = _point_distance
Point.min_x = _point_min_x
Point.min_y = _point_min_y
Point.max_x = _point_max_x
Point.max_y = _point_max_y


# Interval(a: float, b: float)

@property
def _interval_length(self) -> float:
  return self.b - self.a

@property
def _interval_center(self) -> float:
  return (self.b + self.a) / 2

@property
def _interval_ends(self) -> FrozenSet[float]:
  return frozenset({self.a, self.b})

@property
def _interval_valid(self) -> bool:
  return self.a <= self.b

@property
def _interval_non_empty(self) -> bool:
  return self.length > 0

def _interval_contains(self, x: float) -> bool:
  return self.a <= x <= self.b

def _interval_contains_interval(self, other: 'Interval') -> bool:
  return self.a <= other.a <= other.b <= self.b

def _interval_intersects_interval(self, other: 'Interval') -> bool:
  return not (self.b < other.a or other.b < self.a)

def _interval_percentages_overlapping(self, other: 'Interval') -> Optional['Interval']:
  """The percentage ranges of self which other overlaps."""
  intersection = Interval.intersection([self, other])
  if intersection is None:
    return None
  if self.length == 0:
    return Interval(a=0, b=1)
  return Interval(
      a=(intersection.a - self.a) / self.length,
      b=(intersection.b - self.a) / self.length)

def _interval_contains_percentage_of(self, other: 'Interval') -> float:
  """Returns the percentage of other contained in self."""
  if other.length == 0:
    return other.a in self
  intersection = Interval.intersection([self, other])
  return intersection.length / other.length if intersection else 0.0

def _interval_eroded(self, amount: float) -> Optional['Interval']:
  result = Interval(a=self.a + amount, b=self.b - amount)
  return result if result.non_empty else None

def _interval_expanded(self, amount: float) -> 'Interval':
  return Interval(a=self.a - amount, b=self.b + amount)

@staticmethod
def _interval_build(a: float, b: float) -> Optional['Interval']:
  return Interval(a=a, b=b) if a <= b else None

@staticmethod
def _interval_spanning(xs: Iterable[float]) -> 'Interval':
  xs = tuple(xs)
  if not xs:
    # Actually, the empty intersection is defined to be the ambient space --
    # in this case the real line -- so it's not really right to return `None`.
    raise RuntimeError('cannot take the spanning interval '
      'of an empty list of points')
  return Interval(a=min(xs), b=max(xs))

@staticmethod
def _interval_spanning_intervals(Is: Iterable['Interval']) -> 'Interval':
  return Interval.spanning(chain.from_iterable(I.ends for I in Is))

@staticmethod
def _interval_intersection(Is: Iterable['Interval']) -> Optional['Interval']:
  Is = tuple(Is)
  if not Is:
    # Actually, the empty intersection is defined to be the ambient space --
    # in this case the real line -- so it's not really right to return `None`.
    raise RuntimeError('cannot take the intersection '
      'of an empty list of intervals')
  return Interval.build(max(I.a for I in Is), min(I.b for I in Is))

Interval.length = _interval_length
Interval.center = _interval_center
Interval.ends = _interval_ends
Interval.valid = _interval_valid
Interval.non_empty = _interval_non_empty
Interval.__contains__ = _interval_contains
Interval.contains_interval = _interval_contains_interval
Interval.intersects_interval = _interval_intersects_interval
Interval.percentages_overlapping = _interval_percentages_overlapping
Interval.contains_percentage_of = _interval_contains_percentage_of
Interval.eroded = _interval_eroded
Interval.expanded = _interval_expanded
Interval.build = _interval_build
Interval.spanning = _interval_spanning
Interval.spanning_intervals = _interval_spanning_intervals
Interval.intersection = _interval_intersection


# BBox(ix: Interval, iy: Interval)

@property
def _bbox_center(self) -> Point:
  return Point(self.ix.center, self.iy.center)

@property
def _bbox_width(self) -> float:
  return self.ix.length

@property
def _bbox_height(self) -> float:
  return self.iy.length

@property
def _bbox_area(self) -> float:
  return self.width * self.height

@property
def _bbox_valid(self) -> bool:
  return self.ix.valid and self.iy.valid

@property
def _bbox_non_empty(self) -> bool:
  return self.ix.non_empty and self.iy.non_empty

def _bbox_contains(self, p: Point) -> bool:
  return p.x in self.ix and p.y in self.iy

def _bbox_string(self) -> str:
  return "BBox(ix={}, iy={})".format(self.ix, self.iy)

def _bbox_corners(self) -> Generator[Point, None, None]:
  yield Point(x=self.ix.a, y=self.iy.a)
  yield Point(x=self.ix.a, y=self.iy.b)
  yield Point(x=self.ix.b, y=self.iy.b)
  yield Point(x=self.ix.b, y=self.iy.a)

def _bbox_contains_bbox(self, other: 'BBox') -> bool:
  return self.ix.contains_interval(other.ix) and self.iy.contains_interval(
      other.iy)

def _bbox_intersects_bbox(self, other: 'BBox') -> bool:
  return self.ix.intersects_interval(
      other.ix) and self.iy.intersects_interval(other.iy)

def _bbox_percentages_overlapping(self, other: 'BBox') -> Optional['BBox']:
  """The percentage ranges of self which other overlaps.

  Example:
    box1 = BBox(ix=Interval(a=1, b=3), iy=Interval(a=2, b=6))
    box2 = BBox(ix=Interval(0, 2), iy=Interval(a=3, b=5))
    result = BBox(ix=Interval(a=0, b=0.5), iy=Interval(a=0.25, b=0.75))
    assert box1.percentages_overlapping(box2) == result
  """
  return BBox.build(
      self.ix.percentages_overlapping(other.ix),
      self.iy.percentages_overlapping(other.iy))

@staticmethod
def _bbox_build(ix: Optional[Interval], iy: Optional[Interval]) -> Optional['BBox']:
  return BBox(ix=ix, iy=iy) if ix is not None and iy is not None else None

@staticmethod
def _bbox_spanning(ps: Iterable[Point]) -> Optional['BBox']:
  ps = tuple(ps)
  if not ps:
    return None
  ix = Interval(a=min(p.x for p in ps), b=max(p.x for p in ps))
  iy = Interval(a=min(p.y for p in ps), b=max(p.y for p in ps))
  return BBox(ix=ix, iy=iy)

@staticmethod
def _bbox_intersection(bs: Iterable['BBox']) -> Optional['BBox']:
  bs = tuple(bs)
  if not bs:
    return None
  ix = Interval.intersection(b.ix for b in bs)
  iy = Interval.intersection(b.iy for b in bs)
  if ix is None or iy is None:
    return None
  return BBox(ix=ix, iy=iy)

@staticmethod
def _bbox_distance(b1: 'BBox', b2: 'BBox') -> float:
  ix = Interval(a=min(b1.ix.a, b2.ix.a), b=max(b1.ix.b, b2.ix.b))
  iy = Interval(a=min(b1.iy.a, b2.iy.a), b=max(b1.iy.b, b2.iy.b))
  inner_width = max(0, ix.length - b1.ix.length - b2.ix.length)
  inner_height = max(0, iy.length - b1.iy.length - b2.iy.length)
  return sqrt(inner_width**2 + inner_height**2)

BBox.center = _bbox_center
BBox.width = _bbox_width
BBox.height = _bbox_height
BBox.area = _bbox_area
BBox.valid = _bbox_valid
BBox.non_empty = _bbox_non_empty
BBox.__contains__ = _bbox_contains
BBox.__str__ = _bbox_string
BBox.corners = _bbox_corners
BBox.contains_bbox = _bbox_contains_bbox
BBox.intersects_bbox = _bbox_intersects_bbox
BBox.percentages_overlapping = _bbox_percentages_overlapping
BBox.build = _bbox_build
BBox.spanning = _bbox_spanning
BBox.intersection = _bbox_intersection
BBox.distance = _bbox_distance
