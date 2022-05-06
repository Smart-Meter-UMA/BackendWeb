from django.contrib import admin
from django.urls import path, include

from api.views import UsuarioView

urlpatterns = [
    path('usuarios/', UsuarioView.as_view())
]