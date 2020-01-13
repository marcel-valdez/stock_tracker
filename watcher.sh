#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
watchfile -R -d "${SCRIPT_DIR}" --regx '^'${SCRIPT_DIR}'/(tests|lib)/.*\.py$' \
          "bash ${SCRIPT_DIR}/file_changed_handler.sh __file__"
