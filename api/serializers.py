from rest_framework import serializers

from api.models import Usuario

class UsuarioSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    nombre = serializers.CharField(max_length=30)
    apellidos = serializers.CharField(max_length=30)

class HogarSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=20)
    owner = UsuarioSerializer()

class CompartidoSerializer(serializers.Serializer):
    invitado = UsuarioSerializer()
    hogarInvitado = HogarSerializer()

class DispositivoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=20)
    potencia_contratada = serializers.IntegerField()
    hogar = HogarSerializer()

class MedidaSerializer(serializers.Serializer):
    dispositivo = DispositivoSerializer()
    fecha = serializers.DateTimeField()
    intensidad = serializers.FloatField()
    voltaje = serializers.FloatField()