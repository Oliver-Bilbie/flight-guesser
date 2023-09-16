"""Logic for error handling"""

import json
import traceback


class ValidationException(Exception):
    """
    This class is used to handle exceptions raised due to input validaiton.
    It behaves identially to the Exception class.
    """


def handle_exceptions(function):
    """
    Decorator function to handle runtime errors.
    Any errors handled within the code should be raised as
    "ValidationException" types, in which case the error message will be
    passed to the API. Any other error class will return a generic error
    message.

    Args:
        function [Python function]: The function to be executed

    Returns:
        [json]: Json-encoded API response
    """

    def inner(*args):
        try:
            response = function(*args)

        except ValidationException as exc:
            print(traceback.format_exc())
            response = json.dumps({"response": str(exc), "status": 400})

        except Exception:  # pylint: disable=W0718
            print(traceback.format_exc())
            response = json.dumps(
                {
                    "response": "The server was unable to process your request",
                    "status": 500,
                }
            )

        return response

    return inner
