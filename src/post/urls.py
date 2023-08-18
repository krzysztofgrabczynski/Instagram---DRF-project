from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.post import views


router = DefaultRouter()
router.register(r"post", views.PostCreateUpdateDeleteView, basename="post")
router.register(r"post_retrive", views.PostRetriveView, basename="post_retrive")

urlpatterns = [
    path("", include(router.urls)),
]
