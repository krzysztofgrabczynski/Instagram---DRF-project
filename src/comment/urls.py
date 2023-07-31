from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.comment import views


router = DefaultRouter()
router.register(
    r"comment", views.CommentUpdateDeleteView, basename="comment_update_delete"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "create_comment/<int:pk>/",
        views.CommentCreateView.as_view(),
        name="create_comment",
    ),
]
