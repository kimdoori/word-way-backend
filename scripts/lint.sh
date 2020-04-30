#!/usr/bin/env bash
set -e

if [[ "$1" = "" ]] && [[ "$VIRTUAL_ENV" = "" ]]; then
  echo 'You seem not in any virtual environment.  Stopped.' >> /dev/stderr
  exit 1
fi

flake8

sed '/^-/d' requirements.txt | sort -cf
sed '/^-/d' dev-requirements.txt | sort -cf
sed '/^-/d' prod-requirements.txt | sort -cf
