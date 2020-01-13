#!/usr/bin/env bash

[[ -z ${TAGS_BIN} ]] && TAGS_BIN=$(type -p etags)
[[ -z ${PYTHON_BIN} ]] && PYTHON_BIN=$(type -p python)
[[ -z ${TESTS_CMD} ]] && TESTS_CMD="${PYTHON_BIN} -m unittest"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if ! [[ $1 =~ /flycheck_.*\.py$ ]]; then
  echo "Re-running etags."
  ${TAGS_BIN} --declarations \
              ${SCRIPT_DIR}/{lib,tests}/**.py \
              ${SCRIPT_DIR}/{lib,tests}/**/*.py
  echo "Re-running tests."
  ${TESTS_CMD} &
fi

