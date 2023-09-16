"""Unit tests for the error handling logic"""

import json
import pytest
from src.service import error_handling


@pytest.fixture
def return_true():
    @error_handling.handle_exceptions
    def inner():
        return True

    return inner


@pytest.fixture
def raise_validation_exception():
    @error_handling.handle_exceptions
    def inner():
        raise error_handling.ValidationException("test_error")

    return inner


@pytest.fixture
def raise_exception():
    @error_handling.handle_exceptions
    def inner():
        raise Exception("test_error")

    return inner


def test_handle_exceptions_success(return_true):
    assert return_true()


def test_handle_exceptions_validation_error(raise_validation_exception):
    response = raise_validation_exception()
    assert response == json.dumps({"response": "test_error", "status": 400})


def test_handle_exceptions_runtime_error(raise_exception):
    response = raise_exception()
    assert response == json.dumps(
        {"response": "The server was unable to process your request", "status": 500}
    )
