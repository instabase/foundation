#!/usr/bin/env bash

REPO_ROOT="$( git rev-parse --show-toplevel )"

# Get current directory.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PY_OUT="${REPO_ROOT}/py"

STUB_OUT="${REPO_ROOT}/py/stubs/"
mkdir -p ${STUB_OUT}

# Find all directories containing at least one proto file.
# Based on: https://buf.build/docs/migration-prototool#prototool-generate.
for dir in $(find ${DIR} -name '*.proto' -print0 | xargs -0 -n1 dirname | sort | uniq); do
  files=$(find "${dir}" -name '*.proto')

  # Generate python code and mypy stubs.
  protoc -I ${DIR} --python_out=${PY_OUT} --mypy_out=quiet:${PY_OUT} ${files}
done

find "${PY_OUT}/foundation" -type d -exec touch {}/__init__.py \;
find "${PY_OUT}/foundation/protos" -type d -exec touch {}/__init__.pyi \;

