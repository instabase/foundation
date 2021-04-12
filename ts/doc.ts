import * as BBox from './bbox';
import * as Entity from './entity';
import memo from './util/memo';

export type t = {
  bbox: BBox.t;
  entities: Entity.t[];
  name: string | undefined;
};

export const typeNames = memo(
  function(doc: t): string[] {
    const set = new Set<string>(
      [...doc.entities.map(entity => entity.type)]
    );

    return [...set].sort();
  }
);

// It is guaranteed that the indices of entities are stable.
export const entitiesHavingType = memo(
  function(doc: t, typeName: string): Entity.t[] {
    return doc.entities.filter(entity => entity.type == typeName);
  }
);

export const getWords = memo(
  function(doc: t): Entity.t[] {
    return doc.entities.filter(entity =>
      entity.type == 'Text' && entity.words.length == 1);
  }
);