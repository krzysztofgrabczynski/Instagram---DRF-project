from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.post import views


router = DefaultRouter()
router.register(r"post", views.PostCreateUpdateView, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]