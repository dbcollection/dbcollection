shell-python:
	pipenv run python -i -c "import rlcompleter, readline; readline.parse_and_bind('tab: complete');"


#########
# Build
#########

build: mybuild
mybuild:
	pipenv run python setup.py develop

install: myinstall
myinstall:
	pipenv run  python setup.py install

docs: mydocs
mydocs:
	make -C docs html

requirements:
	pipenv lock --requirements > requirements.txt
	pipenv lock --requirements --dev > requirements_dev.txt


#########
# Tests
#########

test:
	make build
	pipenv run tox

test-api:
	make build
	pipenv run pytest -v dbcollection/tests/core/test_api.py

test-cache:
	make build
	pipenv run pytest -v dbcollection/tests/core/test_cache.py

test-loader:
	make build
	pipenv run pytest -v dbcollection/tests/core/test_loader.py

lint:
	pipenv run tox -e flake8

urls_check:
	pipenv run tox -e urls_check

##########
# Deploy
##########

deploy:
	python conda-recipe/deploy.py
