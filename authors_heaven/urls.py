from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("management/", admin.site.urls),
    path("api/v1/", include("apps.common.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Authors Heaven API"
admin.site.site_title = "Authors Heaven API Admin Portal"
admin.site.index_title = "Welcome to Authors Heaven Portal"
