from django.urls import path

from api.views import LoginGoogleView, LoginGoogleCheckView, UsuarioView, UsuarioIDView

urlpatterns = [
    path('usuarios/', UsuarioView.as_view()),
    path('usuarios/<int:id>', UsuarioIDView.as_view()),
    path('login/', LoginGoogleView.as_view()),
    path('login/check', LoginGoogleCheckView.as_view()),
]