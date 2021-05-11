import * as BBox from './geometry/bbox';
import * as Word from './text/word';
import * as Whitespace from './text/whitespace';

export type t = {
  bbox: BBox.t;

  text: string;
  words: Array<Word.t | Whitespace.t>;
  likeness_score: number | undefined;
  year: number | undefined;
  month: number | undefined;
  day: number | undefined;
  type: 'Date'
};
