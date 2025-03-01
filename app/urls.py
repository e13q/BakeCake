from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path("", views.index, name="index"),
    path("lk/", login_required(views.ClientProfileView.as_view()),
        name="client_profile",),
    path("login/", views.ClientLoginView.as_view(), name="client_login"),
    path("logout/", views.ClientLogoutView.as_view(), name="client_logout"),
    path('create-order/', views.create_order, name='create_order'),
]
