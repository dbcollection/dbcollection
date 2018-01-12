#########
# Build
#########

build: mybuild
mybuild:
	python setup.py develop

install: myinstall
myinstall:
	python setup.py install

docs: mydocs
mydocs:
	make -C docs html


#########
# Tests
#########

test:
	make build
	tox

test-api:
	make build
	pytest -v dbcollection/tests/core/test_api.py

test-cache:
	make build
	pytest -v dbcollection/tests/core/test_cache.py

test-loader:
	make build
	pytest -v dbcollection/tests/core/test_loader.py

lint:
	tox -e flake8


##########
# Deploy
##########

deploy:
	python conda-recipe/deploy.py
