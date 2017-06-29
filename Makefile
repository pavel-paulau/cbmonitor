SHELL := /bin/bash

ENV := env
PYTHON := python3.5

build:
	virtualenv --quiet --python ${PYTHON} ${ENV}
	${ENV}/bin/pip install --upgrade --quiet pip wheel
	${ENV}/bin/pip install --quiet -r requirements.txt

clean:
	find . -name '*.pyc' -o -name '*.pyo' -o -name __pycache__ | xargs rm -fr

pep8:
	${ENV}/bin/flake8 --statistics cbmonitor
	${ENV}/bin/isort --quiet --check-only --recursive cbmonitor
	${ENV}/bin/pydocstyle cbmonitor

test:
	${ENV}/bin/nosetests --verbose --with-coverage --cover-html --cover-package cbmonitor tests.py

check: pep8 test
