.PHONY: run
run:
	poetry run uvicorn src.app.main:app --port=8000 --host=0.0.0.0

.PHONY: rundev
rundev:
	poetry run uvicorn src.app.main:app --reload --port=8000 --host=0.0.0.0

.PHONY: install
install:
	pip install -U poetry && poetry install

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit install --hook-type pre-commit

.PHONY: update
update:
	poetry update

.PHONY: lint
lint:
	poetry run pre-commit run
