from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        # Gneric API Exceptions
        return Response({"error": "internal_error", "detail": "An unexpected error occurred."},status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
    
    data = {"error": response.status_code,"details": response.data,}
    response.data = data
    return response
