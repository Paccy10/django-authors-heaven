import random
import string

from ..models import Article


def generate_slug(title, prefix=None):
    slug = "-".join(title.split(" ")).lower()
    slug = slug + f"-{prefix}" if prefix else slug

    if not Article.objects.filter(slug=slug).exists():
        return slug

    else:
        random_str = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=7)
        )
        return generate_slug(title, random_str)


def filter_queryset(queryset, user):
    if user.is_admin:
        return queryset

    return queryset.filter(author=user)
