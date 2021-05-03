#!/usr/bin/env bash

# This has to be run from the root of the Foundation repo.

set -e # Exit when any command fails.

REPO_ROOT="$(git rev-parse --show-toplevel)"

FND_PYTHONPATH=$REPO_ROOT/py

export PYTHONPATH="$PYTHONPATH:$FND_PYTHONPATH"
export MYPYPATH="$PYTHONPATH"

UNIT_TEST_DIR="$REPO_ROOT/unit_tests_py"

echo "Checking mypy"
python3 -m mypy $FND_PYTHONPATH/foundation --show-traceback
python3 -m mypy $UNIT_TEST_DIR
echo "Ok mypy"

echo "Checking unit tests"
python3 -m unittest $UNIT_TEST_DIR/*.py
echo "Ok unit tests"

echo "ALL TESTS PASSED"
