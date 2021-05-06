import * as BBox from './geometry/bbox';
import * as Text from './text';

export type t = {
  bbox: BBox.t;

  text: string;
  name_parts: Text.t[];
  likeness_score: number | undefined;
  type: 'PersonName';
};
