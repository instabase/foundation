export type t = {
  x: number;
  y: number;
};

export function distance(p1: t, p2: t): number {
  return Math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2);
}

export function minX(points: Array<t>): number {
  const xVals = points.map((p) => p.x);
  return Math.min(...xVals); 
}

export function minY(points: Array<t>): number {
  const yVals = points.map((p) => p.y);
  return Math.min(...yVals); 
}

export function maxX(points: Array<t>): number {
  const xVals = points.map((p) => p.x);
  return Math.max(...xVals); 
}

export function maxY(points: Array<t>): number {
  const yVals = points.map((p) => p.y);
  return Math.max(...yVals); 
}
