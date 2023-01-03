from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from .models import Article
from .serializers import NewArticleSerializer


class ArticlesView(mixins.CreateModelMixin, generics.GenericAPIView):
    """Articles view"""

    queryset = Article.objects.all()
    serializer_class = NewArticleSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
