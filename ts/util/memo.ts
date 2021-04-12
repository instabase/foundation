import * as Dict from './dict';
import {Nonempty} from './types';

export default function memo
  <Args extends Nonempty<unknown[]>, Ret>(
    f: (...args: Args) => Ret):
      (...args: Args) => Ret
{
  let dict: Dict.t<Ret> = {};

  return (...args: Args): Ret => {
    if (!Dict.has(dict, args)) {
      dict = Dict.set(dict, args, f(...args));
    }
    return Dict.get(dict, args) as Ret;
  };
}
