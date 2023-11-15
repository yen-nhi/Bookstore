import functools
from django.http import HttpResponse


def pattern_response(func):
    """
    Wrap the route with a pattern response for api request
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> HttpResponse:
        try:
            func(*args, **kwargs)
            return Response(status=200, response="Successful processing")
        except Exception as err:
            return Response(status=400, response=f"Bad request | {err.__class__.__name__}")
    return wrapper

