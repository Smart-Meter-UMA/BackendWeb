

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