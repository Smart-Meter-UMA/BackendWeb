from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.dto import CompartidoObtencionDTO, DispositivoObtenerByIdDTO, HogarObtenerByIdDTO, HogarObtenerDTO, InvitacionDTO, InvtiacionsRecibidasDTO, MedidaDTO, MedidaObtenerDTO, UsuarioObtenerDTO
from api.models import Compartido, Estadistica, Hogar, Dispositivo, Invitacion, Medida, Usuario
from api.serializers import CompartidoCrearSerializer, CompartidoObtencionSerializer, DispositivoActualizarSerializer, DispositivoCrearSerializer, DispositivoObtenerByIdSerializer, HogarCrearSerializer, HogarObtenerByIdSerializer, HogarObtenerSerializer, InvitacionCrearSerializer, InvitacionEnviadasSerializer, InvitacionRecibidasSerializer, MedidaCrearSerializer, MedidaObtenerSerializer, UsuarioModificarSerializer, UsuarioObtenerSerializer
from datetime import date, datetime, timedelta
from google.oauth2 import id_token
from google.auth import transport
import math 
import jwt
from django.core.mail import EmailMultiAlternatives
import sys
from api.json_file import formato_json_historicoDiario

CLIENT_ID_MOVIL = "724046535439-h28ieq17aff119i367el50skelqkdgh4.apps.googleusercontent.com"
CLIENT_ID_WEB = "724046535439-g4gdj010v7qdkpbcpu7qq9edjt61nbva.apps.googleusercontent.com"
TIEMPO_MEDIDA_ESTANDAR = 10 #Segundos
TIEMPO_REFRESCO_ESTANDAR = 15 #Minutos
VOLTAJE_ESTANDAR = 230 #Voltios
DESFASE_ESTANDAR = 1 
ALGORITMO_JWT = ["HS256"]
KEY_SECRECT = "key"

def enviarCorreoInvitacion(usuarioToken,hogar,invitado_aux):
    html_content = """
        <h1>Hola, """ + invitado_aux.nombre + """</h1><br/>
        Este correo sirve para notificarle de que acaba de recibir una invitación
        de """+usuarioToken.nombre+""" ("""+usuarioToken.email+""") para que pueda
        ver las estadísticas de """+hogar.nombre+"""<br/><br/>

        Recureda que puede aceptar o denegar dicha invitación 
        desde la pagina principal de Kproject<br/><br/>
        <URL_KPROJECT><br/><br/>

        KProject.
    """

    message = EmailMultiAlternatives(
        subject="Nueva invitación",
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[invitado_aux.email],
        cc=[]
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

def enviarCorreoAceptadoInvitacion(usuarioToken,hogarCompartido,invitante):
    html_content = """
        <h1>Hola, """ + invitante.nombre + """</h1><br/>
        Este correo sirve para notificarle de que el usaurio """+usuarioToken.nombre+""" 
        ("""+usuarioToken.email+""") ha aceptado la invitación para que pueda
        ver las estadísticas de """+hogarCompartido.nombre+"""<br/><br/>

        Recureda que puede ver la lista de usuarios compartidos en:<br/><br/>
        <URL_KPROJECT><br/><br/>

        KProject.
    """

    message = EmailMultiAlternatives(
        subject="Invitación aceptada",
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[invitante.email],
        cc=[]
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

def enviarCorreoRechazadoInvitacion(usuarioToken,hogarCompartido,invitante):
    html_content = """
    <h1>Hola, """ + invitante.nombre + """</h1><br/>
    Este correo sirve para notificarle de que el usaurio """+usuarioToken.nombre+""" 
    ("""+usuarioToken.email+""") ha denegado la invitación para que pueda
    ver las estadísticas de """+hogarCompartido.nombre+"""<br/><br/>

    Recureda que puede ver la lista de usuarios compartidos en:<br/><br/>
    <URL_KPROJECT><br/><br/>

    KProject.
    """

    message = EmailMultiAlternatives(
        subject="Invitación denegada",
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[invitante.email],
        cc=[]
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

def enviarCorreoTeHanDejadoCompartir(usuarioToken,hogarCompartido,compartido):
    html_content = """
    <h1>Hola, """ + compartido.nombre + """</h1><br/>
    Este correo sirve para notificarle de que el usaurio """+usuarioToken.nombre+""" 
    ("""+usuarioToken.email+""") ha dejado de compartirle para que pueda
    ver las estadísticas de """+hogarCompartido.nombre+"""<br/><br/>

    Recureda que puede ver la lista de usuarios compartidos en:<br/><br/>
    <URL_KPROJECT><br/><br/>

    KProject.
    """

    message = EmailMultiAlternatives(
        subject="Dejado de compartir",
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[compartido.email],
        cc=[]
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

def enviarCorreoSeHaSalido(usuarioToken,hogarCompartido,invitante):
    html_content = """
    <h1>Hola, """ + invitante.nombre + """</h1><br/>
    Este correo sirve para notificarle de que el usaurio """+usuarioToken.nombre+""" 
    ("""+usuarioToken.email+""") ha abandonado para que pueda
    ver las estadísticas de """+hogarCompartido.nombre+"""<br/><br/>

    KProject.
    """

    message = EmailMultiAlternatives(
        subject="Hogar abandonado",
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[invitante.email],
        cc=[]
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

def enviarCorreoNotificacionLimiteMaximo(estadistica,actual):
    html_content = """
    <h1>Hola, """ + estadistica.dispositivo.hogar.owner.nombre + """</h1><br/>
    Este correo sirve para notificarle de que el dispositivo"""+estadistica.dispositivo.nombre+"""
    ha excedido su limite diario máximo:<br/><br/>
        Limite máximo: """+str(estadistica.dispositivo.limite_maximo)+"""<br/><br/>
        Actual: """+str(actual)+"""<br/><br/>

    Esto lo puedes ver a través de la pagina de Kproject:<br/><br/>
    URLKPROJECT


    KProject.
    """

    message = EmailMultiAlternatives(
        subject="Hogar abandonado",
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[estadistica.dispositivo.hogar.owner.email],
        cc=[]
    )

    message.attach_alternative(html_content, "text/html")
    message.send()

def autorizar_usuario(request,login):
    if request.headers.get('Authorization') is not None:
        token = request.headers.get('Authorization')
        idinfo = None
        try:
            idinfo = id_token.verify_oauth2_token(token, transport.requests.Request(), CLIENT_ID_WEB)
        except:
            try:
                idinfo = id_token.verify_oauth2_token(token, transport.requests.Request(), CLIENT_ID_MOVIL)
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
                    email=email,
                    notificacion_invitados = False
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
            return Dispositivo.objects.get(id=dispositivo.get('id'))
        except:
            return None
    else:
        return None

def calcularPotencia(voltaje, intensidad, desfase):
    #TODO FALTA CALCULAR LA POTENCIA Y VER SI LO DEL DESFASE VA ASI
    return (voltaje * intensidad) / 1000

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

def guardarEstadistica(idDispositivo, listaKwTiempo):
    ahora = datetime.now()

    #1º Calculo el tiempo transcurrido entre la primera medida y la ultima
    fechaInicio = listaKwTiempo[0]["tiempo"]
    fechaFin = listaKwTiempo[-1]["tiempo"]

    tiempoTranscurridoHoras = (fechaFin - fechaInicio).total_seconds() / (60 * 60)

    #2º Calculo todos los kw que se han recodigo
    estadistica = Estadistica.objects.get(dispositivo__id=idDispositivo)

    kwh = 0 
    cont = 0
    kwh_horas = 0 

    for medida in listaKwTiempo:
        if listaKwTiempo[-1]["tiempo"] != listaKwTiempo[cont]["tiempo"]:
            kwh += (medida["kw"] * ((listaKwTiempo[cont+1]["tiempo"] - medida["tiempo"]).total_seconds() / (60 * 60)))
            kwh_horas += (medida["kw"] * ((listaKwTiempo[cont+1]["tiempo"] - medida["tiempo"]).total_seconds() / (60 * 60)))
            if listaKwTiempo[cont+1]["tiempo"].strftime("%H") > medida["tiempo"].strftime("%H"):
                estadistica.tramosHistoricoHoras[medida["tiempo"].strftime("%H")+':00'] = estadistica.tramosHistoricoHoras[medida["tiempo"].strftime("%H")+':00'] + kwh_horas
                kwh_horas = 0
        cont += 1
    
    estadistica.tramosHistoricoHoras[listaKwTiempo[-1]["tiempo"].strftime("%H")+':00'] = estadistica.tramosHistoricoHoras[listaKwTiempo[-1]["tiempo"].strftime("%H")+':00'] + kwh_horas

    #3º Calculo los kwh de estas medidas
    
    estadistica.sumaTotalKw = estadistica.sumaTotalKw + kwh
    hoyUltHora = datetime(year=estadistica.fechaDia.year,month=estadistica.fechaDia.month,day=estadistica.fechaDia.day,hour=23,minute=59,second=59,microsecond=999999)
    ultDiaMes = datetime(year=estadistica.fechaMes.year,month=estadistica.fechaMes.month,day=obtenerNumDia(estadistica.fechaMes.month,estadistica.fechaMes.year),hour=23,minute=59,second=59, microsecond=999999)
    ultDiaSemana = datetime(year=estadistica.fechaSemana.year,month=estadistica.fechaSemana.month,day=(estadistica.fechaSemana + timedelta( (6-estadistica.fechaSemana.weekday()) % 7 )).day,hour=23,minute=59,second=59, microsecond=999999)
    ultDiaAño = datetime(year=estadistica.fechaAño.year,month=12, day= 31,hour=23,minute=59,second=59, microsecond=999999)


    if ahora <= hoyUltHora:
        estadistica.sumaDiaKw = estadistica.sumaDiaKw + kwh
    else:
        dia_anterior = ahora - timedelta(days=1)
        energia_consumida_diaria_aproximacion = estadistica.sumaDiaKw / 24
        formato_json_historicoDiario['dia'] = dia_anterior.day 
        formato_json_historicoDiario['mes'] = dia_anterior.month
        formato_json_historicoDiario['year'] = dia_anterior.year
        formato_json_historicoDiario['energia_consumida'] = energia_consumida_diaria_aproximacion
        estadistica.historicoDiario['list'].append(formato_json_historicoDiario)
        estadistica.numDiasTotal = estadistica.numDiasTotal + 1

        if estadistica.minDiaKw > estadistica.sumaDiaKw:
            estadistica.fechaMinDiaKw = datetime(year=estadistica.fechaDia.year,month=estadistica.fechaDia.month,day=estadistica.fechaDia.day,hour=0,minute=0,second=0)
            estadistica.minDiaKw = estadistica.sumaDiaKw

        if estadistica.maxDiaKw < estadistica.sumaDiaKw:
            estadistica.fechaMaxDiaKw = datetime(year=estadistica.fechaDia.year,month=estadistica.fechaDia.month,day=estadistica.fechaDia.day,hour=0,minute=0,second=0)
            estadistica.maxDiaKw = estadistica.sumaDiaKw

        if estadistica.sumaDiaKw > estadistica.consumoDiaMasConsumidoHistoricamente:        
            estadistica.diaMasConsumidoHistoricamente = datetime.today()
            estadistica.consumoDiaMasConsumidoHistoricamente = estadistica.sumaDiaKw

        if ahora <= ultDiaSemana:
            if estadistica.sumaDiaKw > estadistica.consumoDiaMasConsumidoSemana:
                estadistica.diaMasConsumidoSemana = datetime.today()
                estadistica.consumoDiaMasConsumidoSemana = estadistica.sumaDiaKw
        else:
            estadistica.fechaSemana = datetime.today()
            estadistica.consumoDiaMasConsumidoSemana = 0.0

        if ahora <= ultDiaMes:
            if estadistica.sumaDiaKw > estadistica.consumoDiaMasConsumidoMes:
                estadistica.diaMasConsumidoMes = datetime.today()
                estadistica.consumoDiaMasConsumidoMes = estadistica.sumaDiaKw
        else:
            estadistica.consumoDiaMasConsumidoMes = 0.0

        if ahora <= ultDiaAño: 
            if estadistica.sumaDiaKw > estadistica.consumoDiaMasConsumidoAño:
                estadistica.diaMasConsumidoAño = datetime.today()
                estadistica.consumoDiaMasConsumidoAño = estadistica.sumaDiaKw
        else:
            estadistica.fechaAño = datetime.today()
            estadistica.consumoDiaMasConsumidoAño = 0.0
        
        estadistica.sumaDiaKw = kwh
        dia = (estadistica.fechaDia.day + 1)%obtenerNumDia(estadistica.fechaDia.month,estadistica.fechaDia.year)
        if dia == 1:
            mes = (estadistica.fechaDia.month + 1)%12
        else:
            mes = estadistica.fechaDia.month
        
        if mes == 1:
            anio = estadistica.fechaDia.year + 1
        else:
            anio = estadistica.fechaDia.year

        estadistica.fechaDia = datetime(year=anio,month=mes,day=dia)
        estadistica.sumaDiaDinero = 0.0
    
    if ahora <= ultDiaMes:
        estadistica.sumaMesKw = estadistica.sumaMesKw + kwh
    else:
        estadistica.numMesTotal = estadistica.numMesTotal + 1
        if estadistica.minMesKw > estadistica.sumaMesKw:
            estadistica.fechaMinMesKwh = datetime(year=estadistica.fechaMes.year,month=estadistica.fechaMes.month,day=1,hour=0,minute=0,second=0)
            estadistica.minMesKw = estadistica.sumaMesKw
        if estadistica.maxMesKw < estadistica.sumaMesKw:
            estadistica.fechaMaxMesKwh = datetime(year=estadistica.fechaMes.year,month=estadistica.fechaMes.month,day=1,hour=0,minute=0,second=0)
            estadistica.maxMesKw = estadistica.sumaMesKw
        
        estadistica.sumaMesKw = kwh
        mes = (estadistica.fechaMes.month + 1)%12
        if mes == 1:
            anio = estadistica.fechaMes.year + 1
        else:
            anio = estadistica.fechaMes.year
        estadistica.fechaMes = datetime(year=anio,month=mes,day=1)
        estadistica.sumaMesDinero = 0.0
    

    estadistica.save()
    if estadistica.dispositivo.notificacion and estadistica.sumaDiaKw > estadistica.dispositivo.limite_maximo:
        enviarCorreoNotificacionLimiteMaximo(estadistica,estadistica.sumaDiaKw)

def guardarEstadisticaDinero(idDispositivo,listaKwTiempo):
    #1º Calculo el tiempo transcurrido entre la primera medida y la ultima
    fechaInicio = listaKwTiempo[0]["tiempo"]
    fechaFin = listaKwTiempo[-1]["tiempo"]

    tiempoTranscurridoHoras = (fechaFin - fechaInicio).total_seconds() / (60 * 60)

    #2º Calculo todos los kw que se han recodigo
    count = 0 
    for medida in listaKwTiempo:
        count += medida["kw"]
    
    #3º Calculo los kwh de estas medidas
    kwh = count / tiempoTranscurridoHoras

    #4º Pido los datos de precio de hoy
    aux = requests.get('http://51.38.189.176/pvpc_diario')

    #5º Veo la hora que es ahora (tomo la de la fecha fin)
    hora = fechaFin.hour

    #6º Busco el precio a esa hora
    preciokwh = aux.json()["precios_pvpc"][hora][poner0(hora)] / 1000

    #7º Uso el precio para calcular lo gastado
    gastado = kwh * preciokwh

    #8º Actualizo los valores
    estadistica = Estadistica.objects.get(dispositivo__id=idDispositivo)

    estadistica.sumaDiaDinero = 0 if estadistica.sumaDiaDinero is None else estadistica.sumaDiaDinero
    estadistica.sumaMesDinero = 0 if estadistica.sumaMesDinero is None else estadistica.sumaMesDinero
    estadistica.sumaTotalDinero = 0 if estadistica.sumaTotalDinero is None else estadistica.sumaTotalDinero

    estadistica.sumaTotalDinero = estadistica.sumaTotalDinero + gastado
    estadistica.sumaMesDinero = estadistica.sumaMesDinero + gastado
    estadistica.sumaDiaDinero = estadistica.sumaDiaDinero + gastado
    estadistica.save()


    










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
            usuario.notificacion_invitados = serializer.validated_data.get("notificacion_invitados")
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

        idCompartido = -1
        compartido = Compartido.objects.filter(compartido__id=usuarioToken.id)
        compartido = compartido.filter(hogarCompartido__id=hogar.id)
        if compartido.count() == 0 and hogar.owner.id != usuarioToken.id:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        if compartido.count() != 0:
            idCompartido = compartido[0].id

        dispositivos = Dispositivo.objects.filter(hogar__id=id)

        auxDispositivos = []
        for d in dispositivos:
            if d.verificado:
                auxDispositivos.append(d)

        hogarDto = HogarObtenerByIdDTO(hogar,auxDispositivos,idCompartido)

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
                tiempo_refrescado = TIEMPO_REFRESCO_ESTANDAR,
                hogar = Hogar.objects.get(id=serializer.validated_data.pop("hogar").get("id")),
                verificado = False
            )
            try:
                dispositivo.save()
                ahora = datetime.now() 
                estadistica = Estadistica(
                    dispositivo = dispositivo,
                    #fechaDia = datetime(year=ahora.year,month=ahora.month,day=ahora.day,hour=0,minute=0,second=0,microsecond=000000),
                    sumaDiaKw = 0,
                    #fechaMes = datetime(year=ahora.year,month=ahora.month,day=1,hour=0,minute=0,second=0,microsecond=000000),
                    sumaMesKw = 0,
                    sumaTotalKw = 0,
                    numDiasTotal = 1,
                    numMesTotal = 1,
                    minDiaKw = sys.float_info.max,
                    maxDiaKw = 0,
                    minMesKw = sys.float_info.max,
                    maxMesKw = 0,
                    fechaMinDiaKw = ahora,
                    fechaMaxDiaKw = ahora,
                    fechaMinMesKw = ahora,
                    fechaMaxMesKw = ahora,
                    diaMasConsumidoSemana = ahora,
                    diaMasConsumidoMes = ahora,
                    diaMasConsumidoAño = ahora,
                    diaMasConsumidoHistoricamente = ahora,
                    mesMasConsumidoAño = ahora,
                    mesMasConsumidoHistoricamente = ahora,
                    añoMasConsumidoHistoricamente = ahora,
                    fechaDia = ahora,
                    fechaMes = ahora,
                    fechaSemana = ahora,
                    fechaAño = ahora,
                    sumaSemanaKw = 0,
                    sumaAñoKw = 0,

                    consumoDiaMasConsumidoSemana = 0,
                    
                    consumoDiaMasConsumidoMes = 0,
                    consumoDiaMasConsumidoAño = 0,
                    consumoDiaMasConsumidoHistoricamente = 0,

                    consumoMesMasConsumidoAño = 0,
                    consumoMesMasConsumidoHistoricamente = 0,

                    consumoAñoMasConsumidoHistoricamente = 0,
                    tramosHistoricoHoras = {'00:00': 0, '01:00': 0, '02:00': 0, '03:00': 0, '04:00': 0, '05:00': 0,
                                            '06:00': 0, '07:00': 0, '08:00': 0, '09:00': 0, '10:00': 0, '11:00': 0,
                                            '12:00': 0, '13:00': 0, '14:00': 0, '15:00': 0, '16:00': 0, '17:00': 0,
                                            '18:00': 0, '19:00': 0, '20:00': 0, '21:00': 0, '22:00': 0, '23:00': 0},
                    historicoDiario = {'list':[]}
                )
                                
                estadistica.save()
                objeto = {
                    'id':dispositivo.id,
                    'id_hogar': dispositivo.hogar.id,
                    'id_owner':dispositivo.hogar.owner.id
                }
                token = jwt.encode(objeto,key=KEY_SECRECT,algorithm=ALGORITMO_JWT[0])
                return Response({"token" : token},status=status.HTTP_201_CREATED)
            except:
                return Response({"mensaje":"Error: El dispositivo no ha podido ser creado."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mensaje":"Error: El formato del dispositivo es incorrecto."},status=status.HTTP_400_BAD_REQUEST)

#/verificacionDispositivo
class DispositivosVerificacionView(APIView):
    def post(self,request,format=None):
        dispositivo = autorizar_dispositivo(request)
        if dispositivo == None:
            return Response({"mensage":"Dispositivo no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        if dispositivo.verificado == True:
            return Response({"mensage":"Error: El dispositivo ya fue verificado"},status=status.HTTP_400_BAD_REQUEST)

        dispositivo.verificado = True
        try:
            dispositivo.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({"mensaje":"Error: El dispositivo no se ha podido verificar"},status=status.HTTP_400_BAD_REQUEST)



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
        
        if dispositivo.verificado == False:
            return Response({"mensage":"El dispositivo todavía no esta verificado"},status=status.HTTP_400_BAD_REQUEST)

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
        
        if dipositivo.verificado == False:
            return Response({"mensage":"El dispositivo todavía no esta verificado"},status=status.HTTP_400_BAD_REQUEST)
        
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
        
        if dispositivo.verificado == False:
            return Response({"mensage":"El dispositivo todavía no esta verificado"},status=status.HTTP_400_BAD_REQUEST)

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
            medidas = Medida.objects.filter(dispositivo__id=id)
        except:
            return Response({"mensaje":"Error: No se ha encontrado las medidas de ese dispositivo con ese ID"},status=status.HTTP_404_NOT_FOUND)

        if request.query_params.get("minDate") is not None:
            medidas = medidas.filter(fecha__gte=request.query_params.get("minDate"))
            
        if request.query_params.get("maxDate") is not None:
            medidas = medidas.filter(fecha__lte=request.query_params.get("maxDate"))

        if request.query_params.get("minData") is not None:
            medidas = medidas.filter(kw__gte=request.query_params.get("minData"))
            
        if request.query_params.get("maxData") is not None:
            medidas = medidas.filter(kw__lte=request.query_params.get("maxData"))
        
        if (request.query_params.get('orderBy') is not None):
            medidas = medidas.order_by(request.query_params.get('orderBy'))
        
        if (request.query_params.get('limit') is not None and request.query_params.get('offset') is not None):
            medidas = medidas[int(request.query_params.get('offset')):int(request.query_params.get('offset'))+int(request.query_params.get('limit'))]


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

        if request.query_params.get("minDate") is not None:
            medidas = medidas.filter(fecha__gte=request.query_params.get("minDate"))
            
        if request.query_params.get("maxDate") is not None:
            medidas = medidas.filter(fecha__lte=request.query_params.get("maxDate"))

        if request.query_params.get("minData") is not None:
            medidas = medidas.filter(kw__gte=request.query_params.get("minData"))
            
        if request.query_params.get("maxData") is not None:
            medidas = medidas.filter(kw__lte=request.query_params.get("maxData"))
        
        if (request.query_params.get('orderBy') is not None):
            medidas = medidas.order_by(request.query_params.get('orderBy'))

        if (request.query_params.get('limit') is not None and request.query_params.get('offset') is not None):
            medidas = medidas[int(request.query_params.get('offset')):int(request.query_params.get('offset'))+int(request.query_params.get('limit'))]

        medidasDTO = MedidaObtenerDTO.toMedidaObtenerDTO(medidas)
        serializer = MedidaObtenerSerializer(medidasDTO,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK,headers={"X-TOTAL-COUNT":medidas.count()})

    def post(self,request,format=None):
        dispositivo = autorizar_dispositivo(request)
        if dispositivo == None:
            return Response({"mensage":"Dispositivo no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        if dispositivo.verificado == False:
            return Response({"mensage":"El dispositivo todavía no esta verificado"},status=status.HTTP_400_BAD_REQUEST)

        listaKwTiempo = []
        for medida in request.data:
            serializer = MedidaCrearSerializer(data=medida)
            if serializer.is_valid():
                voltaje = serializer.validated_data.get("voltaje") if serializer.validated_data.get("voltaje") != None else VOLTAJE_ESTANDAR
                desfase = serializer.validated_data.get("desfase") if serializer.validated_data.get("desfase") != None else DESFASE_ESTANDAR
                kw = calcularPotencia(intensidad=serializer.validated_data.get("intensidad"),voltaje=voltaje,desfase=desfase)
                listaKwTiempo.append({"kw":kw,"tiempo":serializer.validated_data.get("fecha")})
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
        #guardarEstadisticaDinero(dispositivo.id,listaKwTiempo)
        return Response({"tiempoRecogidaMedida":dispositivo.tiempo_medida,"tiempoActualizacionMedida":dispositivo.tiempo_refrescado},status=status.HTTP_201_CREATED)

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
            ya_compartido = Compartido.objects.filter(compartido=invitado_aux, hogarCompartido=hogar)
            if ya_invitado.count() == 0 and ya_compartido.count() == 0:
                invitacion = Invitacion(
                    invitado = invitado_aux,
                    hogarInvitado = hogar,
                    invitante = usuarioToken
                )
                try:
                    invitacion.save()
                    if usuarioToken.notificacion_invitados:
                        enviarCorreoInvitacion(usuarioToken,hogar,invitado_aux)
                    return Response({"id":invitacion.id},status=status.HTTP_201_CREATED)
                except:
                    return Response({"mensaje":"Error: La invitación no ha podido ser creada"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"mensaje":"Error: Hay ya una invitación pendiente."},status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"mensaje":"Error: El formato de la invitación es incorrecto."},status=status.HTTP_400_BAD_REQUEST)


#invitacionsRecibidas/
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
            hogarCompartido = invitacion.hogarInvitado
            invitante = invitacion.invitante
            invitacion.delete()
            enviarCorreoRechazadoInvitacion(usuarioToken,hogarCompartido,invitante)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"mensaje":"Error: No se ha podido eliminar una invitacion con ese ID"},status=status.HTTP_400_BAD_REQUEST)

#/compartidos
class CompartidoView(APIView):
    def post(self,request,format=None):
        usuarioToken = autorizar_usuario(request,False)
        if usuarioToken == None:
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)

        serializer = CompartidoCrearSerializer(data=request.data)
        if serializer.is_valid():
            id_hogar_compartido = serializer.validated_data.pop("hogarCompartido").get("id")
            invitacion = Invitacion.objects.filter(hogarInvitado__id=id_hogar_compartido)
            invitacion = invitacion.filter(invitado__id=usuarioToken.id)
            invitante = None
            if invitacion.count() == 0:
                return Response({"mensage":"No tienes invtación para compartir"},status=status.HTTP_400_BAD_REQUEST)
            else:
                invitante = invitacion[0].invitante
                invitacion.delete()
            
            hogarCompartido = Hogar.objects.get(id = id_hogar_compartido)
            compartido = Compartido(
                compartido = usuarioToken,
                hogarCompartido = hogarCompartido 
            )
            try:
                compartido.save()
                enviarCorreoAceptadoInvitacion(usuarioToken,hogarCompartido,invitante)
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
    
        if(compartido.hogarCompartido.owner.id != usuarioToken.id and compartido.compartido.id != usuarioToken.id):
            return Response({"mensage":"Usuario no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            hogarCompartido = compartido.hogarCompartido
            compartidoUsuario = compartido.compartido
            invitante = compartido.hogarCompartido.owner
            compartido.delete()
            if compartido.hogarCompartido.owner.id == usuarioToken.id:
                enviarCorreoTeHanDejadoCompartir(usuarioToken,hogarCompartido,compartido=compartidoUsuario)
            else:
                enviarCorreoSeHaSalido(usuarioToken,hogarCompartido,invitante)
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


def poner0(val):
    return ""+str(val) if val >= 10 else "0"+str(val)


import requests
class PreciosView(APIView):
    def get(self,request,id,format=None):
        resp = None
        if id == 3:
            resp = {
                "00":0,
                "01":0,
                "02":0,
                "03":0,
                "04":0,
                "05":0,
                "06":0,
                "07":0,
                "08":0,
                "09":0,
                "10":0,
                "11":0,
                "12":0,
                "13":0,
                "14":0,
                "15":0,
                "16":0,
                "17":0,
                "18":0,
                "19":0,
                "20":0,
                "21":0,
                "22":0,
                "23":0,
            }
            today = date.today()
            for i in range(7):
                aux = requests.get('http://51.38.189.176/pvpc_dia/' + today.strftime('%y-%m-%d'))
                json = aux.json()
                for j in range(24):
                    resp[poner0(j)] = resp[poner0(j)] + json["precios_pvpc"][j][poner0(j)]
                
                today = today - timedelta(days=1)
               
            for j in range(24):
                resp[poner0(j)] = round(resp[poner0(j)] / 7,2)
            
            return Response(resp,status=status.HTTP_200_OK)
        
        elif id == 4:
            resp = {
                "00":0,
                "01":0,
                "02":0,
                "03":0,
                "04":0,
                "05":0,
                "06":0,
                "07":0,
                "08":0,
                "09":0,
                "10":0,
                "11":0,
                "12":0,
                "13":0,
                "14":0,
                "15":0,
                "16":0,
                "17":0,
                "18":0,
                "19":0,
                "20":0,
                "21":0,
                "22":0,
                "23":0,
            }
            today = date.today()
            for i in range(30):
                aux = requests.get('http://51.38.189.176/pvpc_dia/' + today.strftime('%y-%m-%d'))
                json = aux.json()
                for j in range(24):
                    resp[poner0(j)] = resp[poner0(j)] + json["precios_pvpc"][j][poner0(j)]
                
                today = today - timedelta(days=1)
               
            for j in range(24):
                resp[poner0(j)] = round(resp[poner0(j)] / 30,2)
            
            return Response(resp,status=status.HTTP_200_OK)
        elif id == 5 :
            resp = {
                "00":0,
                "01":0,
                "02":0,
                "03":0,
                "04":0,
                "05":0,
                "06":0,
                "07":0,
                "08":0,
                "09":0,
                "10":0,
                "11":0,
                "12":0,
                "13":0,
                "14":0,
                "15":0,
                "16":0,
                "17":0,
                "18":0,
                "19":0,
                "20":0,
                "21":0,
                "22":0,
                "23":0,
            }
            count = {
                "00":0,
                "01":0,
                "02":0,
                "03":0,
                "04":0,
                "05":0,
                "06":0,
                "07":0,
                "08":0,
                "09":0,
                "10":0,
                "11":0,
                "12":0,
                "13":0,
                "14":0,
                "15":0,
                "16":0,
                "17":0,
                "18":0,
                "19":0,
                "20":0,
                "21":0,
                "22":0,
                "23":0,
            }
            today = date.today()
            for i in range(91):
                aux = requests.get('http://51.38.189.176/pvpc_dia/' + today.strftime('%y-%m-%d'))
                json = aux.json()
                for j in range(24):
                    try:
                        val = json["precios_pvpc"][j][poner0(j)]
                        count[poner0(j)] = count[poner0(j)] + 1
                    except:
                        val = 0
                    resp[poner0(j)] = resp[poner0(j)] + val
                
                today = today - timedelta(days=1)
               
            for j in range(24):
                if count[poner0(j)] != 0:
                    resp[poner0(j)] = round(resp[poner0(j)] / count[poner0(j)],2)
                else:
                    resp[poner0(j)] = 0
            
            return Response(resp,status=status.HTTP_200_OK)
           
    
        return Response(status=status.HTTP_200_OK)
        