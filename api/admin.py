from django.contrib import admin

from api.models import Compartido, Dispositivo, Hogar, Medida, Usuario

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Hogar)
admin.site.register(Compartido)
admin.site.register(Dispositivo)
admin.site.register(Medida)
