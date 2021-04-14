import * as Interval from './interval';
import * as Point from './point';
import {Nonempty} from './util/types';

export type t = {
  ix: Interval.t;
  iy: Interval.t;
};

export function width(bbox: t): number {
  return (Interval.length(bbox.ix));
}

export function height(bbox: t): number {
  return (Interval.length(bbox.iy));
}

export function upperLeft(bbox: t) {
  return {x: bbox.ix.a, y: bbox.iy.a};
}

export function upperRight(bbox: t) {
  return {x: bbox.ix.b, y: bbox.iy.a};
}

export function lowerRight(bbox: t) {
  return {x: bbox.ix.b, y: bbox.iy.b};
}

export function lowerLeft(bbox: t) {
  return {x: bbox.ix.a, y: bbox.iy.b};
}

export function leftHalf({ix, iy}: t): t {
  return {ix: Interval.lowerHalf(ix), iy};
}

export function rightHalf({ix, iy}: t): t {
  return {ix: Interval.upperHalf(ix), iy};
}

export function lowerHalf({ix, iy}: t): t {
  return {ix, iy: Interval.upperHalf(iy)};
}

export function upperHalf({ix, iy}: t): t {
  return {ix, iy: Interval.lowerHalf(iy)};
}

export function distanceFromLeft(p: Point.t, bbox: t) {
  return (p.x - bbox.ix.a);
}

export function distanceFromRight(p: Point.t, bbox: t) {
  return (bbox.ix.b - p.x);
}

export function distanceFromTop(p: Point.t, bbox: t) {
  return (p.y - bbox.iy.a);
}

export function distanceFromBottom(p: Point.t, bbox: t) {
  return (bbox.iy.b - p.y);
}

export function percentageFromLeft(p: Point.t, bbox: t) {
  return (distanceFromLeft(p, bbox) / width(bbox));
}

export function percentageFromRight(p: Point.t, bbox: t) {
  return (distanceFromRight(p, bbox) / width(bbox));
}

export function percentageFromTop(p: Point.t, bbox: t) {
  return (distanceFromTop(p, bbox) / height(bbox));
}

export function percentageFromBottom(p: Point.t, bbox: t) {
  return (distanceFromBottom(p, bbox) / height(bbox));
}

export function percentageBasedPositionIn(bbox: t, other: t): t {
  return {
    ix: {
      a: percentageFromLeft(upperLeft(bbox), other),
      b: percentageFromLeft(upperRight(bbox), other),
    },
    iy: {
      a: percentageFromTop(upperLeft(bbox), other),
      b: percentageFromTop(lowerLeft(bbox), other),
    },
  }
}

export function containing(ps: Nonempty<Point.t[]>): t {
  return {
    ix: {
      a: Math.min(...ps.map(p => p.x)),
      b: Math.max(...ps.map(p => p.x)),
    },
    iy: {
      a: Math.min(...ps.map(p => p.y)),
      b: Math.max(...ps.map(p => p.y)),
    },
  };
}

export function contains(bigger: t, smaller: t): boolean {
  return Interval.contains(bigger.ix, smaller.ix) &&
         Interval.contains(bigger.iy, smaller.iy);
}

export function intersect(bbox1: t, bbox2: t): boolean {
  return Interval.intersect(bbox1.ix, bbox2.ix) &&
         Interval.intersect(bbox1.iy, bbox2.iy);
}

export function areEqual(bbox1: t, bbox2: t): boolean {
  return bbox1.ix.a == bbox2.ix.a &&
          bbox1.ix.b == bbox2.ix.b &&
          bbox1.iy.a == bbox2.iy.a &&
          bbox1.iy.b == bbox2.iy.b
}

export function splitSquareLike(bbox: t): [t, t] {
  if (width(bbox) > height(bbox)) {
    return [leftHalf(bbox), rightHalf(bbox)];
  } else {
    return [upperHalf(bbox), lowerHalf(bbox)];
  }
}
