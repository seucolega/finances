.PHONY:	install format lint test sec
ISORT_ARGS=--trailing-comma --multi-line 3
PYTHONPATH=./my_finances

install:
	@poetry install
	@pip uninstall pylint-django -y
format:
	@blue .
	@isort . $(ISORT_ARGS)
lint:
	@blue . --check
	@isort . --check $(ISORT_ARGS)
test:
	@prospector . --with-tool pep257 --doc-warning
	@PYTHONPATH=$(PYTHONPATH) pytest -v --cov --cov-report term-missing
