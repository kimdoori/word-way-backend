#!/usr/bin/env bash
set -e

if [[ "$VIRTUAL_ENV" = "" ]]; then
  echo 'You seem not in any virtual environment.' \
    'Please try after activate virtualenv.'
  exit 1
fi

git config core.hooksPath "$PWD/git/hooks/"

pip install --upgrade pip
pip install -r dev-requirements.txt
