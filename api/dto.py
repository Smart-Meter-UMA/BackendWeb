from datetime import datetime

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
    def __init__(self, hogar):
        self.id = hogar.id
        self.nombre = hogar.nombre
    
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

class EstadisticaDTO():
    def __init__(self,estadistica):
        #TODO: Hacer las estadistica
        self.minKWHDiario = estadistica.minDiaKwh
        self.consumidoHoy = estadistica.sumaDiaKwh
        self.consumidoMes = estadistica.sumaMesKwh
        self.diaMinKWHGastado = estadistica.fechaMinDiaKwh
        self.maxKWHDiario = estadistica.maxDiaKwh
        self.diaMaxKWHGastado = estadistica.fechaMaxDiaKwh
        self.minKWHMensual = estadistica.minMesKwh
        self.mesMinKWHGastado = estadistica.fechaMinMesKwh
        self.maxKWHMensual = estadistica.maxMesKwh
        self.mesMaxKWHGastado = estadistica.fechaMaxMesKwh

        ahora = datetime.now()
        self.mediaKWHDiaria = estadistica.sumaTotalKwh / ((estadistica.numDiasTotal * 24) + ((ahora - datetime.fromtimestamp(estadistica.fechaDia.timestamp())).total_seconds()/3600))
        self.mediaKWHMensual = estadistica.sumaTotalKwh / ((estadistica.numMesTotal * 730.001) + ((ahora - datetime.fromtimestamp(estadistica.fechaMes.timestamp())).total_seconds()/3600))

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
    def __init__(self, hogar, dispositivos, editable):
        self.id = hogar.id
        self.potencia_contratada = hogar.potencia_contratada
        self.nombre = hogar.nombre
        self.dispositivos = DispositivoDTO.toDispositivoDTO(dispositivos)
        self.editable = editable

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