from sanic.exceptions import SanicException


class TooManyRequests(SanicException):
    status_code = 429
    message = "Rate limit exceeded"
    quiet = True
