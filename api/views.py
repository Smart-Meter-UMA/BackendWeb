from urllib import response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.dto import UsuarioDTO
from api.models import Usuario
from api.serializers import UsuarioSerializer
from google.oauth2 import id_token
from google.auth import transport
from datetime import date

CLIENT_ID = "860266555787-337c130jdi6jar97gkmomb1dq71sv02i.apps.googleusercontent.com"

def autorizar(request):
    if request.headers.get('Authorization') is not None:
            
        token = request.headers.get('Authorization')
        idinfo = None
        try:
            idinfo = id_token.verify_oauth2_token(token, transport.requests.Request(), CLIENT_ID)
        except:
            return None

        email = idinfo['email']

        try:
            usuario = Usuario.objects.get(email=email)
            return usuario
        except:
            return None
    else :
        return None

# Create your views here.

# /usuarios
class UsuarioView(APIView):
    def get(self,request,format=None):
        usuarios = Usuario.objects.all()

        usuariosDTO = UsuarioDTO.toUsuariosDTO(usuarios)

        serializer = UsuarioSerializer(usuariosDTO,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":usuarios.count()})


class UsuarioIDView(APIView):
    def get(self,request,id,format=None):
        try:
            usuario = Usuario.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un usuario con ese ID"},status=status.HTTP_404_NOT_FOUND)

        usuarioDTO = UsuarioDTO(usuario)
        serializer = UsuarioSerializer(usuarioDTO)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id,format=None):
        try:
            usuario = Usuario.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un usuario con ese ID."},status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario.nombre = serializer.validated_data.get("nombre")
            usuario.apellidos = serializer.validated_data.get("apellidos")
            try:
                usuario.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"mensaje":"Error: El usuario no ha podido ser actualizado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del usuario es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        try:
            usuario = Usuario.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un usuario con ese ID"},status=status.HTTP_404_NOT_FOUND)
        try:
            usuario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar un usuario con ese ID"},status=status.HTTP_400_BAD_REQUEST)

#/login
class LoginView(APIView):
    def post(self,request,format=None):
        email = request.data.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
        except:
            usuario = Usuario(
                nombre = request.data.get('nombre'),
                apellidos = "",
                email = email,
                username = ""
            )
            try:
                usuario.save()
            except:
                return Response({'Error':'No se ha podido crear el usuario'},status=status.HTTP_400_BAD_REQUEST)

        usuarioDTO = UsuarioDTO(usuario)
        serializer = UsuarioSerializer(usuarioDTO)        

        return Response(serializer.data,status=status.HTTP_200_OK)