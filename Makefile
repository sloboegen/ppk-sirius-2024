lint: ruff mypy
	@echo '[OK] Linters checks passed successfully'

mypy:
	poetry run mypy --config-file pyproject.toml --cache-dir=/dev/null src

ruff:
	poetry run ruff check src --no-cache

fmt:
	poetry run ruff check --select I --fix .
	poetry run ruff format . --no-cache
	@echo '[OK] Formatters went through successfully'
