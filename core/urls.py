from django.contrib import admin
from django.urls import path, include

from src.user import urls as user_app_urls
from src.post import urls as post_app_urls
from src.comment import urls as comment_app_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(user_app_urls)),
    path("", include(post_app_urls)),
    path("", include(comment_app_urls)),
]
