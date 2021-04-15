import * as Address from './address';
import * as Cluster from './cluster';
import * as Date from './date';
import * as DollarAmount from './dollarAmount';
import * as PersonName from './personName';
import * as Text from './text';

export const Types = [
  'Address',
  'Cluster',
  'Date',
  'DollarAmount',
  'PersonName',
  'Text',
] as const;

export type t =
  | Address.t
  | Cluster.t
  | Date.t
  | DollarAmount.t
  | PersonName.t
  | Text.t
;

export type Type = typeof Types[number];

export const DefaultType: Type = 'Text';

export function text(entity: t): string | undefined {
  return entity.text;
}
