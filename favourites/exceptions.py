from rest_framework.exceptions import APIException


class NotAuthorized(APIException):
    status_code = 401
    default_detail = 'Client with tis token is not authorized by Twitter API'
    default_code = 'not_authorized'


class NotFound(APIException):
    status_code = 404
    default_detail = 'Tweet with this ID is not found'
    default_code = 'not_found'
