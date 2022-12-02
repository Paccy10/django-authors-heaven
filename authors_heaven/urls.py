from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("management/", admin.site.urls),
]

admin.site.site_header = "Authors Heaven API"
admin.site.site_title = "Authors Heaven API Admin Portal"
admin.site.index_title = "Welcome to Authors Heaven Portal"
