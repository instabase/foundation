import * as BBox from './bbox';
import * as Word from './word';

export type t = {
  bbox: BBox.t;

  text: string;
  words: Word.t[];
  likeness_score: number | undefined;
  type: 'Date';
};
