from django.urls import path

from api.views import CompartidoView, CompartidosIDView, DispositivoIDEstadisticasView, DispositivoIDMedidadView, DispositivoIDView, DispositivosView, HogarIDView, HogarView, HogarsIDCompartidosView, HogarsIDispositivosView, InvitacionsIDView, LoginView, UsuarioView, UsuarioIDView, UsuariosIDHogaresView, UsuariosIDInvitacionsView

urlpatterns = [
    path('login/', LoginView.as_view()),

    path('usuarios/', UsuarioView.as_view()),
    path('usuarios/<int:id>', UsuarioIDView.as_view()),
    path('usuarios/<int:id>/hogars', UsuariosIDHogaresView.as_view()),
    path('usuarios/<int:id>/invitacions', UsuariosIDInvitacionsView.as_view()),

    path('hogars/', HogarView.as_view()),
    path('hogars/<int:id>', HogarIDView.as_view()),
    path('hogars/<int:id>/dispositivos', HogarsIDispositivosView.as_view()),
    path('hogars/<int:id>/compartidos', HogarsIDCompartidosView.as_view()),

    path('dispositivos/', DispositivosView.as_view()),
    path('dispositivos/<int:id>', DispositivoIDView.as_view()),
    path('dispositivos/<int:id>/medidas', DispositivoIDMedidadView.as_view()),
    path('dispositivos/<int:id>/estadisticas', DispositivoIDEstadisticasView.as_view()),

    path('invitacions/<int:id>', InvitacionsIDView.as_view()),
    path('compartidos/', CompartidoView.as_view()),
    path('compartidos/<int:id>', CompartidosIDView.as_view()),
]