from django.db import models
from taggit.managers import TaggableManager

from ..common.models import BaseModel
from ..users.models import User


class Article(BaseModel):
    """Article model"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)
    body = models.TextField()
    tags = TaggableManager()
    author = models.ForeignKey(User, related_name="articles", on_delete=models.CASCADE)
