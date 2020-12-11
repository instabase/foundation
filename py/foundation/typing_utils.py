from typing import NoReturn


def assert_exhaustive(x: NoReturn) -> NoReturn:
  """Takes advantage of mypy's type narrowing to statically check exhaustivity.

  Use this to ensure all type variants of a Union/Enum/etc are cased.

  See: https://github.com/python/mypy/issues/5818

  Example:
    MyUnion = Union[int, str, bytes]

    def my_function(x: MyUnion) -> None:
      if isinstance(x, int):
        ...
      elif isinstance(x, str):
        ...
      # oh no, we forgot to put in a case for bytes!
      else:
        assert_exhaustive(x)  # mypy will catch this statically
  """
  raise AssertionError(f'Unhandled type: {type(x).__name__}')
