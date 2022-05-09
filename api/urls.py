from django.urls import path

from api.views import LoginView, UsuarioView, UsuarioIDView

urlpatterns = [
    path('usuarios/', UsuarioView.as_view()),
    path('usuarios/<int:id>', UsuarioIDView.as_view()),
    path('login/', LoginView.as_view()),
]