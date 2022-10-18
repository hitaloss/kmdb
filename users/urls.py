from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:user_id>/", views.UserDetailView.as_view()),
    path("users/register/", views.UserCreateView.as_view()),
    path("users/login/", obtain_auth_token),
    # path("users/login/", LoginView.as_view()),
]
