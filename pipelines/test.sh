!/bin/bash

set -Eeo pipefail
trap "echo '[FAILED]' && exit 1" ERR

echo "[INFO] Installing dependencies"
make install-dev-deps

echo "[INFO] Running tests"
make lint
make bandit
make unit-test
make int-test
make frontend-test

echo "[INFO] Testing successful"