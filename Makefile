.PHONY: clean
clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf  '.pytest_cache'
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .tox
	@rm -rf venv/lib/python*/site-packages/*.egg

.PHONY: install_deps
install_deps:
	python -m pip install poetry
	poetry install

.PHONY: install
install:
	poetry build
	poetry install 

.PHONY: lint
lint:
	poetry run tox -e lint

.PHONY: test
test:
	poetry run pytest -v
