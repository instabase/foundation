#!/usr/bin/env bash

# This has to be run from within the Foundation repository.

set -e # Exit when any command fails.

REPO_ROOT="$( git rev-parse --show-toplevel )"

export FONDN_PYTHONPATH=$REPO_ROOT/py
export PYTHONPATH="$PYTHONPATH:$FONDN_PYTHONPATH"

python3 -m mypy $FONDN_PYTHONPATH/foundation

echo "ALL TESTS PASSED"
