class Cache():

    def __init__(self,usuario,rol):
        self.usuario = usuario
        self.roles = ['Administrador', 'Operador']
        self.rol = rol

    def usuarioEsAdministrador(self):
        return True if self.rol == "Administrador" else False