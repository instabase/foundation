"""Private code for file format modules."""

import dataclasses
import typing


T = typing.TypeVar('T')


def _instantiate(t: typing.Type[T], v: typing.Any,
                 forward_ref_resolver:
                   typing.Optional[
                     typing.Dict[str, typing.Type]] = None) -> T:
  """Map a raw dict to a tree of dataclasses.

  The intended use of this is to load the contents of a JSON file into an
  immutable statically-typed Python object.

  This function may get copy-pasted directly into Python files defining JSON
  schemas -- if you want to use its functionality you should probably make your
  own copy, too.

  Args:
    t: A float, int, string, dict, dataclass, or list, or one of the above
      wrapped in `Optional`. If this is a dataclass, then its attributes must
      also be one of these types. Default values for dataclass members are
      allowed. If this is a list, then it must be a `List[T]`, where `T` is one
      of the above types. If this is a dict, then it must be a `Dict[K, T]`,
      where `K` is an int, float, or str, and `T` is one of the above types.
    v: A float, int, string, dict, list, or `None`.
    forward_ref_resolver: If any dataclasses have types which are forward
      references, this dictionary must be provided, mapping each
      forward-referenced type to its actual class type.

  Example code:
    @dataclass
    class MyDataclass:
      x: int
      name: str
      ys: List[float]
      z: Optional[int] = None

    _instantiate(MyDataclass, {
      'x': 1,
      'name': 'apples',
      'ys': [1, 2.5, 3, 4.3, 5],
    })

  Warning:
    The types given in the dataclass will be used as constructor calls, so if
    for example you set `'name': 42` in the above code, then you would end up
    with `name='42'` in the resulting `MyDataclass` instance.
  """

  FRR = forward_ref_resolver

  # These are provided in `typing` in Python 3.8.
  def get_args(t: typing.Type) -> typing.Tuple[type, ...]:
    return getattr(t, '__args__', tuple())
  def get_origin(t: typing.Type) -> typing.Optional[type]:
    return getattr(t, '__origin__', None)
  # These may not be part of the official API...
  KT = typing.KT # type: ignore
  VT = typing.VT # type: ignore
  def get_forward_arg(t: typing.ForwardRef) -> str:
    return t.__forward_arg__

  def is_optional(t: typing.Type[T]) -> bool:
    return (get_origin(t) is typing.Union and # type: ignore
            len(get_args(t)) == 2 and # type: ignore
            type(None) in get_args(t)) # type: ignore

  def get_optional_arg(t: typing.Type[T]) -> typing.Type:
    assert is_optional(t)
    for subtype in get_args(t): # type: ignore
      if subtype is not type(None):
        return subtype
    assert False

  if dataclasses.is_dataclass(t):
    if not isinstance(v, dict):
      raise RuntimeError('dataclasses must be instantiated from dicts; '
        f'error instantiating {t} from {v}')
    types = {field.name: field.type for field in dataclasses.fields(t)}
    return t(**{key: _instantiate(types[key], value, FRR) # type: ignore
                for key, value in v.items()})

  # This is not right. >>>>:(
  elif get_origin(t) == list or get_origin(t) == tuple:
    if not isinstance(v, list):
      raise RuntimeError('lists must be instantiated from lists; '
        f'error instantiating {t} from {v}')
    return tuple(_instantiate(get_args(t)[0], entry, FRR) for entry in v) # type: ignore

  elif is_optional(t):
    return None if v is None else _instantiate(get_optional_arg(t), v, FRR) # type: ignore

  elif get_origin(t) == dict:
    if not isinstance(v, dict):
      raise RuntimeError('dicts must be instantiated from dicts; '
        f'error instantiating {t} from {v}')

    if (get_args(t) != (KT, VT) and # typing.Dict with no args, Python <  3.9
        get_args(t) != tuple()):    # ditto,                           >= 3.9

      assert len(get_args(t)) == 2 # type: ignore
      key_type, value_type = get_args(t) # type: ignore
      if not key_type in {int, float, str}:
        raise RuntimeError(f'invalid key type in dict: {key_type} in {t}')
      return dict(**{key_type(key): _instantiate(value_type, value, FRR) # type: ignore
                     for key, value in v.items()})
    else:
      return v # type: ignore

  elif isinstance(t, typing.ForwardRef):
    t_name = get_forward_arg(t)
    if FRR and t_name in FRR:
      return _instantiate(FRR[t_name], v, FRR)
    else:
      raise RuntimeError(
        'you need to provide _instantiate with a dictionary to resolve '
        f'types which are forward references (for "{get_forward_arg(t)}")')

  else:
    return t(v) # type: ignore
