.PHONY: lint format test quality

lint:
	ruff check .

format:
	black .

test:
	pytest --cov=. --cov-report=term-missing --cov-report=html

quality:
	ruff check .
	black --check .