from rest_framework import serializers

from api.models import Usuario

class UsuarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    nombre = serializers.CharField(max_length=30)
    apellidos = serializers.CharField(max_length=30)

class HogarSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=20)
    owner = UsuarioSerializer()

class CompartidoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    invitado = UsuarioSerializer()
    hogarInvitado = HogarSerializer()

class DispositivoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=20)
    potencia_contratada = serializers.IntegerField()
    hogar = HogarSerializer()

class MedidaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    dispositivo = DispositivoSerializer()
    fecha = serializers.DateTimeField()
    intensidad = serializers.FloatField()
    voltaje = serializers.FloatField()