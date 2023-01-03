from django.urls import path

from .views import ArticlesView, ArticleView

urlpatterns = [
    path("", ArticlesView.as_view(), name="all-articles"),
    path("<slug:slug>/", ArticleView.as_view(), name="single-article"),
]
