from django.urls import path
from apps.authenticate import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
]
