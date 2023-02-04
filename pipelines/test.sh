# !/bin/bash

set -Eeo pipefail

##### Test backend #####
cd backend
echo "[INFO] Installing backend development dependencies"
python -m pipenv install --dev

echo "[INFO] Linting backend source code using pylint"
python -m pipenv run pylint --fail-under 7.5 src/service/*

echo "[INFO] Linting source code using bandit to look for common security issues in python source"
python -m pipenv run bandit -r src/serivce

# echo "[INFO] Running unit tests"
# export COVERAGE_FILE=./target/coverage/.cov_unit
# python -m pipenv run coverage run --source=src/service -m pytest -s --junitxml=target/unit-test/unit-result.xml src/test/unit/*.py
# python -m pipenv run coverage html --directory=target/unit-test/coverage --fail-under=60
# python -m pipenv run coverage report
# python -m pipenv run coverage xml -o target/unit-test/coverage/coverage.xml

# echo "[INFO] Running component integration tests"
# export COVERAGE_FILE=./target/coverage/.cov_int
# python -m pipenv run coverage run --source=src/service -m pytest -s --junitxml=target/integration-test/integration-result.xml src/test/integration/*.py
# python -m pipenv run coverage html --directory=target/integration-test/coverage --fail-under=50
# python -m pipenv run coverage report
# python -m pipenv run coverage xml -o target/integration-test/coverage/coverage.xml


##### Test frontend #####
cd ../frontend
echo "[INFO] Installing frontend development dependencies"
yarn

echo "[INFO] Linting frontend source code using eslint"
yarn lint

# echo "[INFO] Running frontend tests"
# yarn test

echo "[INFO] Testing completed successfully"