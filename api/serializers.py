from rest_framework import serializers

from api.models import Estadistica

class UsuarioObtenerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    nombre = serializers.CharField(max_length=30)
    apellidos = serializers.CharField(max_length=30, allow_blank=True)

class UsuarioModificarSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=30)
    apellidos = serializers.CharField(max_length=30, allow_blank=True)

class HogarObtenerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=20)
    potencia_contratada = serializers.IntegerField()

class HogarCrearSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=20)
    potencia_contratada = serializers.IntegerField()

class CompartidoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    compartido = UsuarioObtenerSerializer()
    hogarCompartido = HogarObtenerSerializer()

class DispositivoCrearSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    hogar = HogarObtenerSerializer()

class EstadisticaObtenerSerializer(serializers.Serializer):
    mediaKwhDiaria = serializers.FloatField()
    mediaKwhMensual = serializers.FloatField()
    minKWHDiaria = serializers. FloatField()
    diaMinKWHGastado = serializers.DateField()
    maxKWHDiario =  serializers. FloatField()
    diaMaxKWHGastado = serializers.DateField()
    minKWHMensual =  serializers. FloatField()
    mesMinKWHGastado = serializers.DateField()
    maxKwhMensual = serializers.FloatField()
    mesMaxKwhGastado = serializers.DateField()

class DispositivoObtenerByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    estadisticas = EstadisticaObtenerSerializer()

class DispositivoActualizarSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    notificacion = serializers.BooleanField()
    limiteMaximo = serializers.IntegerField()

class DispositivoHogarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=20)

class DispositivoModificarSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=20)
    notificacion = serializers.BooleanField()
    general = serializers.BooleanField()
    tiempo_medida = serializers.IntegerField(required=False)
    tiempo_refrescado = serializers.IntegerField(required=False)
    limite_minimo = serializers.FloatField(required=False)
    limite_maximo = serializers.FloatField(required=False)

class MedidaObtenerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fecha = serializers.DateTimeField()
    kw = serializers.FloatField()

class MedidaCrearSerializer(serializers.Serializer):
    fecha = serializers.DateTimeField()
    intensidad = serializers.FloatField()
    voltaje = serializers.FloatField(required=False)
    desfase = serializers.FloatField(required=False)

class InvitacionEnviadasSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    invitado = UsuarioObtenerSerializer()
    hogarInvitado = HogarObtenerSerializer()

class InvitacionRecibidasSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    oferta = UsuarioObtenerSerializer()
    hogarInvitado = HogarObtenerSerializer()

class HogarObtenerByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=20)
    potencia_contratada = serializers.IntegerField()
    dispositivos = DispositivoModificarSerializer(many=True)
