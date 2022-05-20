from django.urls import path

from api.views import DispositivoIDView, DispositivosView, HogarIDView, HogarView, HogarsIDCompartidosView, InvitacionsIDView, InvitacionsRecibidasView, LoginView, MedidaView, OfrecerInvitacionView, UsuarioView


urlpatterns = [
    path("login/", LoginView.as_view()),
    path("usuarios/", UsuarioView.as_view()),
    path("hogars/", HogarView.as_view()),
    path("hogars/<int:id>", HogarIDView.as_view()),
    path("hogars/<int:id>/compartidos", HogarsIDCompartidosView.as_view()),
    path("dispositivos/", DispositivosView.as_view()),
    path("dispositivos/<int:id>", DispositivoIDView.as_view()),
    path("medidas/", MedidaView.as_view()),
    path("ofrecerInvitacion/", OfrecerInvitacionView.as_view()),
    path("invitacionsRecibidas/", InvitacionsRecibidasView.as_view()),
    path("invitacions/<int:id>", InvitacionsIDView.as_view())
]