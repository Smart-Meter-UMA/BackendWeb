from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.dto import CompartidoDTO, DispositivoDTO, HogarDTO, InvitacionDTO, MedidaDTO, UsuarioDTO
from api.models import Compartido, Hogar, Dispositivo, Invitacion, Medida, Usuario
from api.serializers import CompartidoSerializer, DispositivoSerializer, HogarSerializer, InvitacionSerializer, MedidaSerializer, UsuarioSerializer
from datetime import datetime, timedelta

def calcularPotencia(voltaje, intensidad):
    return voltaje * intensidad


# Create your views here.

# /usuarios
class UsuarioView(APIView):
    def get(self,request,format=None):
        usuarios = Usuario.objects.all()

        usuariosDTO = UsuarioDTO.toUsuariosDTO(usuarios)

        serializer = UsuarioSerializer(usuariosDTO,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":usuarios.count()})

    def post(self,request,format=None):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = Usuario(
                nombre = serializer.validated_data.get("nombre"),
                apellidos = serializer.validated_data.get("apellidos"),
                username = serializer.validated_data.get("username"),
                email = serializer.validated_data.get("email")
            )
            try:
                usuario.save()
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: El usuario no ha podido ser crear."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del usuario es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

#/usuarios/:id
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

#/usuarios/:id/hogars
class UsuariosIDHogaresView(APIView):
    def get(self,request,id,format=None):
        try:
            hogars = Hogar.objects.get(owner__id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un usuario con ese ID"},status=status.HTTP_404_NOT_FOUND)

        hogarsDTO = HogarDTO.toHogarsDTO(hogars)
        serializer = HogarSerializer(hogarsDTO,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":hogars.count()})

#/usuarios/:id/invitacions
class UsuariosIDInvitacionsView(APIView):
    def get(self,request,id,format=None):
        try:
            invitacions = Invitacion.objects.filter(invitado__id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado las invitaciones del invitado con ese ID"},status=status.HTTP_404_NOT_FOUND)

        invitacionsDTO = InvitacionDTO.toInvitacionDTO(invitacions)
        serializer = InvitacionSerializer(invitacionsDTO,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":invitacions.count()})



#/hogars
class HogarView(APIView):
    def get(self,request,format=None):
        hogars = Hogar.objects.all()

        hogarsDto = HogarDTO.toHogarsDTO(hogars)

        serializer = HogarSerializer(hogarsDto,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":hogars.count()})

    def post(self,request,format=None):
        serializer = HogarSerializer(data=request.data)
        if serializer.is_valid():
            hogar = Hogar(
                nombre = serializer.validated_data.get("nombre"),
                potencia_contratada = serializer.validated_data.get("potencia_contratada"),
                owner = Usuario.objects.get(id=serializer.validated_data.pop("owner").get("id"))
            )
            try:
                hogar.save()
                hogarDto = HogarDTO(hogar)
                serializer = HogarSerializer(hogarDto)
                return Response(data=serializer.data,status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: El hogar no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del hogar es incorrecto."},status=status.HTTP_400_BAD_REQUEST)


#/hogars/:id
class HogarIDView(APIView):
    def get(self,request,id,format=None):
        try:
            hogar = Hogar.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado ese hogar con ese ID"},status=status.HTTP_404_NOT_FOUND)

        hogarDto = HogarDTO(hogar)

        serializer = HogarSerializer(hogarDto)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id,format=None):
        try:
            hogar = Hogar.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un hogar con ese ID."},status=status.HTTP_404_NOT_FOUND)
        serializer = HogarSerializer(data=request.data)
        if serializer.is_valid():
            hogar.nombre = serializer.validated_data.get("nombre")
            hogar.potencia_contratada = serializer.validated_data.get("potencia_contratada")
            try:
                hogar.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"mensaje":"Error: El hogar no ha podido ser actualizado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del hogar es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        try:
            hogar = Hogar.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un hogar con ese ID"},status=status.HTTP_404_NOT_FOUND)
        try:
            hogar.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar un hogar con ese ID"},status=status.HTTP_400_BAD_REQUEST)

#/hogars/:id/dispositivos
class HogarsIDispositivosView(APIView):
    def get(self,request,id,format=None):
        try:
            dispositivos = Dispositivo.objects.filter(hogar__id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado los dispisitivos de esa hogar con ese ID"},status=status.HTTP_404_NOT_FOUND)

        dipositivosDTO = DispositivoDTO.toDispositivoDTO(dispositivos)
        serializer = DispositivoSerializer(dipositivosDTO,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":dispositivos.count()})

#/hogars/:id/compartidos
class HogarsIDCompartidosView(APIView):
    def get(self,request,id,format=None):
        try:
            compartidos = Compartido.objects.filter(hogarCompartido__id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado los dispisitivos de esa hogar con ese ID"},status=status.HTTP_404_NOT_FOUND)

        compartidoDTO = CompartidoDTO.toCompartidoDTO(compartidos)
        serializer = CompartidoSerializer(compartidoDTO,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":compartidos.count()})


#/dispositivos
class DispositivosView(APIView):
    def get(self,request,format=None):
        dispositivos = Dispositivo.objects.all()

        dispositivosDTO = DispositivoDTO.toDispositivoDTO(dispositivos)

        serializer = DispositivoSerializer(dispositivosDTO,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":dispositivos.count()})

    def post(self,request,format=None):
        #Falta por ver como se hace
        serializer = DispositivoSerializer(data=request.data)
        if serializer.is_valid():
            dispositivo = Dispositivo(
                nombre = serializer.validated_data.get("nombre"),
                potencia_contratada = serializer.validated_data.get("potencia_contratada"),
                hogar = Hogar.objects.get(id=serializer.validated_data.pop("hogar").get("id"))
            )
            try:
                dispositivo.save()
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: El dispositivo no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del dispositivo es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

#/dispositivos/:id
class DispositivoIDView(APIView):
    def get(self,request,id,format=None):
        try:
            dispositivo = Dispositivo.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado ese dispositivo con ese ID"},status=status.HTTP_404_NOT_FOUND)

        dispositivoDTO = DispositivoDTO(dispositivo)

        serializer = DispositivoSerializer(dispositivoDTO)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id,format=None):
        try:
            dipositivo = Dispositivo.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un dispositivo con ese ID."},status=status.HTTP_404_NOT_FOUND)
        serializer = HogarSerializer(data=request.data)
        if serializer.is_valid():
            dipositivo.nombre = serializer.validated_data.get("nombre"),
            dipositivo.potencia_contratada = serializer.validated_data.get("potencia_contratada"),
            try:
                dipositivo.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"mensaje":"Error: El dispositivo no ha podido ser actualizado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del dispositivo es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        try:
            dispositivo = Dispositivo.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un dispositivo con ese ID"},status=status.HTTP_404_NOT_FOUND)
        try:
            dispositivo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar un dispositivo con ese ID"},status=status.HTTP_400_BAD_REQUEST)

#/dispositivos/:id/medidas
class DispositivoIDMedidadView(APIView):
    def get(self,request,id,format=None):
        try:
            medidas = Medida.objects.get(dispositivo__id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado las medidas de ese dispositivo con ese ID"},status=status.HTTP_404_NOT_FOUND)

        medidasDTO = MedidaDTO.toMedidaDTO(medidas)
        serializer = MedidaSerializer(medidasDTO,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":medidas.count()})


#/medidas
class MedidaView(APIView):
    def get(self,request,format=None):
        medidas = Medida.objects.all()

        medidasDTO = MedidaDTO.toMedidaDTO(medidas)

        serializer = MedidaSerializer(medidasDTO,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":medidas.count()})

    def post(self,request,format=None):
        #Falta por ver que me envia
        serializer = MedidaSerializer(data=request.data)
        if serializer.is_valid():
            kw = calcularPotencia(intensidad=serializer.validated_data.get("intensidad"),voltaje=serializer.validated_data.get("voltaje"))
            medida = Medida(
                #dispositivo
                fecha = datetime.now(),
                intensidad = serializer.validated_data.get("intensidad"),
                voltaje = serializer.validated_data.get("voltaje"),
                kw = kw
            )
            try:
                medida.save()
                #guardarEstadistica(idDispositivo,kw,datetime.now())
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: La medida no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato de la medida es incorrecto."},status=status.HTTP_400_BAD_REQUEST)


#invitacions/:id
class InvitacionsIDView(APIView):
    def delete(self,request,id,format=None):
        try:
            invitacion = Invitacion.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado una invitacion con ese ID"},status=status.HTTP_404_NOT_FOUND)
        try:
            invitacion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar un dispositivo con ese ID"},status=status.HTTP_400_BAD_REQUEST)

#/compartidos
class CompartidoView(APIView):
    def post(self,request,format=None):
        serializer = CompartidoSerializer(data=request.data)
        if serializer.is_valid():
            compartido = Compartido(
                compartido = Usuario.objects.get(id=serializer.validated_data.pop("compartido").get("id")),
                hogarCompartido = Hogar.objects.get(id=serializer.validated_data.pop("hogarCompartido").get("id"))                
            )
            try:
                compartido.save()
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: El dispositivo no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del dispositivo es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

#/compartidos/:id
class CompartidosIDView(APIView):
    def delete(self,request,id,format=None):
        try:
            compartido = Compartido.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado una comparticion con ese ID"},status=status.HTTP_404_NOT_FOUND)
        try:
            compartido.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar ese compartido con ese ID"},status=status.HTTP_400_BAD_REQUEST)





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