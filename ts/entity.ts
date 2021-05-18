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

export function heuristicDefaultType(field: string): Type {
  if (field.endsWith('date')) {
    return 'Date';
  } else if (field.endsWith('address')) {
    // return 'Address'; // Address finding is janky ATM.
    return 'Text';
  } else if (field.endsWith('name')) {
    // return 'PersonName'; // Person name finding is janky ATM.
    return 'Text';
  } else if (field.endsWith('amount')) {
    return 'DollarAmount';
  } else {
    return 'Text';
  }
}

export function heuristicDefaultIsLabel(field: string): boolean {
  return heuristicDefaultType(field) == 'Text' &&
         field.includes('label');
}
