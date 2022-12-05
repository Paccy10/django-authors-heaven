from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("management/", admin.site.urls),
    path("api/v1/", include("apps.common.urls")),
]

admin.site.site_header = "Authors Heaven API"
admin.site.site_title = "Authors Heaven API Admin Portal"
admin.site.index_title = "Welcome to Authors Heaven Portal"
