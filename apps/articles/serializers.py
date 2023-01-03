from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from ..common.serializers import BaseSerializer
from ..users.models import User
from .helpers.utils import generate_slug
from .models import Article


class AuthorSerializer(serializers.ModelSerializer):
    """Author serializer"""

    avatar = serializers.ImageField(source="profile.avatar")

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "middle_name", "avatar"]


class NewArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    """New article serializer"""

    title = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    body = serializers.CharField()
    tags = TagListSerializerField(required=False)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            "title",
            "slug",
            "body",
            "tags",
            "author",
        ] + BaseSerializer.Meta.fields

    def create(self, validated_data):
        validated_data["slug"] = generate_slug(validated_data["title"])
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
