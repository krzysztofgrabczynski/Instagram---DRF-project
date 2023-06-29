from django.urls import path, include

from src.user import views


urlpatterns = [
    path("sign_up/", views.UserCreateView.as_view(), name="sign_up")
]
