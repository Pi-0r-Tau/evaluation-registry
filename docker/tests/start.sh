#!/bin/sh

set -o errexit
set -o nounset

python manage.py migrate --noinput
echo
echo '----------------------------------------------------------------------'
echo
nosetests -v ./tests --logging-level=ERROR --with-coverage --cover-package=evaluation_registry
pytest -v ./pytest_tests
