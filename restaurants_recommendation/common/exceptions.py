from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidParameterException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid parameter"
    default_code = "invalid_parameter"
