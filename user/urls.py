from django.contrib import admin
from django.urls import path
from . import views as user_views

urlpatterns = [
  path("info",user_views.UsersView.as_view())
]
