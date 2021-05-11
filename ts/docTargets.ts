import * as TargetAssignment from './targetAssignment';
import * as TargetValue from './targetValue';
import memo from './util/memo';

export type t = {
  doc_name: string;
  assignments: TargetAssignment.t[];
  doc_tags: string[];
  notes: string | undefined;
};

export function build(docName: string): t {
  return {
    doc_name: docName,
    assignments: [],
    doc_tags: [],
    notes: undefined,
  };
}

export function isEmpty(docTargets: t): boolean {
  return fields(docTargets).length == 0;
}

export const fields = memo(
  function(docTargets: t): string[] {
    return docTargets.assignments.map(
      ({field, value}) => field
    );
  }
);

export function hasValue(docTargets: t, field: string): boolean {
  return asDict(docTargets)[field] != undefined;
}

export function hasAllValues(docTargets: t, fields: string[]): boolean {
  return fields.every(field => hasValue(docTargets, field));
}

export function hasNonNullValue(docTargets: t, field: string): boolean {
  const value = asDict(docTargets)[field];
  return value != undefined && TargetValue.isNonNull(value);
}

export function hasAllNonNullValues(docTargets: t, fields: string[]): boolean {
  return fields.every(field => hasNonNullValue(docTargets, field));
}

export function hasPositionedValue(docTargets: t, field: string): boolean {
  const value = asDict(docTargets)[field];
  return value != undefined && TargetValue.isPositioned(value);
}

export function hasAllPositionedValues(docTargets: t, fields: string[]): boolean {
  return fields.every(field => hasPositionedValue(docTargets, field));
}

export const asDict = memo(
  function(
    docTargets: t):
      Partial<Record<string, TargetValue.t>>
  {
    const result: Partial<Record<string, TargetValue.t>> = {};
    docTargets.assignments.forEach(
      ({field, value}) => result[field] = value
    );
    return result;
  }
);

export const value = memo(
  function(
    docTargets: t,
    field: string):
      TargetValue.t | undefined
  {
    return asDict(docTargets)[field];
  }
);
