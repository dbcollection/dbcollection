build: mybuild
mybuild:
	python setup.py develop

docs: mydocs
mydocs:
	make -C docs html

test:
	make build
	tox

lint:
	tox -e flake8

deploy:
	python conda-recipe/deploy.py
