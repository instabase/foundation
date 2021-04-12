import * as BBox from './bbox';
import * as Text from './text';

export type t = {
  bbox: BBox.t;

  text: string;
  lines: Text.t[];
  address_parts: string[][];
  likeness_score: number | undefined;
  type: 'Address';
};
