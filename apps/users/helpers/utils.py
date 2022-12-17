import random

from ..models import User


def generate_username(name):
    username = "".join(name.split(" ")).lower()

    if not User.objects.filter(username=username).exists():
        return username

    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)
