.PHONY: proxy
proxy:
	poetry run uvicorn ai_researcher.bin.enhanced_inference_proxy:app --reload --port 4242

.PHONY: format
format:
	poetry run isort .
	poetry run black .

.PHONY: lint
lint:
	poetry run flake8 .
