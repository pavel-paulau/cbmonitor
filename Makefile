PYTHON := python3.5
ENV := env

build:
	virtualenv --quiet --python ${PYTHON} ${ENV}
	${ENV}/bin/pip install --upgrade --quiet pip wheel
	${ENV}/bin/pip install --quiet -r requirements.txt

clean:
	find . -name '*.pyc' -o -name '*.pyo' -o -name __pycache__ | xargs rm -fr

pep8:
	${ENV}/bin/flake8 --statistics cbmonitor
	${ENV}/bin/isort --quiet --check-only --recursive cbmonitor

test: pep8
