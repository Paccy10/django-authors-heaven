from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from .helpers.utils import filter_queryset
from .models import Article
from .serializers import ArticleDisplaySerializer, NewArticleSerializer


class ArticlesView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    """Articles view"""

    serializer_class = NewArticleSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["-pkid"]
    search_fields = [
        "title",
        "body",
        "tags__name",
        "author__first_name",
        "author__last_name",
        "author__middle_name",
    ]

    def get_queryset(self):
        return filter_queryset(Article.objects.all(), self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.serializer_class = ArticleDisplaySerializer
        return self.list(request, *args, **kwargs)


class ArticleView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    """Artcicle view"""

    serializer_class = ArticleDisplaySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return filter_queryset(Article.objects.all(), self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
