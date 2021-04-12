import * as BBox from './bbox';
import * as Text from './text';

export type t = {
  bbox: BBox.t;

  text: string;
  words: Text.t[];
  likeness_score: number | undefined;
  type: 'DollarAmount';
};
