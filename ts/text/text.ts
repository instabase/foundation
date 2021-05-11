import * as BBox from '../geometry/bbox';
import * as Word from './word';
import * as Whitespace from './whitespace';

export type t = {
  bbox: BBox.t;

  text: string;
  words: Array<Word.t | Whitespace.t>;
  maximality_score: number | undefined;
  ocr_score: number | undefined;
  type: 'Text';
};

export function text(text: t): string {
  const texts = text.words.map((w) => w.text);
  return texts.join('');
}
