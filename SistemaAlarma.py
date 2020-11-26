import os
import RPi.GPIO as GPIO

class SistemaAlarma():
    
    def __init__(self,codigoDesactivacion):
        self.activo = True
        self.DIR_BASE = os.path.dirname(os.path.abspath(__file__))
        self.rutaLogs = os.path.join(self.DIR_BASE, 'logs')
        self.nombreArchivo = 'bitacora_alarma.txt'
        self.rutaArchivo = os.path.join(self.rutaLogs, self.nombreArchivo)
        self.crearArchivo()
        
    def cambiarEstado(self):
        self.activo = not self.activo
        
    def estaActivo(self):
        return self.activo
        
    def crearArchivo(self):
        try:
            file = open(self.rutaArchivo, "r")
            file.close()
        except IOError:
            file = open(self.rutaArchivo, "w")
            file.close()
            
    def registrarEnBitacora(self, mensaje):
        with open(self.rutaArchivo, 'a') as log:
            log.write(mensaje)