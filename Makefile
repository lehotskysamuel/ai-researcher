.PHONY: install
install:
	poetry install

.PHONY: start
start:
	poetry run start

.PHONY: format
format:
	poetry run isort .
	poetry run black .

.PHONY: lint
lint:
	poetry run flake8 .
