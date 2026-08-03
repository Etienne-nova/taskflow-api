.PHONY: lint format test quality

lint:
	ruff check .

format:
	black .

test:
	python manage.py test

quality:
	ruff check .
	black --check .