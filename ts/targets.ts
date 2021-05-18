import * as Doc from './doc';
import * as DocTargets from './docTargets';
import * as Schema from './targetsSchema';
import * as TargetValue from './targetValue';
import * as Entity from './entity';

import memo from './util/memo';

type DocTagDescription = {
  short: string | undefined;
  long: string | undefined;
};

type DocTags = Partial<Record<string, DocTagDescription>>;

export type t = {
  doc_targets: DocTargets.t[];
  schema: Schema.t;
  doc_tags: DocTags;

  // output_config
  // field_groups
};

export function build(): t {
  return {
    doc_targets: [],
    schema: Schema.build(),
    doc_tags: {},
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
    return DocTargets.asDocNameDict(targets.doc_targets);
  }
);

export function fields(targets: t): string[] {
  return Schema.fields(targets.schema);
}

export function hasField(targets: t, field: string): boolean {
  return Schema.hasField(targets.schema, field);
}

export type FieldValuePair = [string, TargetValue.t | undefined];

export function fieldValuePairs(
  targets: t,
  docName: string):
    FieldValuePair[] | undefined
{
  const theseDocTargets = docTargets(targets, docName);
  if (theseDocTargets != undefined) {
    return Schema.fieldValuePairs(
      targets.schema,
      theseDocTargets);
  }
}

export function merged(existing: t, provided: t): t {
  return {
    doc_targets: DocTargets.merged(existing.doc_targets, provided.doc_targets),
    schema: Schema.merged(existing.schema, provided.schema),
    doc_tags: mergedDocTags(existing.doc_tags, provided.doc_tags),
  };
}

export function populateSchema(targets: t): t {
  const schema = [...targets.schema];

  targets.doc_targets.forEach(
    docTargets => {
      docTargets.assignments.forEach(
        ({field}) => {
          if (!Schema.hasField(schema, field)) {
            schema.push({
              field,
              type: Entity.heuristicDefaultType(field),
              is_label: Entity.heuristicDefaultIsLabel(field),
            });
          }
        }
      );
    }
  );

  return {...targets, schema};
}

function mergedDocTags(existing: DocTags, provided: DocTags) {
  const keys = new Set([...Object.keys(existing), ...Object.keys(provided)]);
  const result: DocTags = {};
  keys.forEach(
    key => {
      result[key] = {
        short: existing[key]?.short || provided[key]?.short,
        long: existing[key]?.long || provided[key]?.long,
      };
    }
  );
  return result;
}
