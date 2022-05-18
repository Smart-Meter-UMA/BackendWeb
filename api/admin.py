from django.contrib import admin

from api.models import Compartido, Estadistica, Dispositivo, Hogar, Invitacion, Usuario, Medida

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Hogar)
admin.site.register(Compartido)
admin.site.register(Dispositivo)
admin.site.register(Medida)
admin.site.register(Invitacion)
admin.site.register(Estadistica)