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
        usuario = Usuario.objects.get(id=id)

        usuarioDTO = UsuarioDTO(usuario)

        serializer = UsuarioSerializer(usuarioDTO)

        return Response(serializer.data,status=status.HTTP_200_OK)



# Google Login
class LoginGoogleView(APIView):
    def post(self,request,format=None):
        if request.headers.get('Authorization') is not None:
            
            token = request.headers.get('Authorization')
            idinfo = None
            try:
                idinfo = id_token.verify_oauth2_token(token, transport.requests.Request(), CLIENT_ID)
            except:
                return Response({"mensaje": "Token caducado"}, status=status.HTTP_400_BAD_REQUEST)

            email = idinfo['email']
            usuario = None
            try:
                usuario = Usuario.objects.get(email=email)
            except:

                name = idinfo['given_name']
                try:
                    apellidos = idinfo['family_name']
                except:
                    apellidos = ""
                imagen = idinfo['picture']

                
                usuario = Usuario(
                    email = email,
                    username = "prueba",
                    nombre = name,
                    apellidos = apellidos
                )

                usuario.save()

            userDTO = UsuarioDTO(usuario)
            serializer = UsuarioSerializer(userDTO)
            return Response(serializer.data,status=status.HTTP_200_OK)

        else :
            return Response({"mensaje" : "Es necesario el header Authorization"}, status=status.HTTP_400_BAD_REQUEST)

class LoginGoogleCheckView(APIView):
    def post(self,request,format=None):
        if request.headers.get('Authorization') is not None:
            
            token = request.headers.get('Authorization')
            idinfo = None
            try:
                id_token.verify_oauth2_token(token, transport.requests.Request(), CLIENT_ID)
            except:
                return Response({"mensaje": "caducado"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"mensaje" : "ok"},status=status.HTTP_200_OK)

        else :
            return Response({"mensaje" : "header"}, status=status.HTTP_400_BAD_REQUEST)