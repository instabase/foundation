"""Geometry."""

from dataclasses import dataclass
from itertools import chain
from typing import FrozenSet, Generator, Iterable, Optional

from .protos.python_out.geometry_pb2 import BBox as PBBBox, Interval as PBInterval, Point as PBPoint


@dataclass(frozen=True)
class Interval:
  """Represents a closed interval."""

  a: float
  b: float

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
      return Interval(0, 1)
    return Interval(
        (intersection.a - self.a) / self.length,
        (intersection.b - self.a) / self.length)

  def contains_percentage_of(self, other: 'Interval') -> float:
    """Returns the percentage of other contained in self."""
    if other.length == 0:
      return other.a in self
    intersection = Interval.intersection([self, other])
    return intersection.length / other.length if intersection else 0.0

  def eroded(self, amount: float) -> Optional['Interval']:
    result = Interval(self.a + amount, self.b - amount)
    return result if result.non_empty else None

  def expanded(self, amount: float) -> 'Interval':
    return Interval(self.a - amount, self.b + amount)

  @staticmethod
  def build(a: float, b: float) -> Optional['Interval']:
    return Interval(a, b) if a <= b else None

  @staticmethod
  def from_proto(proto: PBInterval) -> Optional['Interval']:
    return Interval.build(proto.a, proto.b)

  def to_proto(self) -> PBInterval:
    return PBInterval(a=self.a, b=self.b)

  @staticmethod
  def spanning(xs: Iterable[float]) -> 'Interval':
    xs = tuple(xs)
    if not xs:
      # Actually, the empty intersection is defined to be the ambient space --
      # in this case the real line -- so it's not really right to return `None`.
      raise RuntimeError('cannot take the spanning interval '
        'of an empty list of points')
    return Interval(min(xs), max(xs))

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


@dataclass(frozen=True)
class Point:
  x: float
  y: float

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

  @staticmethod
  def from_proto(proto: PBPoint) -> 'Point':
    return Point(proto.x, proto.y)

  def to_proto(self) -> PBPoint:
    return PBPoint(x=self.x, y=self.y)


@dataclass(frozen=True)
class BBox:
  ix: Interval
  iy: Interval

  @property
  def center(self) -> Point:
    return Point(self.ix.center, self.iy.center)

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
    return "BBox(ix={}, iy={})".format(self.ix, self.iy)

  def corners(self) -> Generator[Point, None, None]:
    yield Point(self.ix.a, self.iy.a)
    yield Point(self.ix.a, self.iy.b)
    yield Point(self.ix.b, self.iy.b)
    yield Point(self.ix.b, self.iy.a)

  def contains_bbox(self, other: 'BBox') -> bool:
    return self.ix.contains_interval(other.ix) and self.iy.contains_interval(
        other.iy)

  def intersects_bbox(self, other: 'BBox') -> bool:
    return self.ix.intersects_interval(
        other.ix) and self.iy.intersects_interval(other.iy)

  def percentages_overlapping(self, other: 'BBox') -> Optional['BBox']:
    """The percentage ranges of self which other overlaps.
    Example:
      box1 = BBox(Interval(1, 3), Interval(2, 6))
      box2 = BBox(Interval(0, 2), Interval(3, 5))
      result = BBox(Interval(0, 0.5), Interval(0.25, 0.75))
      assert box1.percentages_overlapping(box2) == result
    """
    return BBox.build(
        self.ix.percentages_overlapping(other.ix),
        self.iy.percentages_overlapping(other.iy))

  @staticmethod
  def build(ix: Optional[Interval], iy: Optional[Interval]) -> Optional['BBox']:
    return BBox(ix, iy) if ix is not None and iy is not None else None

  @staticmethod
  def from_proto(proto: PBBBox) -> Optional['BBox']:
    return BBox.build(
      Interval.from_proto(proto.ix),
      Interval.from_proto(proto.iy))

  def to_proto(self) -> PBBBox:
    return PBBBox(
      ix=PBInterval(a=self.ix.a, b=self.ix.b),
      iy=PBInterval(a=self.iy.a, b=self.iy.b))

  @staticmethod
  def spanning(ps: Iterable[Point]) -> Optional['BBox']:
    ps = tuple(ps)
    if not ps:
      return None
    ix = Interval(min(p.x for p in ps), max(p.x for p in ps))
    iy = Interval(min(p.y for p in ps), max(p.y for p in ps))
    return BBox(ix, iy)

  @staticmethod
  def intersection(bs: Iterable['BBox']) -> Optional['BBox']:
    bs = tuple(bs)
    if not bs:
      return None
    ix = Interval.intersection(b.ix for b in bs)
    iy = Interval.intersection(b.iy for b in bs)
    if ix is None or iy is None:
      return None
    return BBox(ix, iy)

  @staticmethod
  def distance(b1: 'BBox', b2: 'BBox') -> float:
    ix = Interval(min(b1.ix.a, b2.ix.a), max(b1.ix.b, b2.ix.b))
    iy = Interval(min(b1.iy.a, b2.iy.a), max(b1.iy.b, b2.iy.b))
    inner_width = max(0, ix.length - b1.ix.length - b2.ix.length)
    inner_height = max(0, iy.length - b1.iy.length - b2.iy.length)
    return sqrt(inner_width**2 + inner_height**2)
