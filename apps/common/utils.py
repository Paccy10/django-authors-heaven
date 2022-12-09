from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import APIException


class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict error"

    def __init__(self, detail=None):
        super().__init__(detail=detail)


def validate_unique_value(**kwargs):

    field = kwargs["field"]
    value = kwargs["value"]
    errors = kwargs["errors"]
    model = kwargs["model"]
    instance = kwargs["instance"]
    query = {field: value}

    row = model.objects.filter(**query).first()

    # this works on updating
    if row and instance:
        if row.pkid != instance.pkid:
            raise ConflictException(errors[field]["unique"])

    # this works on first creation
    if row and not instance:
        raise ConflictException(errors[field]["unique"])
