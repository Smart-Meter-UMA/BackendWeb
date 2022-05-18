from django.db import models

# Create your models here.
class Usuario(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    
class Hogar(models.Model):
    nombre = models.CharField(max_length=20)
    potencia_contratada = models.IntegerField()
    owner = models.ForeignKey(Usuario, related_name="owner", on_delete=models.CASCADE)

class Compartido(models.Model):
    compartido = models.ForeignKey(Usuario, related_name='compartido', on_delete=models.CASCADE)
    hogarCompartido = models.ForeignKey(Hogar, related_name='hogarCompartido', on_delete=models.CASCADE)

class Invitacion(models.Model):
    invitado = models.ForeignKey(Usuario, related_name='invitado', on_delete=models.CASCADE)
    hogarInvitado = models.ForeignKey(Hogar, related_name='hogarInvitado', on_delete=models.CASCADE)
    invitante = models.ForeignKey(Usuario, related_name='invitante', on_delete=models.CASCADE)

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=20)
    limite_minimo = models.IntegerField()
    limite_maximo = models.IntegerField()
    tiempo_medida = models.IntegerField()
    hogar = models.ForeignKey(Hogar, related_name='Hogar', on_delete=models.CASCADE)

class Medida(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, related_name='Dispositivo', on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    intensidad = models.FloatField()
    voltaje = models.FloatField()
    kw = models.FloatField()

class Estadistica(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, related_name="dispositivo_estadisitica_diaria", on_delete=models.CASCADE)
    
    fechaDia = models.DateTimeField()
    sumaDiaKW = models.FloatField()
    
    fechaMes = models.DateTimeField()
    sumaMesKW = models.FloatField()

    sumaTotalKW = models.FloatField()
    numDiasTotal = models.IntegerField()
    numMesTotal = models.IntegerField()

    minDiaKw = models.FloatField()
    maxDiaKw = models.FloatField()

    minMesKw = models.FloatField()
    maxMesKw = models.FloatField()


#class Medicion(models.Model):
#    Tipo = (
#        ('V', 'Voltaje'),
#        ('I', 'Intensidad')
#    )
#    tipo = models.CharField(max_length=1, choices=Tipo)
#    valor = models.FloatField()

