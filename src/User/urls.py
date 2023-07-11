from django.urls import path

from src.user import views


urlpatterns = [
    path("sign_up/", views.UserCreateView.as_view(), name="sign_up"),
    path(
        "edit_account/<int:pk>/",
        views.UserEditAccountView.as_view(),
        name="edit_account",
    ),
    path(
        "edit_password/<int:pk>/",
        views.UserEditPasswordView.as_view(),
        name="edit_password",
    ),
    path(
        "edit_profile/<int:pk>/",
        views.UserEditProfileView.as_view(),
        name="edit_profile",
    ),
    
]
