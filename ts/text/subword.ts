import * as BBox from '../geometry/bbox';

export type t = {
  bbox: BBox.t;
  text: string;
  start: number;
  end: number;
};

export function getText(sw: t) {
  return sw.text.slice(sw.start, sw.end);
}
