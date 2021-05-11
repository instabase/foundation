import * as BBox from '../geometry/bbox';

export type t = {
  bbox: BBox.t;
  text: string;
};

export function isValid(ws: t): boolean {
  return ws.text.trim() === '';
}
