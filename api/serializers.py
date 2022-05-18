from rest_framework import serializers

class UsuarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30, required=False, allow_blank=True)
    nombre = serializers.CharField(max_length=30, required=False, allow_blank=True)
    apellidos = serializers.CharField(required=False, max_length=30, allow_blank=True)

class HogarSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=20)
    is_general = serializers.BooleanField(required=False)
    potencia_contratada = serializers.IntegerField(required=False)
    owner = UsuarioSerializer(required=False)

class CompartidoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    compartido = UsuarioSerializer()
    hogarCompartido = HogarSerializer()

class DispositivoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    nombre = serializers.CharField(max_length=20)
    limite_minimo = serializers.IntegerField()
    limite_maximo = serializers.IntegerField()
    tiempo_medida = serializers.IntegerField(required=False)
    hogar = HogarSerializer(required=False)
    
class MedidaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    dispositivo = DispositivoSerializer(required=False)
    fecha = serializers.DateTimeField(required=False)
    intensidad = serializers.FloatField(required=False)
    voltaje = serializers.FloatField(required=False)

class InvitacionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    invitado = UsuarioSerializer()
    hogarInvitado = HogarSerializer()
    invitante = UsuarioSerializer()
