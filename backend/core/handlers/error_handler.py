from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from core.exceptions.jwt_exception import JwtException  # Імпорт класу JwtException

def error_handler(exc: Exception, context: dict) -> Response:
    handlers = {
        "JwtException": _jwt_validation_error_handler
    }

    response = exception_handler(exc, context)
    exc_class = exc.__class__.__name__

    if exc_class in handlers:
        return handlers[exc_class](exc, context)

    return response

def _jwt_validation_error_handler(exc: Exception, context: dict) -> Response:
    return Response({'detail': 'Token is invalid or expired'}, status.HTTP_403_FORBIDDEN)
