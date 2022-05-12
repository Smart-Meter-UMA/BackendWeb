from rest_framework import serializers

from api.models import Usuario

class UsuarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30, required=False, allow_blank=True)
    nombre = serializers.CharField(max_length=30, required=False, allow_blank=True)
    apellidos = serializers.CharField(required=False, max_length=30, allow_blank=True)

class HogarSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=20)
    owner = UsuarioSerializer(required=False)

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
    kw = serializers.FloatField(required=False)