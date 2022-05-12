from django.urls import path

from api.views import DispositivoIDMedidadView, DispositivoIDView, DispositivosView, HogarIDView, HogarView, HogarsIDispositivosView, LoginView, UsuarioView, UsuarioIDView, UsuariosIDHogaresView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('usuarios/', UsuarioView.as_view()),
    path('usuarios/<int:id>', UsuarioIDView.as_view()),
    path('usuarios/<int:id>/hogars', UsuariosIDHogaresView.as_view()),
    path('hogars/', HogarView.as_view()),
    path('hogars/<int:id>', HogarIDView.as_view()),
    path('hogars/<int:id>/dispositivos', HogarsIDispositivosView.as_view()),
    path('dispositivos/', DispositivosView.as_view()),
    path('dispositivos/<int:id>', DispositivoIDView.as_view()),
    path('dispositivos/<int:id>/medidas', DispositivoIDMedidadView.as_view()),
]