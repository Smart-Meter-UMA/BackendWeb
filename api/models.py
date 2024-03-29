from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Usuario(models.Model):
    email = models.EmailField()
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    notificacion_invitados = models.BooleanField()
    
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
    verificado = models.BooleanField()
    notificacion = models.BooleanField()
    general = models.BooleanField()
    limite_minimo = models.FloatField()
    limite_maximo = models.FloatField()
    tiempo_medida = models.IntegerField()
    tiempo_refrescado = models.IntegerField()
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
    sumaDiaKw = models.FloatField()
    sumaDiaDinero = models.FloatField()
    
    fechaMes = models.DateTimeField()
    sumaMesKw = models.FloatField()
    sumaMesDinero = models.FloatField()

    sumaTotalKw = models.FloatField()
    sumaTotalDinero = models.FloatField()
    numDiasTotal = models.IntegerField()
    numMesTotal = models.IntegerField()

    fechaSemana = models.DateTimeField()
    sumaSemanaKw = models.FloatField()
    fechaAño = models.DateTimeField()
    sumaAñoKw = models.FloatField()

    tramosHoras = models.JSONField()
    tramoSemanal = models.JSONField()
    tramosMensual = models.JSONField()

    historicoDiario = models.JSONField()
    historicoMensual = models.JSONField()
    historicoMasConsumido = models.JSONField()
    
