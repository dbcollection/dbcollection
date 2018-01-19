# Makefile to build, test and deploy dbcollection
#

REQUIREMENTS_FILE = requirements.txt
REQUIREMENTS_DEV_FILE = requirements_dev.txt

.PHONE: shell-python
shell-python:
	pipenv run python -i -c "import rlcompleter, readline; readline.parse_and_bind('tab: complete');"


#########
# Build
#########

.PHONE: build
build: mybuild
mybuild:
	pipenv run python setup.py develop

.PHONY: install
install: myinstall
myinstall:
	pipenv run  python setup.py install

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
	pipenv lock --requirements --dev > $(REQUIREMENTS_DEV_FILE)


#########
# Tests
#########

.PHONY: test
test:
	make build
	pipenv run tox

.PHONY: test-api
test-api:
	make build
	pipenv run pytest -v dbcollection/tests/core/test_api.py

.PHONY: test-cache
test-cache:
	make build
	pipenv run pytest -v dbcollection/tests/core/test_cache.py

.PHONY: test-loader
test-loader:
	make build
	pipenv run pytest -v dbcollection/tests/core/test_loader.py

.PHONY: lint
lint:
	pipenv run tox -e flake8

.PHONY: urls_check
urls_check:
	pipenv run tox -e urls_check_health

##########
# Deploy
##########

.PHONY: eploy
deploy:
	python conda-recipe/deploy.py
