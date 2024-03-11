.PHONY: install
install:
	poetry install

.PHONY: start
start:
	SQLITE_FILE=prod_db.sqlite MILVUS_COLLECTION=ProdCollection poetry run streamlit run ai_researcher/bin/streamlit_main.py

.PHONY: dev
dev:
	poetry run uvicorn --host 127.0.0.1 --port 8080 --reload ai_researcher.bin.main:app

.PHONY: format
format:
	poetry run isort . --skip-glob=frontend/
	poetry run black . --exclude frontend/

.PHONY: lint
lint:
	poetry run flake8 . --exclude=frontend/
