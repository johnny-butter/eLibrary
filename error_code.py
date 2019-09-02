from rest_framework import status
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException


class PayFail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Pay fail.')
    default_code = 'pay_error'
