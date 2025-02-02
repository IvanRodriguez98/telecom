import os
from gpiozero import DistanceSensor
import RPi.GPIO as GPIO

class SistemaAlarma():
    
    def __init__(self,codigoDesactivacion):
        self.activo = True
        self.DIR_BASE = os.path.dirname(os.path.abspath(__file__))
        self.rutaLogs = os.path.join(self.DIR_BASE, 'logs')
        self.nombreArchivo = 'bitacora_alarma.txt'
        self.rutaArchivo = os.path.join(self.rutaLogs, self.nombreArchivo)
        self.crearArchivo()
        self.codigoDesactivacion = codigoDesactivacion
        self.pinAlarma = 25
        self.distanciaSensor = 100
        self.pinled = 3
        self.pinEcho = 7
        self.pinTrig = 8
        self.estadoSensor = True
        
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

    def cambiarEstadoSensor(self):
        self.estadoSensor = not self.estadoSensor

    def sensorActivo(self):
        return self.estadoSensor

    def establecerDistanciaSensor(self,distancia,linea):
        self.distanciaSensor = distancia
        self.registrarEnBitacora(linea)