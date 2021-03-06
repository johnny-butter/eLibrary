from rest_framework import status
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException

__all__ = [
    'ApiCheckFail',
    'PayFail',
    'InvalidToken',
    'AuthenticationFailed',
    'StockNotEnough',
    'VipOnly',
]


class ApiCheckFail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Check fail'
    default_code = 'general_001'


class StockNotEnough(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Stock not enough')
    default_code = 'book_001'


class PayFail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Pay fail')
    default_code = 'pay_001'


class InvalidToken(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid token')
    default_code = 'auth_001'


class AuthenticationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Auth fail')
    default_code = 'auth_002'


class VipOnly(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('The item is only for VIP')
    default_code = 'auth_003'
