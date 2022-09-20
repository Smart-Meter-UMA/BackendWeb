from datetime import datetime
import sys

from api.models import Estadistica

class UsuarioObtenerDTO():
    def __init__(self, usuario):
        self.id = usuario.id
        self.email = usuario.email
        self.nombre = usuario.nombre
        self.apellidos = usuario.apellidos
        self.notificacion_invitados = usuario.notificacion_invitados
    
    @staticmethod
    def toUsuarioObtenerDTO(usuarios):
        lista = []
        for u in usuarios:
            lista.append(UsuarioObtenerDTO(u))
        return lista

class HogarObtenerDTO():
    def __init__(self, hogar, compartido):
        self.id = hogar.id
        self.potencia_contratada = hogar.potencia_contratada
        self.nombre = hogar.nombre
        self.compartido = compartido
    
    @staticmethod
    def toHogarObtenerDTO(hogars,compartidos):
        lista = []
        for h in hogars:
            lista.append(HogarObtenerDTO(h,False))
        for c in compartidos:
            lista.append(HogarObtenerDTO(c.hogarCompartido,True))
        return lista


class DispositivoDTO():
    def __init__(self, dispositivo):
        self.id = dispositivo.id
        self.nombre = dispositivo.nombre
        self.general = dispositivo.general
        self.notificacion = dispositivo.notificacion
        self.limite_minimo = dispositivo.limite_minimo
        self.limite_maximo = dispositivo.limite_maximo
        self.tiempo_medida = dispositivo.tiempo_medida
        self.tiempo_refrescado = dispositivo.tiempo_refrescado
    
    @staticmethod
    def toDispositivoDTO(dispositivos):
        lista = []
        for d in dispositivos:
            lista.append(DispositivoDTO(d))
        return lista

class DispositivoHogarObtenerDTO():
    def __init__(self, hogar):
        self.id = hogar.id
        self.nombre = hogar.nombre
        self.estadistica = EstadisticaDTO(Estadistica.objects.get(dispositivo__id=hogar.id))
    
    @staticmethod
    def toDispositivoHogarObtenerDTO(dispositivos):
        lista = []
        for d in dispositivos:
            lista.append(DispositivoHogarObtenerDTO(d))
        return lista

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

class EstadisticaDTO():
    def __init__(self,estadistica):
        ahora = datetime.now()
        sumaDia = estadistica.sumaDiaKw
        sumaMes = estadistica.sumaMesKw

        self.fechaHoy = estadistica.fechaDia.strftime("%Y-%m-%dT%H:%M") 
        self.fechaAhora = ahora.strftime("%Y-%m-%dT%H:%M")
        self.consumidoHoy = round(sumaDia,3)
        self.sumaDiaDinero = round(0 if estadistica.sumaDiaDinero is None else estadistica.sumaDiaDinero,2)
        
        self.consumidoMes = round(sumaMes,3)
        self.sumaMesDinero = round(0 if estadistica.sumaMesDinero is None else estadistica.sumaMesDinero,2)

        sumaTotal = estadistica.sumaTotalKw
        self.mediaKWHDiaria = round(sumaTotal / estadistica.numDiasTotal,3)
        self.mediaKWHMensual = round(sumaTotal / estadistica.numMesTotal,3)

        auxDineroTotal = 0 if estadistica.sumaTotalDinero is None else estadistica.sumaTotalDinero
        
        self.sumaMediaDiariaDinero = round(auxDineroTotal / estadistica.numDiasTotal,2)
        self.sumaMediaMensualDinero = round(auxDineroTotal / estadistica.numMesTotal,2)

        self.tramosHoras = estadistica.tramosHoras
        self.tramosHorasMedia = {}
        for attribute, value in estadistica.tramosHoras.items():
            self.tramosHorasMedia[attribute] = round(value / estadistica.numDiasTotal,3)
        
        self.tramoSemanal = estadistica.tramoSemanal
        self.tramosSemanalMedia = {}
        for attribute, value in estadistica.tramoSemanal.items():
            self.tramosSemanalMedia[attribute] = round(value / (estadistica.numDiasTotal/7),3)
        
        self.tramosMensual = estadistica.tramosMensual
        self.tramosMensualMedia = {}
        for attribute, value in estadistica.tramosMensual.items():
            self.tramosMensualMedia[attribute] = round(value / (estadistica.numDiasTotal/30),3)
        
        self.historicoDiario = estadistica.historicoDiario
        self.historicoMensual = estadistica.historicoMensual

        self.historicoMasConsumido = estadistica.historicoMasConsumido

    
class DispositivoObtenerByIdDTO():
    def __init__(self, hogar, estadistica):
        self.id = hogar.id
        self.nombre = hogar.nombre
        self.estadisticas = EstadisticaDTO(estadistica)

class InvitacionDTO():
    def __init__(self, invitacion):
        self.id = invitacion.id
        self.invitante = UsuarioObtenerDTO(invitacion.invitante)
        self.hogarInvitado = HogarObtenerDTO(invitacion.hogarInvitado)
        self.invitado = UsuarioObtenerDTO(invitacion.invitado)
    
    @staticmethod
    def toInvitacionDTO(invitacions):
        lista = []
        for i in invitacions:
            lista.append(InvitacionDTO(i))
        return lista

class CompartidoObtencionDTO():
    def __init__(self, compartido):
        self.id = compartido.id
        self.compartido = UsuarioObtenerDTO(compartido.compartido)
    
    @staticmethod
    def toCompartidoObtencionDTO(compartidos):
        lista = []
        for c in compartidos:
            lista.append(CompartidoObtencionDTO(c))
        return lista


class MedidaDTO():
    def __init__(self, medida):
        self.id = medida.id
        self.fecha = medida.fecha
        self.intensidad = medida.intensidad
        self.voltaje = medida.voltaje
        self.kw = medida.kw
       
    @staticmethod
    def toMedidaDTO(medidas):
        lista = []
        for m in medidas:
            lista.append(MedidaDTO(m))
        return lista

class MedidaObtenerDTO():
    def __init__(self, medida):
        self.id = medida.id
        self.fecha = medida.fecha
        self.kw = medida.kw
       
    @staticmethod
    def toMedidaObtenerDTO(medidas):
        lista = []
        for m in medidas:
            lista.append(MedidaObtenerDTO(m))
        return lista

class HogarObtenerByIdDTO():
    def __init__(self, hogar, dispositivos, idCompartido):
        self.id = hogar.id
        self.potencia_contratada = hogar.potencia_contratada
        self.nombre = hogar.nombre
        self.dispositivos = DispositivoDTO.toDispositivoDTO(dispositivos)
        self.idCompartido = idCompartido

class InvtiacionsRecibidasDTO():
    def __init__(self, invitacions):
        self.id = invitacions.id
        self.ofertante = invitacions.invitante
        self.hogarInvitado = invitacions.hogarInvitado

    @staticmethod
    def toInvtiacionsRecibidasDTO(invitacions):
        lista = []
        for i in invitacions:
            lista.append(InvtiacionsRecibidasDTO(i))
        return lista