

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
        self.potencia_contratada = hogar.potencia_contratada
    
    @staticmethod
    def toDispositivoDTO(dispositivos):
        lista = []
        for d in dispositivos:
            lista.append(DispositivoDTO(d))
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