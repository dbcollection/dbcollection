# Makefile to build, test and deploy dbcollection
#

REQUIREMENTS_FILE = requirements.txt
REQUIREMENTS_DEV_FILE = requirements_dev.txt

.PHONY: shell-python
shell-python:
	pipenv run python -i -c "import rlcompleter, readline; readline.parse_and_bind('tab: complete');"


#########
# Build
#########

.PHONY: build
build: mybuild
mybuild:
	python setup.py develop

.PHONY: install
install: myinstall
myinstall:
	python setup.py install

.PHONY: docs
docs: mydocs
mydocs:
	make -C docs html

.PHONY: docs-clean
docs-clean:
	make -C docs clean

.PHONY: requirements
requirements:
	pipenv lock --requirements | tail -n +2 > $(REQUIREMENTS_FILE)

.PHONY: requirements-dev
requirements-dev:
	pipenv lock --requirements --dev | tail -n +2 > $(REQUIREMENTS_DEV_FILE)


#########
# Tests
#########

.PHONY: test
test:
	pipenv run tox

.PHONY: test-api
test-api:
	make build
	pipenv run pytest -v tests/core/api/

.PHONY: test-manager
test-manager:
	make build
	pipenv run pytest -v tests/core/test_manager.py

.PHONY: test-loader
test-loader:
	make build
	pipenv run pytest -v tests/core/test_loader.py

.PHONY: test-utils
test-utils:
	make build
	pipenv run pytest -v tests/utils

.PHONY: test-datasets
test-datasets:
	make build
	pipenv run pytest -v tests/datasets

.PHONY: lint
lint:
	pipenv run tox -e flake8

.PHONY: urls_check
urls_check:
	pipenv run tox -e urls_check_health


##########
# Deploy
##########

.PHONY: deploy
deploy:
	python setup.py sdist upload
	python setup.py bdist_wheel upload
