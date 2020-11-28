import os
import RPi.GPIO as GPIO
import Adafruit_DHT


class SistemaAire():
    
    def __init__(self,codigoDesactivacion):
        self.activo = True
        self.DIR_BASE = os.path.dirname(os.path.abspath(__file__))
        self.rutaLogs = os.path.join(self.DIR_BASE, 'logs')
        self.nombreArchivo = 'bitacora_aire.txt'
        self.rutaArchivo = os.path.join(self.rutaLogs, self.nombreArchivo)
        self.crearArchivo()
        self.codigoDesactivacion = codigoDesactivacion
        self.pinSensor = 2
        self.gradosSensor = 40
        self.estadoSensor = True
        self.setup()
        
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
            
    def Dht11(self):
        sensor = Adafruit_DHT.DHT11
        return Adafruit_DHT.read_retry(sensor,self.pinSensor)

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        
    def cambiarEstadoSensor(self):
        self.estadoSensor = not self.estadoSensor

    def sensorActivo(self):
        return self.estadoSensor

    def establecerGradosSensor(self,grados,linea):
        self.gradosSensor = grados
        self.registrarEnBitacora(linea)