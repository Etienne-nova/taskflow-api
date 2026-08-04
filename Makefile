.PHONY: lint format test quality

lint:
	ruff check .

format:
	black .

test:
	pytest

quality:
	ruff check .
	black --check .