"""Unit Test for the Utils class."""

from genai.exceptions import ApiResponseException
from httpx import Response
from openai import BadRequestError

from ols.utils import errors_parsing


def test_parse_generic_llm_error_on_bad_request_error_without_info():
    """Test the parse_generic_llm_error function when BadRequestError is passed."""
    status_code = 400
    response = Response(status_code=status_code, request={})
    error = BadRequestError("Exception", response=response, body=None)

    # try to parse the exception
    status_code, error_message, cause = errors_parsing.parse_generic_llm_error(error)

    # check the parsed error
    assert status_code == status_code
    assert error_message == "Exception"
    assert cause == "Exception"


def test_parse_generic_llm_error_on_bad_request_error_with_info():
    """Test the parse_generic_llm_error function when BadRequestError is passed."""
    status_code = 400
    message = "Exception message"
    response = Response(status_code=status_code, request={})
    error = BadRequestError("Exception", response=response, body={"message": message})

    # try to parse the exception
    status_code, error_message, cause = errors_parsing.parse_generic_llm_error(error)

    # check the parsed error
    assert status_code == status_code
    assert error_message == message
    assert cause == "Exception"


def test_parse_generic_llm_error_on_api_response_exception_without_info():
    """Test the parse_generic_llm_error function when ApiResponseException is passed."""
    error = ApiResponseException(
        response={
            "error": "",
            "message": "",
            "extensions": {},
            "status_code": 400,
        },
        message=None,
    )

    # try to parse the exception
    status_code, error_message, cause = errors_parsing.parse_generic_llm_error(error)

    # check the parsed error
    assert status_code == status_code
    expected = """Server Error
{
  "error": "",
  "extensions": {
    "code": "INVALID_INPUT",
    "state": null
  },
  "message": "",
  "status_code": 400
}"""
    assert error_message == expected
    assert cause == expected


def test_parse_generic_llm_error_on_api_response_exception_with_info():
    """Test the parse_generic_llm_error function when ApiResponseException is passed."""
    error = ApiResponseException(
        response={
            "error": "this is error",
            "message": "this is error message",
            "extensions": {},
            "status_code": 400,
        },
        message=None,
    )

    # try to parse the exception
    status_code, error_message, cause = errors_parsing.parse_generic_llm_error(error)

    # check the parsed error
    assert status_code == status_code
    expected = """Server Error
{
  "error": "this is error",
  "extensions": {
    "code": "INVALID_INPUT",
    "state": null
  },
  "message": "this is error message",
  "status_code": 400
}"""
    assert error_message == expected
    assert cause == expected


def test_parse_generic_llm_error_on_unknown_exception():
    """Test the parse_generic_llm_error function when unknown exception is passed."""
    # generic exception
    error = Exception("Exception")

    # try to parse the exception
    status_code, error_message, cause = errors_parsing.parse_generic_llm_error(error)

    # check the parsed error
    assert status_code == errors_parsing.DEFAULT_STATUS_CODE
    assert error_message == errors_parsing.DEFAULT_ERROR_MESSAGE
    assert cause == "Exception"


def test_parse_generic_llm_error_on_unknown_exception_without_message():
    """Test the parse_generic_llm_error function when unknown exception is passed."""
    # generic exception
    error = Exception()

    # try to parse the exception
    status_code, error_message, cause = errors_parsing.parse_generic_llm_error(error)

    # check the parsed error
    assert status_code == errors_parsing.DEFAULT_STATUS_CODE
    assert error_message == errors_parsing.DEFAULT_ERROR_MESSAGE
    assert cause == ""
