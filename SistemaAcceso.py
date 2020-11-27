import os
from gpiozero import AngularServo


class SistemaAcceso():

    def __init__(self,codigoDesactivacion):
        self.activo = True
        self.DIR_BASE = os.path.dirname(os.path.abspath(__file__))
        self.rutaLogs = os.path.join(self.DIR_BASE, 'logs')
        self.nombreArchivo = 'bitacora_accesso.txt'
        self.rutaArchivo = os.path.join(self.rutaLogs, self.nombreArchivo)
        self.crearArchivo()
        self.estadoServo = True
        self.anguloDefault = 90
        self.gpioServoPin = 17
        self.codigoDesactivacion = codigoDesactivacion
        #self.servo = AngularServo(self.gpioServoPin)

    def cambiarEstado(self):
        self.activo = not self.activo

    def cambiarEstadoServo(self):
        self.estadoServo = not self.estadoServo

    def estaActivo(self):
        return self.activo
    
    def servoActivo(self):
        return self.estadoServo

    def crearArchivo(self):
        try:
            file = open(self.rutaArchivo, "r")
            file.close()
        except IOError:
            file = open(self.rutaArchivo, "w")
            file.close()

    def levantarPluma(self, linea):
        self.servo.angle = self.anguloDefault
        self.registrarEnBitacora(linea)

    def bajarPluma(self, linea):
        self.servo.angle = 0
        self.registrarEnBitacora(linea)

    def setAngulo(self, angulo, linea):
        self.anguloDefault = angulo
        self.registrarEnBitacora(linea)

    def registrarEnBitacora(self, mensaje):
        with open(self.rutaArchivo, 'a') as log:
            log.write(mensaje)
