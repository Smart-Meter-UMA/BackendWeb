from rest_framework import serializers

class UsuarioObtenerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    nombre = serializers.CharField(max_length=30)
    apellidos = serializers.CharField(max_length=30, allow_blank=True)
    notificacion_invitados = serializers.BooleanField()

class UsuarioModificarSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=30)
    apellidos = serializers.CharField(max_length=30, allow_blank=True)
    notificacion_invitados = serializers.BooleanField()

class HogarObtenerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=20)
    potencia_contratada = serializers.IntegerField()

class HogarCrearSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=20)
    potencia_contratada = serializers.IntegerField()

class DispositivoCrearSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    hogar = HogarObtenerSerializer()

class EstadisticaObtenerSerializer(serializers.Serializer):
    consumidoHoy = serializers.FloatField()
    consumidoMes = serializers.FloatField()
    mediaKWHDiaria = serializers.FloatField()
    mediaKWHMensual = serializers.FloatField()
    minKWHDiario = serializers. FloatField()
    diaMinKWHGastado = serializers.DateField()
    maxKWHDiario =  serializers. FloatField()
    diaMaxKWHGastado = serializers.DateField()
    minKWHMensual =  serializers. FloatField()
    mesMinKWHGastado = serializers.DateField()
    maxKWHMensual = serializers.FloatField()
    mesMaxKWHGastado = serializers.DateField()

class DispositivoObtenerByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    estadisticas = EstadisticaObtenerSerializer()

class DispositivoActualizarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    notificacion = serializers.BooleanField()
    limite_maximo = serializers.IntegerField()
    general = serializers.BooleanField()
    limite_minimo = serializers.FloatField()
    tiempo_medida = serializers.IntegerField()
    tiempo_refrescado = serializers.IntegerField()

class DispositivoHogarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=20)
    general = serializers.BooleanField()
    notificacion = serializers.BooleanField()
    limite_minimo = serializers.IntegerField()
    limite_maximo = serializers.IntegerField()
    tiempo_medida = serializers.IntegerField()
    tiempo_refrescado = serializers.IntegerField()

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

class InvitacionCrearSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    correoInvitado = serializers.EmailField()
    hogarInvitado = HogarObtenerSerializer()

class InvitacionEnviadasSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    invitado = UsuarioObtenerSerializer()
    hogarInvitado = HogarObtenerSerializer()

class InvitacionRecibidasSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ofertante = UsuarioObtenerSerializer()
    hogarInvitado = HogarObtenerSerializer()



class HogarObtenerByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=20)
    potencia_contratada = serializers.IntegerField()
    dispositivos = DispositivoHogarSerializer(many=True)
    idCompartido = serializers.IntegerField()

class CompartidoCrearSerializer(serializers.Serializer):
    hogarCompartido = HogarObtenerSerializer()

class CompartidoObtencionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    compartido = UsuarioObtenerSerializer()
