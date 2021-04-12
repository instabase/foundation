import * as Doc from './doc';
import * as DocTargets from './docTargets';
import * as TargetValue from './targetValue';
import * as TargetsSchema from './targetsSchema';
import memo from './util/memo';

export type t = {
  doc_targets: DocTargets.t[];
  schema: TargetsSchema.t;
  // output_config
  // doc_tags
  // field_groups
};

export function build(): t {
  return {
    doc_targets: [],
    schema: TargetsSchema.build(),
  };
}

export const docNames = memo(
  function(targets: t): string[] {
    return targets.doc_targets.map(
      docTargets => docTargets.doc_name
    );
  }
);

export function docTargets(
  targets: t,
  docName: string):
    DocTargets.t | undefined
{
  return asDict(targets)[docName];
}

export const asDict = memo(
  function(targets: t):
    Partial<Record<string, DocTargets.t>>
  {
    const result: Partial<Record<string, DocTargets.t>> = {};
    targets.doc_targets.forEach(
      docTargets => {
        result[docTargets.doc_name] = docTargets;
      }
    );
    return result;
  }
);

export function fields(targets: t): string[] {
  return TargetsSchema.fields(targets.schema);
}

export function hasField(targets: t, field: string): boolean {
  return TargetsSchema.hasField(targets.schema, field);
}

export type FieldValuePair = [string, TargetValue.t | undefined];

export function fieldValuePairs(
  targets: t,
  docName: string):
    FieldValuePair[] | undefined
{
  const theseDocTargets = docTargets(targets, docName);
  if (theseDocTargets != undefined) {
    return TargetsSchema.fieldValuePairs(
      targets.schema,
      theseDocTargets);
  }
}
