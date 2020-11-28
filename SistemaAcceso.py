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
        self.estadoServo2 = True
        self.anguloDefault = 90
        self.angulo2Default = 90
        self.gpioServoPin = 17
        self.gpioServo2Pin = 20
        self.codigoDesactivacion = codigoDesactivacion
        self.servo = AngularServo(self.gpioServoPin)
        self.servo2 = AngularServo(self.gpioServo2Pin)

    def cambiarEstado(self):
        self.activo = not self.activo

    def cambiarEstadoServo(self):
        self.estadoServo = not self.estadoServo
        
    def cambiarEstadoServo2(self):
        self.estadoServo2 = not self.estadoServo2

    def estaActivo(self):
        return self.activo
    
    def servoActivo(self):
        return self.estadoServo
    
    def servo2Activo(self):
        return self.estadoServo2

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
        
    def levantarPluma2(self, linea):
        self.servo2.angle = self.angulo2Default
        self.registrarEnBitacora(linea)

    def bajarPluma2(self, linea):
        self.servo2.angle = 0
        self.registrarEnBitacora(linea)

    def setAngulo2(self, angulo, linea):
        self.angulo2Default = angulo
        self.registrarEnBitacora(linea)

    def registrarEnBitacora(self, mensaje):
        with open(self.rutaArchivo, 'a') as log:
            log.write(mensaje)
