#!/usr/bin/env bash

# This has to be run from within the Foundation repository.

set -e # Exit when any command fails.

REPO_ROOT="$( git rev-parse --show-toplevel )"

FND_PYTHONPATH=$REPO_ROOT/py
export PYTHONPATH="$PYTHONPATH:$FND_PYTHONPATH"

UNITTEST_DIR="$REPO_ROOT/unit_tests/"

echo "Checking mypy"
python3 -m mypy $FND_PYTHONPATH/foundation
echo "Ok mypy"

echo "Checking unit tests"
python3 -m unittest $UNITTEST_DIR/*.py
echo "Ok unit tests"

echo "ALL TESTS PASSED"
