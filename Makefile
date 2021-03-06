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
	pipenv lock --requirements > $(REQUIREMENTS_FILE)
	python setup.py develop
	rm $(REQUIREMENTS_FILE)

.PHONY: install
install: myinstall
myinstall:
	pipenv lock --requirements > $(REQUIREMENTS_FILE)
	python setup.py install
	rm $(REQUIREMENTS_FILE)

.PHONY: docs
docs: mydocs
mydocs:
	make -C docs html

.PHONY: docs-clean
docs-clean:
	make -C docs clean

.PHONY: requirements
requirements:
	pipenv lock --requirements > $(REQUIREMENTS_FILE)

.PHONY: requirements-dev
requirements-dev:
	pipenv lock --requirements --dev > $(REQUIREMENTS_DEV_FILE)


#########
# Tests
#########

.PHONY: test
test:
	pipenv lock --requirements > requirements.txt
	pipenv run tox
	rm requirements.txt

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
