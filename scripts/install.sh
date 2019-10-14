#!/usr/bin/env bash
set -e

if [[ "$VIRTUAL_ENV" = "" ]]; then
  echo 'You seem not in any virtual environment.' \
    'Please try after activate virtualenv.'
  exit 1
fi

if [[ ! -f .git/hooks/pre-commit ]]; then
  cwd="$( cd "$(dirname "$0")/.." ; pwd -P )"
  git config core.hooksPath "$cwd/hooks"
fi

pip install --upgrade pip
pip install -r dev-requirements.txt
