

from api.models import Usuario


class UsuarioDTO():
    def __init__(self, usuario):
        self.id = usuario.id
        self.email = usuario.email
        self.username = usuario.username
        self.nombre = usuario.nombre
        self.apellidos = usuario.apellidos
    
    @staticmethod
    def toUsuariosDTO(usuarios):
        lista = []
        for u in usuarios:
            lista.append(UsuarioDTO(u))
        return lista

class HogarDTO():
    def __init__(self, hogar):
        self.id = hogar.id
        self.potencia_contratada = hogar.potencia_contratada
        self.nombre = hogar.nombre
    
    @staticmethod
    def toHogarsDTO(hogars):
        lista = []
        for h in hogars:
            lista.append(HogarDTO(h))
        return lista


class DispositivoDTO():
    def __init__(self, hogar):
        self.id = hogar.id
        self.nombre = hogar.nombre
        self.limite_minimo = hogar.limite_minimo
        self.limite_maximo = hogar.limite_maximo
    
    @staticmethod
    def toDispositivoDTO(dispositivos):
        lista = []
        for d in dispositivos:
            lista.append(DispositivoDTO(d))
        return lista

class InvitacionDTO():
    def __init__(self, invitacion):
        self.id = invitacion.id
        self.invitante = UsuarioDTO(invitacion.invitante)
        self.hogarInvitado = HogarDTO(invitacion.hogarInvitado)
        self.invitado = UsuarioDTO(invitacion.invitado)
    
    @staticmethod
    def toInvitacionDTO(invitacions):
        lista = []
        for i in invitacions:
            lista.append(InvitacionDTO(i))
        return lista

class CompartidoDTO():
    def __init__(self, compartido):
        self.id = compartido.id
        self.compartido = UsuarioDTO(compartido.compartido)
        self.hogarCompartido = HogarDTO(compartido.hogarCompartido)
    
    @staticmethod
    def toCompartidoDTO(compartidos):
        lista = []
        for c in compartidos:
            lista.append(CompartidoDTO(c))
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