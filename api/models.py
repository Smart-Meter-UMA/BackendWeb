from django.db import models

# Create your models here.
class Usuario(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)

class Hogar(models.Model):
    nombre = models.CharField(max_length=20)
    owner = models.ForeignKey(Usuario, related_name="owner", on_delete=models.CASCADE)

class Compartido(models.Model):
    invitado = models.ForeignKey(Usuario, related_name='Invitado', on_delete=models.CASCADE)
    hogarInvitado = models.ForeignKey(Hogar, related_name='HogarInvitado', on_delete=models.CASCADE)

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=20)
    potencia_contratada = models.IntegerField()
    hogar = models.ForeignKey(Hogar, related_name='Hogar', on_delete=models.CASCADE)

class Medida(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, related_name='Dispositivo', on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    intensidad = models.FloatField()
    voltaje = models.FloatField()


#class Medicion(models.Model):
#    Tipo = (
#        ('V', 'Voltaje'),
#        ('I', 'Intensidad')
#    )
#    tipo = models.CharField(max_length=1, choices=Tipo)
#    valor = models.FloatField()

