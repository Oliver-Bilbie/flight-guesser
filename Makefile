bootstrap: install-deps install-dev-deps
	@pre-commit install

test: unit-test int-test

install-deps:
	@echo "[INFO] Installing dependencies"
	@python -m pipenv lock --pre
	@python -m pipenv install

install-dev-deps:
	@echo "[INFO] Installing dev dependencies"
	@python -m pipenv lock --pre
	@python -m pipenv install --dev

format-src:
	@echo "[INFO] Formatting source code using black"
	@cd backend && python -m pipenv run black src

lint:
	@echo "[INFO] Linting source code using pylint"
	@cd backend && python -m pipenv run pylint --fail-under 8 src/service/*

bandit:
	@echo "[INFO] Linting source code using bandit to look for common security issues in python source"
	@cd backend && python -m pipenv run  bandit -r src/service --configfile bandit.yaml

type-check:
	@echo "[INFO] Checking static typing of source code using mypy"
	@cd backend && python -m mypy src/service --ignore-missing-imports
