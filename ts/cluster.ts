import * as BBox from './bbox';
import * as Text from './text';

export type t = {
  bbox: BBox.t;

  text: string;
  lines: Text.t[];
  label: string | undefined;
  type: 'Cluster';
};
