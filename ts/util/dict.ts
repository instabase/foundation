import {Nonempty} from './types';

export type Path = Nonempty<any[]>;

export type t<T> = {
  [numPathComponents: number]: Map<any, any>;
};

export function empty<T>(): t<T> {
  return {};
}

export function set<T>(dict: t<T>, path: Path, t: T): t<T> {
  function recurse(map: Map<any, any> | undefined, path: any[]): Map<any, any> | T {
    if (path.length == 0) {
      return t;
    } else {
      const copy = new Map(map || []);
      copy.set(
        path[0],
        recurse(
          copy.get(path[0]),
          path.slice(1)));
      return copy;
    }
  }
  return {
    ...dict,
    [path.length]: recurse(dict[path.length], path) as Map<any, any>,
  };
}

export function get<T>(dict: t<T>, path: Path): T | undefined {
  function recurse(map: Map<any, any> | undefined, path: Path): any {
    if (map == undefined) {
      return undefined;
    } else if (path.length == 1) {
      return map.get(path[0]);
    } else {
      return recurse(map.get(path[0]), path.slice(1) as Path);
    }
  }
  return recurse(dict[path.length], path);
}

export function has<T>(dict: t<T>, path: Path): boolean {
  function recurse(map: Map<any, any> | undefined, path: Path): boolean {
    if (map == undefined) {
      return false;
    } else if (path.length == 1) {
      return map.has(path[0]);
    } else {
      return recurse(map.get(path[0]), path.slice(1) as Path);
    }
  }
  return recurse(dict[path.length], path);
}
