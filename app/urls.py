from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lk/", login_required(views.ClientProfileView.as_view()),
        name="client_profile",),
    path("login/", views.ClientLoginView.as_view(), name="client_login"),
    path("logout/", views.ClientLogoutView.as_view(), name="client_logout"),
]
