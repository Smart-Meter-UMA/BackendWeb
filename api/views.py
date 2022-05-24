from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.dto import CompartidoObtencionDTO, DispositivoObtenerByIdDTO, HogarObtenerByIdDTO, HogarObtenerDTO, InvitacionDTO, InvtiacionsRecibidasDTO, MedidaDTO, MedidaObtenerDTO, UsuarioObtenerDTO
from api.models import Compartido, Estadistica, Hogar, Dispositivo, Invitacion, Medida, Usuario
from api.serializers import CompartidoCrearSerializer, CompartidoObtencionSerializer, DispositivoActualizarSerializer, DispositivoCrearSerializer, DispositivoObtenerByIdSerializer, HogarCrearSerializer, HogarObtenerByIdSerializer, HogarObtenerSerializer, InvitacionCrearSerializer, InvitacionEnviadasSerializer, InvitacionRecibidasSerializer, MedidaCrearSerializer, MedidaObtenerSerializer, UsuarioModificarSerializer, UsuarioObtenerSerializer
from datetime import datetime
from google.oauth2 import id_token
from google.auth import transport
import math 
import jwt

#CLIENT_ID = "724046535439-cch2rhprjcdak84a6id2jqckbt8d5ngf.apps.googleusercontent.com"
#CLIENT_ID = "724046535439-h28ieq17aff119i367el50skelqkdgh4.apps.googleusercontent.com"
CLIENT_ID = "724046535439-g4gdj010v7qdkpbcpu7qq9edjt61nbva.apps.googleusercontent.com"
TIEMPO_MEDIDA_ESTANDAR = 10 #Segundos
TIEMPO_REFRESCO_ESTANDAR = 15 #Minutos
VOLTAJE_ESTANDAR = 230 #Voltios
DESFASE_ESTANDAR = 1 
ALGORITMO_JWT = ["HS256"]
KEY_SECRECT = "key"

def autorizar_usuario(request,login):
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
            if login == True:
                usuario = Usuario(
                    nombre=idinfo['given_name'],
                    apellidos=idinfo['family_name'],
                    email=email
                ) 
                usuario.save()
                return usuario
            else:
                return None        
    else:
        return None

def autorizar_dispositivo(request):
    if request.headers.get('Authorization') is not None:
        token = request.headers.get('Authorization')
        dispositivo = jwt.decode(token, key=KEY_SECRECT, algorithms=ALGORITMO_JWT)
        try:
            return Dispositivo.objects.get(id=dispositivo.id)
        except:
            return None
    else:
        return None

def calcularPotencia(voltaje, intensidad, desfase):
    #TODO FALTA CALCULAR LA POTENCIA Y VER SI LO DEL DESFASE VA ASI
    return voltaje * intensidad * math.cos(desfase)

def obtenerNumDia(mes,anio):
    if (mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12): 
        return 31
    
    if (mes == 4 or mes == 6 or mes == 9 or mes == 11):
        return 30
    
    if (mes == 2 and ((anio % 4 == 0) and ((anio % 100 != 0) or (anio % 400 == 0)))):
        return 29
    
    if (mes == 2 and not((anio % 4 == 0) and ((anio % 100 != 0) or (anio % 400 == 0)))):
        return 28
    
    return None

def guardarEstadistica(idDispositivo, kw):
    ahora = datetime.now()

    estadistica = Estadistica.objects.get(dispositivo__id=idDispositivo)

    estadistica.sumaTotalKW = estadistica.sumaTotalKW + kw

    hoyUltHora = datetime(year=estadistica.fechaDia.year,month=estadistica.fechaDia.month,day=estadistica.fechaDia.day,hour=23,minute=59,second=59)
    ultDiaMes = datetime(year=estadistica.fechaMes.year,month=estadistica.fechaMes.month,day=obtenerNumDia(estadistica.fechaMes.month,estadistica.fechaMes.year),hour=23,minute=59,second=59)
    
    if ahora > hoyUltHora:
        estadistica.sumaDiaKW = estadistica.sumaDiaKW + kw
    else:
        estadistica.numDiasTotal = estadistica.numDiasTotal + 1
        if estadistica.minDiaKw > estadistica.sumaDiaKW:
            estadistica.fechaMinDiaKwh = datetime(year=estadistica.fechaDia.year,month=estadistica.fechaDia.month,day=estadistica.fechaDia.day,hour=0,minute=0,second=0)
            estadistica.minDiaKw = estadistica.sumaDiaKW
        if estadistica.maxDiaKw < estadistica.sumaDiaKW:
            estadistica.fechaMaxDiaKwh = datetime(year=estadistica.fechaDia.year,month=estadistica.fechaDia.month,day=estadistica.fechaDia.day,hour=0,minute=0,second=0)
            estadistica.maxDiaKw = estadistica.sumaDiaKW
        estadistica.sumaDiaKW = kw

        estadistica.fechaDia = datetime(year=ahora.year,month=ahora.month,day=ahora.day)

    if ahora > ultDiaMes:
        estadistica.sumaMesKW = estadistica.sumaMesKW + kw
    else:
        estadistica.numMesTotal = estadistica.numMesTotal + 1
        if estadistica.minMesKw > estadistica.sumaMesKW:
            estadistica.fechaMinMesKwh = datetime(year=estadistica.fechaMes.year,month=estadistica.fechaMes.month,day=1,hour=0,minute=0,second=0)
            estadistica.minMesKw = estadistica.sumaMesKW
        if estadistica.maxMesKw < estadistica.sumaMesKW:
            estadistica.fechaMaxMesKwh = datetime(year=estadistica.fechaMes.year,month=estadistica.fechaMes.month,day=1,hour=0,minute=0,second=0)
            estadistica.maxMesKw = estadistica.sumaMesKW
        
        estadistica.sumaMesKW = kw

        estadistica.fechaMes = datetime(year=ahora.year,month=ahora.month,day=1)

# Create your views here.

# /usuarios
class UsuarioView(APIView):
    def get(self,request,format=None):
        usuario = autorizar_usuario(request,False)
        if usuario == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        usuarios = Usuario.objects.all()

        if request.query_params.get("email") is not None:
            usuarios = usuarios.filter(email__icontains=request.query_params.get("email"))
        
        if request.query_params.get("nombre") is not None:
            usuarios = usuarios.filter(nombre__icontains=request.query_params.get("nombre"))

        if request.query_params.get("apellidos") is not None:
            usuarios = usuarios.filter(apellidos__icontains=request.query_params.get("apellidos"))

        usuariosDTO = UsuarioObtenerDTO.toUsuarioObtenerDTO(usuarios)

        serializer = UsuarioObtenerSerializer(usuariosDTO,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":usuarios.count()})
    
class UsuarioIDView(APIView): 
    def put(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        if usuarioToken.id != id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            usuario = Usuario.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un usuario con ese ID."},status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsuarioModificarSerializer(data=request.data)
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
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        if usuarioToken.id != id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            usuario = Usuario.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un usuario con ese ID"},status=status.HTTP_404_NOT_FOUND)
        try:
            usuario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar un usuario con ese ID"},status=status.HTTP_400_BAD_REQUEST)


#/hogars
class HogarView(APIView):
    def get(self,request,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        hogars = Hogar.objects.filter(owner__id=usuarioToken.id)

        compartidos = Compartido.objects.filter(compartido__id=usuarioToken.id)

        count = hogars.count() + compartidos.count()

        hogarsDto = HogarObtenerDTO.toHogarObtenerDTO(hogars,compartidos)

        serializer = HogarObtenerSerializer(hogarsDto,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":count})

    def post(self,request,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = HogarCrearSerializer(data=request.data)
        if serializer.is_valid():
            hogar = Hogar(
                nombre = serializer.validated_data.get("nombre"),
                potencia_contratada = serializer.validated_data.get("potencia_contratada"),
                owner = usuarioToken
            )
            try:
                hogar.save()
                return Response(data={"id":hogar.id},status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: El hogar no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del hogar es incorrecto."},status=status.HTTP_400_BAD_REQUEST)


#/hogars/:id
class HogarIDView(APIView):
    def get(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            hogar = Hogar.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado ese hogar con ese ID"},status=status.HTTP_404_NOT_FOUND)

        compartido = Compartido.objects.filter(compartido__id=usuarioToken.id)
        compartido = compartido.filter(hogarCompartido__id=hogar.id)
        if compartido.count() == 0 and hogar.owner.id != usuarioToken.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        dispositivos = Dispositivo.objects.filter(hogar__id=id)

        hogarDto = HogarObtenerByIdDTO(hogar,dispositivos,hogar.owner.id == usuarioToken.id)

        serializer = HogarObtenerByIdSerializer(hogarDto)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            hogar = Hogar.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un hogar con ese ID."},status=status.HTTP_404_NOT_FOUND)
        
        if hogar.owner.id != usuarioToken.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        serializer = HogarCrearSerializer(data=request.data)
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
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            hogar = Hogar.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un hogar con ese ID."},status=status.HTTP_404_NOT_FOUND)
        
        if hogar.owner.id != usuarioToken.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            hogar.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar un hogar con ese ID"},status=status.HTTP_400_BAD_REQUEST)

#/hogars/:id/compartidos
class HogarsIDCompartidosView(APIView):
    def get(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            hogar = Hogar.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un hogar con ese ID."},status=status.HTTP_404_NOT_FOUND)

        if hogar.owner.id != usuarioToken.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            compartidos = Compartido.objects.filter(hogarCompartido__id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado los dispisitivos de esa hogar con ese ID"},status=status.HTTP_404_NOT_FOUND)

        compartidoDTO = CompartidoObtencionDTO.toCompartidoObtencionDTO(compartidos=compartidos)
        serializer = CompartidoObtencionSerializer(compartidoDTO,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":compartidos.count()})

#/dispositivos
class DispositivosView(APIView):
    def post(self,request,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        serializer = DispositivoCrearSerializer(data=request.data)
        if serializer.is_valid():
            dispositivo = Dispositivo(
                nombre = serializer.validated_data.get("nombre"),
                notificacion = False,
                general = False,
                limite_minimo = 0,
                limite_maximo = 0,
                tiempo_medida = TIEMPO_MEDIDA_ESTANDAR,
                tiempo_refresco = TIEMPO_REFRESCO_ESTANDAR,
                hogar = Hogar.objects.get(id=serializer.validated_data.pop("hogar").get("id"))
            )
            try:
                dispositivo.save()
                ahora = datetime.now()
                estadistica = Estadistica(
                    dispositivo = dispositivo,
                    fechaDia = datetime(year=ahora.year,month=ahora.month,day=ahora.day),
                    sumaDiaKW = 0,
                    fechaMes = datetime(year=ahora.year,month=ahora.month,day=1),
                    sumaMesKW = 0,
                    sumaTotalKW = 0,
                    numDiasTotal = 1,
                    numMesTotal = 1,
                    minDiaKw = 0,
                    maxDiaKw = 0,
                    minMesKw = 0,
                    maxMesKw = 0,
                    fechaMinDiaKwh = ahora,
                    fechaMaxDiaKwh = ahora,
                    fechaMinMesKwh = ahora,
                    fechaMaxMesKwh = ahora
                )
                estadistica.save()
                token = jwt.encode(dispositivo,key=KEY_SECRECT,algorithm=ALGORITMO_JWT)
                return Response({"token" : token},status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: El dispositivo no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del dispositivo es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

#/dispositivos/:id
class DispositivoIDView(APIView):
    def get(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            dispositivo = Dispositivo.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado ese dispositivo con ese ID"},status=status.HTTP_404_NOT_FOUND)

        compartido = Compartido.objects.filter(hogarCompartido__id=dispositivo.hogar.id)
        compartido = compartido.filter(compartido__id=usuarioToken.id)

        if compartido.count() == 0 and usuarioToken.id != dispositivo.hogar.owner.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        estadistica = Estadistica.objects.get(dispositivo__id=id)
        dispositivoDTO = DispositivoObtenerByIdDTO(dispositivo,estadistica)
        serializer = DispositivoObtenerByIdSerializer(dispositivoDTO)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            dipositivo = Dispositivo.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un dispositivo con ese ID."},status=status.HTTP_404_NOT_FOUND)
        
        if usuarioToken.id != dipositivo.hogar.owner.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        
        serializer = DispositivoActualizarSerializer(data=request.data)
        if serializer.is_valid():
            dipositivo.nombre = serializer.validated_data.get("nombre")
            dipositivo.notificacion = serializer.validated_data.get("notificacion")
            dipositivo.general = serializer.validated_data.get("general")
            dipositivo.limite_minimo = serializer.validated_data.get("limite_minimo")
            dipositivo.limite_maximo = serializer.validated_data.get("limite_maximo")
            dipositivo.tiempo_medida = serializer.validated_data.get("tiempo_medida")
            dipositivo.tiempo_refrescado = serializer.validated_data.get("tiempo_refrescado")
            dipositivo.potencia_contratada = serializer.validated_data.get("potencia_contratada"),
            try:
                dipositivo.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"mensaje":"Error: El dispositivo no ha podido ser actualizado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del dispositivo es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            dispositivo = Dispositivo.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado un dispositivo con ese ID."},status=status.HTTP_404_NOT_FOUND)
        
        if usuarioToken.id != dispositivo.hogar.owner.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            dispositivo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar un dispositivo con ese ID"},status=status.HTTP_400_BAD_REQUEST)



#/dispositivos/:id/medidas
class DispositivoIDMedidadView(APIView):
    def get(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            dispositivo = Dispositivo.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado ese dispositivo con ese ID"},status=status.HTTP_404_NOT_FOUND)

        compartido = Compartido.objects.filter(hogarCompartido__id=dispositivo.hogar.id)
        compartido = compartido.filter(compartido__id=usuarioToken.id)

        if compartido.count() == 0 and usuarioToken.id != dispositivo.hogar.owner.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            medidas = Medida.objects.get(dispositivo__id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado las medidas de ese dispositivo con ese ID"},status=status.HTTP_404_NOT_FOUND)

        medidasDTO = MedidaObtenerDTO.toMedidaObtenerDTO(medidas)
        serializer = MedidaObtenerSerializer(medidasDTO,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":medidas.count()})

#/medidas
class MedidaView(APIView):
    def get(self,request,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        medidas = Medida.objects.all()

        medidasDTO = MedidaObtenerDTO.toMedidaObtenerDTO(medidas)
        serializer = MedidaObtenerSerializer(medidasDTO,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":medidas.count()})

    def post(self,request,format=None):
        dispositivo = autorizar_dispositivo(request)
        if dispositivo == None:
            return Response({"mensage":"Dispositivo no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        listaKwTiempo = []
        for medida in request.data:
            serializer = MedidaCrearSerializer(data=medida)
            if serializer.is_valid():
                voltaje = serializer.validated_data.get("voltaje") if serializer.validated_data.get("voltaje") != None else VOLTAJE_ESTANDAR
                desfase = serializer.validated_data.get("desfase") if serializer.validated_data.get("desfase") != None else DESFASE_ESTANDAR
                kw = calcularPotencia(intensidad=serializer.validated_data.get("intensidad"),voltaje=voltaje,desfase=desfase)
                listaKwTiempo.append((kw,serializer.validated_data.get("fecha")))
                medida = Medida(
                    dispositivo = dispositivo,
                    fecha = serializer.validated_data.get("fecha"),
                    intensidad = serializer.validated_data.get("intensidad"),
                    voltaje = serializer.validated_data.get("voltaje"),
                    kw = kw
                )
                try:
                    medida.save()
                except:
                    return Response({"mensaje":"Error: La medida no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"mensaje":"Error: El formato de la medida es incorrecto."},status=status.HTTP_400_BAD_REQUEST)
        
        guardarEstadistica(dispositivo.id,listaKwTiempo)
        return Response({"tiempoRecogidaMedida":dispositivo.tiempo_medida,"tiempoActualizacionMedida":dispositivo.tiempo_refrescado})

#ofrecerInvitacion/
class OfrecerInvitacionView(APIView):
    def post(self,request, format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        serializer = InvitacionCrearSerializer(data=request.data)
        if serializer.is_valid():
            hogar = Hogar.objects.get(id=serializer.validated_data.pop("hogarInvitado").get("id"))
            if hogar.owner.id != usuarioToken.id:
                return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
            try: 
                invitado_aux = Usuario.objects.filter(email__iexact=serializer.validated_data.get("correoInvitado")).first()
            except:
                return Response({"mensaje":"Error: No existe usuario con ese email en la plataforma"},status=status.HTTP_400_BAD_REQUEST)

            ya_invitado = Invitacion.objects.filter(invitado = invitado_aux, hogarInvitado = hogar, invitante = usuarioToken)
            if ya_invitado.count() == 0 :
                invitacion = Invitacion(
                    invitado = invitado_aux,
                    hogarInvitado = hogar,
                    invitante = usuarioToken
                )
                try:
                    invitacion.save()
                    return Response(status=status.HTTP_201_CREATED)
                except:
                    return Response({"mensaje":"Error: La invitación no ha podido ser creada"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"mensaje":"Error: Hay ya una invitación pendiente."},status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"mensaje":"Error: El formato de la invitación es incorrecto."},status=status.HTTP_400_BAD_REQUEST)


#invitacionRecibidas/
class InvitacionsRecibidasView(APIView):
    def get(self,request,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        invitacions = Invitacion.objects.filter(invitado__id=usuarioToken.id)

        invitacionsDTO = InvtiacionsRecibidasDTO.toInvtiacionsRecibidasDTO(invitacions)

        serializers = InvitacionRecibidasSerializer(invitacionsDTO,many=True)

        return Response(serializers.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":invitacions.count()})

#invitacions/:id
class InvitacionsIDView(APIView):
    def delete(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            invitacion = Invitacion.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado una invitacion con ese ID"},status=status.HTTP_404_NOT_FOUND)
        
        if invitacion.invitado.id != usuarioToken.id and invitacion.invitante.id != usuarioToken.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            invitacion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar un dispositivo con ese ID"},status=status.HTTP_400_BAD_REQUEST)

#/compartidos
class CompartidoView(APIView):
    def post(self,request,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        serializer = CompartidoCrearSerializer(data=request.data)
        if serializer.is_valid():
            invitacion = Invitacion.objects.filter(hogarInvitado__id=serializer.validated_data.pop("hogarCompartido").get("id"))
            invitacion = invitacion.filter(invitado__id=usuarioToken.id)
            if invitacion.count() == 0:
                return Response({"mensage":"No tienes invtación para compartir"},status=status.HTTP_400_BAD_REQUEST)
            else:
                invitacion.delete()

            compartido = Compartido(
                compartido = usuarioToken,
                hogarCompartido = Hogar.objects.get(id=serializer.validated_data.pop("hogarCompartido").get("id"))                
            )
            try:
                compartido.save()
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: La compartición no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del dispositivo es incorrecto."},status=status.HTTP_400_BAD_REQUEST)
#/compartidos/:id
class CompartidosIDView(APIView):
    def delete(self,request,id,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        try:
            compartido = Compartido.objects.get(id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado una comparticion con ese ID"},status=status.HTTP_404_NOT_FOUND)
        
        if(compartido.hogarCompartido.owner.id != usuarioToken.id):
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        try:
            compartido.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar ese compartido con ese ID"},status=status.HTTP_400_BAD_REQUEST)
#/login
class LoginView(APIView):
    def post(self,request,format=None):
        usuarioToken = autorizar_usuario(request,True)
        if usuarioToken == None:
            return Response(data={"mensaje":"Token no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        usuarioDTO = UsuarioObtenerDTO(usuarioToken)
        serializers = UsuarioObtenerSerializer(usuarioDTO)
        return Response(serializers.data,status=status.HTTP_200_OK)
        