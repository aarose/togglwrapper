# -*- coding: utf-8 -*-

"""
togglwrapper.decorators
-----------------------

This module collects all decorators. These decorators manipulate the output of
methods, and ensure errors in the responses are raised as exceptions.
"""

from functools import wraps
from typing import Any, Callable
from requests import Response

from .exceptions import AuthError


def return_json(func: Callable[..., Response]) -> Any:
    """Returns the JSON content of a requests.Response."""

    @wraps(func)
    def inner(*args, **kwargs) -> Any:
        response = func(*args, **kwargs)
        return response.json()

    return inner


def error_checking(func: Callable[..., Response]) -> Response:
    """Raises exceptions if the response did not return 200 OK."""

    @wraps(func)
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        # Status code of 403 Forbidden means incorrect API token/wrong auth
        if response.status_code == 403:
            raise AuthError("Incorrect API token.")
        # Raise an HTTPError if status code isn't 200
        try:
            reason = response.json()
        except ValueError:
            pass
        else:
            response.reason = reason
        response.raise_for_status()
        return response

    return inner
