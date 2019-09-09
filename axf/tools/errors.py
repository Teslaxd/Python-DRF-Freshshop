
from rest_framework.exceptions import APIException


class PramException(APIException):

    def __init__(self, err):
        self.detail = err








