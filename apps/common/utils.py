from functools import wraps

from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.request import Request


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


def send_email(subject, message, to):
    email_message = EmailMessage(subject, message, to=to)
    email_message.content_subtype = "html"
    email_message.send()


def find_request(args):
    for item in args:
        if isinstance(item, Request):
            return item


def should_be_admin():
    """Decorator to check if the user is an admin"""

    def check(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            request = find_request(args)

            if not request.user.is_admin:
                raise PermissionDenied()

            return view(*args, **kwargs)

        return wrapped_view

    return check


def get_country_name(country):
    return country.name if country else None
