#!/usr/bin/env bash

REPO_ROOT="$( git rev-parse --show-toplevel )"

PY_OUT="${REPO_ROOT}/py"
PROTOS_DIR="${PY_OUT}/foundation/protos"

if [ -d "$PROTOS_DIR" ]; then
  rm -r "$PROTOS_DIR"
fi
