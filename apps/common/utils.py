from rest_framework import status
from rest_framework.exceptions import APIException

from django.db.models import Q


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

    # this works on updating
    if instance:
        if model.objects.filter(
            ~Q(pkid=instance.pkid),
            **query,
        ).exists():
            raise ConflictException(errors[field]["unique"])

    else:
        if model.objects.filter(**query).exists():
            raise ConflictException(errors[field]["unique"])
