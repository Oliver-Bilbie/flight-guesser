bootstrap: install-deps install-dev-deps
	@pre-commit install

install-deps:
	@echo "[INFO] Installing dependencies"
	@cd backend && python -m pipenv lock --pre
	@cd backend && python -m pipenv install
	@cd frontend && yarn

install-dev-deps:
	@echo "[INFO] Installing dev dependencies"
	@cd backend && python -m pipenv lock --pre
	@cd backend && python -m pipenv install --dev

format-src:
	@echo "[INFO] Formatting backend source code using black"
	@cd backend && python -m pipenv run black src
	@echo "[INFO] Formatting frontend source code using prettier"
	@cd frontend && yarn pretty

lint:
	@echo "[INFO] Linting backend source code using pylint"
	@cd backend && python -m pipenv run pylint --fail-under 7 src/*
	@echo "[INFO] Linting frontend source code using eslint"
	@cd frontend && yarn lint

bandit:
	@echo "[INFO] Linting source code using bandit to look for common security issues in python source"
	@cd backend && python -m pipenv run bandit -r src

type-check:
	@echo "[INFO] Checking static typing of source code using mypy"
	@cd backend && python -m mypy src --ignore-missing-imports
