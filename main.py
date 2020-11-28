from SistemaAcceso import SistemaAcceso
from SistemaAlarma import SistemaAlarma
from SistemaAire import SistemaAire
import tkinter as tk
from tkinter import messagebox, simpledialog,Button
from Cache import Cache
import time
import threading
from gpiozero import DistanceSensor
import RPi.GPIO as GPIO


class App():

    def __init__(self,usuario,rol,codigo1,codigo2,codigo3):
        self.window = tk.Tk()
        self.window.title("Sistemas Integrados")
        self.datosCache = Cache(usuario, rol)
        self.sistemaAcceso = SistemaAcceso(codigo1)
        self.sistemaAlarma = SistemaAlarma(codigo2)
        self.sistemaAire = SistemaAire(codigo3)
        self.window.geometry("1000x450")
        self.buildApp()
        self.buildLabels()
        self.update_clock()
        self.sensor = DistanceSensor(self.sistemaAlarma.pinEcho,self.sistemaAlarma.pinTrig)
        self.setup()
        self.threadAlarma = threading.Thread(target=self.lecturaSensor)
        self.threadAlarma.start()
        self.threadTemperatura = threading.Thread(target=self.lecturaSensorTemperatura)
        self.threadTemperatura.start()
        self.window.mainloop()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sistemaAlarma.pinAlarma, GPIO.OUT)
        GPIO.setup(self.sistemaAlarma.pinled, GPIO.OUT)
        
    def update_clock(self):
        now = time.strftime("%d/%m/%y %H:%M:%S")
        self.lblReloj.configure(text=now)
        self.window.after(1000, self.update_clock)

    def buildLabels(self):
        estadoSistema = "Activo" if self.sistemaAcceso.estaActivo() else "Inactivo"
        estadoServo = "Activa" if self.sistemaAcceso.servoActivo() else "Inactiva"
        estadoServo2 = "Activa" if self.sistemaAcceso.servo2Activo() else "Inactiva"
        estadoSistemaAire = "Activo" if self.sistemaAire.estaActivo() else "Inactivo"
        estadoSensorAire = "Activo" if self.sistemaAire.sensorActivo() else "Inactivo"
        estadoSistemaAlerta = "Activo" if self.sistemaAlarma.estaActivo() else "Inactivo"
        estadoSensorAlarma = "Activo" if self.sistemaAlarma.sensorActivo() else "Inactivo"
        frame_nombre = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_nombre.grid(row=0, column=0)
        self.lblEstadoSistemaAcceso = tk.Label(master=frame_nombre,
                                               text=f"Estado del sistema de acceso: {estadoSistema}")
        self.lblEstadoSistemaAcceso.pack()
        frame_estadoAlarma = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_estadoAlarma.grid(row=0, column=1)
        self.lblEstadoSistemaAlarma = tk.Label(master=frame_estadoAlarma,
                                               text=f"\tEstado del sistema de alarma: {estadoSistemaAlerta}")
        self.lblEstadoSistemaAlarma.pack()
        frame_estadoAire = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_estadoAire.grid(row=0, column=3)
        self.lblEstadoSistemaAire = tk.Label(master=frame_estadoAire,
                                               text=f"\tEstado del sistema de control de aire: {estadoSistemaAire}")
        self.lblEstadoSistemaAire.pack()
        frame_pluma = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_pluma.grid(row=2, column=0)
        self.lblEstadoPluma = tk.Label(master=frame_pluma, text=f"Estado de la pluma de entrada: {estadoServo}")
        self.lblEstadoPluma.pack()
        frame_pluma2 = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_pluma2.grid(row=9, column=0)
        self.lblEstadoPluma2 = tk.Label(master=frame_pluma2, text=f"Estado de la pluma de salida: {estadoServo2}")
        self.lblEstadoPluma2.pack()
        frame_x = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_x.grid(row=7, column=1)
        self.lblDistancia = tk.Label(master=frame_x, text=f"Distancia establecida: {self.sistemaAlarma.distanciaSensor} cm")
        self.lblDistancia.pack()
        frame_x = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_x.grid(row=8, column=1)
        self.lblLecturaSensor = tk.Label(master=frame_x, text="Ultima lectura: ")
        self.lblLecturaSensor.pack()
        frame_x = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_x.grid(row=9, column=1)
        self.lblEstadoSensor = tk.Label(master=frame_x, text=f"Estado de sensor: {estadoSensorAlarma}")
        self.lblEstadoSensor.pack()
        
        frame_x = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_x.grid(row=7, column=3)
        self.lblTmpEstablecida = tk.Label(master=frame_x, text=f"Temperatura establecida: {self.sistemaAire.gradosSensor} °C")
        self.lblTmpEstablecida.pack()
        frame_x = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_x.grid(row=8, column=3)
        self.lblLecturaSensorT = tk.Label(master=frame_x, text="Ultima lectura: ")
        self.lblLecturaSensorT.pack()
        
        frame_sensorT = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_sensorT.grid(row=9, column=3)
        self.lblEstadoSensorT = tk.Label(master=frame_sensorT, text=f"Estado de sensor de temperatura: {estadoSensorAire}")
        self.lblEstadoSensorT.pack()
        frame_usuario = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_usuario.grid(row=0, column=1)
        self.lblUsuario = tk.Label(master=self.window, text=f"Usuario actual: {self.datosCache.usuario}")
        self.lblUsuario.place(x=0.0, y=400)
        self.lblRol = tk.Label(master=self.window, text=f"Rol de usuario: {self.datosCache.rol}")
        self.lblRol.place(x=0.0, y=420)
        frame_reloj = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_reloj.grid(row=0, column=5)
        self.lblReloj = tk.Label(master=self.window)
        self.lblReloj.place(x=150, y=400)

    def buildApp(self):
        frame_1 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_1.grid(row=1, column=0)
        self.btnDesactivar = tk.Button(master=frame_1, text="Desactivar", command=self.cambiarEstadoSistemaAcceso)
        self.btnDesactivar.pack()
        
        frame_1_5 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_1_5.grid(row=1, column=1)
        self.btnDesactivarAlarma = tk.Button(master=frame_1_5, text="Desactivar",
                                             command=self.cambiarEstadoSistemaAlarma)
        self.btnDesactivarAlarma.pack()
        
        frame_2_5 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2_5.grid(row=1, column=3)
        self.btnDesactivarAire = tk.Button(master=frame_2_5, text="Desactivar",
                                             command=self.cambiarEstadoSistemaAire)
        self.btnDesactivarAire.pack()
        
        frame_1_6 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_1_6.grid(row=10, column=1)
        self.btnEstadoSensor = tk.Button(master=frame_1_6, text="Desactivar sensor",
                                         command=self.cambiarEstadoSensorAlarma)
        self.btnEstadoSensor.pack()
        frame_2_6 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2_6.grid(row=10, column=3)
        self.btnEstadoSensorT = tk.Button(master=frame_2_6, text="Desactivar sensor",
                                         command=self.cambiarEstadoSensorTemperatura)
        self.btnEstadoSensorT.pack()

        frame_2 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2.grid(row=4, column=0)
        self.btnCambiarAngulo = tk.Button(master=frame_2, text="Cambiar angulo de pluma de entrada",
                                          command=self.cambiarAnguloPluma)
        self.btnCambiarAngulo.pack()
        frame_2 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2.grid(row=10, column=0)
        self.btnCambiarAngulo2 = tk.Button(master=frame_2, text="Cambiar angulo de pluma de salida",
                                          command=self.cambiarAnguloPluma2)
        self.btnCambiarAngulo2.pack()
        frame_2_1 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2_1.grid(row=2, column=1)
        self.btnCambiarDistancia = tk.Button(master=frame_2_1, text="Cambiar distancia del sensor",
                                          command=self.cambiarDistanciaSensor)
        self.btnCambiarDistancia.pack()
        frame_2_1 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2_1.grid(row=2, column=3)
        self.btnCambiarTmp = tk.Button(master=frame_2_1, text="Cambiar temperatura maxima para sensor",
                                          command=self.cambiarTemperatura)
        self.btnCambiarTmp.pack()
        frame_3 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_3.grid(row=5, column=0)
        self.btnLevantarPluma = tk.Button(master=frame_3, text="Levantar pluma",
                                          command=self.levantarPluma)
        self.btnLevantarPluma.pack()
        frame_3_1 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_3_1.grid(row=13, column=0)
        self.btnLevantarPluma2 = tk.Button(master=frame_3_1, text="Levantar pluma",
                                          command=self.levantarPluma2)
        self.btnLevantarPluma2.pack()
        
        frame_4 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_4.grid(row=6, column=0)
        self.btnBajarPluma = tk.Button(master=frame_4, text="Bajar pluma",
                                          command=self.bajarPluma)
        self.btnBajarPluma.pack()
        frame_4 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_4.grid(row=14, column=0)
        self.btnBajarPluma2 = tk.Button(master=frame_4, text="Bajar pluma",
                                          command=self.bajarPluma2)
        self.btnBajarPluma2.pack()
        frame_5 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_5.grid(row=3, column=0)
        self.btnEstadoPluma = tk.Button(master=frame_5, text="Desactivar pluma de entrada", command=self.cambiarEstadoPluma)
        self.btnEstadoPluma.pack()
        frame_6 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_6.grid(row=12, column=0)
        self.btnEstadoPluma2 = tk.Button(master=frame_6, text="Desactivar pluma de salida", command=self.cambiarEstadoPluma2)
        self.btnEstadoPluma2.pack()

    def lecturaSensor(self):
        while self.sistemaAlarma.estaActivo():
            while self.sistemaAlarma.sensorActivo():
                try:
                    lectura = "{:.2f}".format((self.sensor.distance * 100))
                    self.lblLecturaSensor['text'] = f"Ultima lectura: {lectura} cm"
                    if (self.sensor.distance * 100) < self.sistemaAlarma.distanciaSensor:
                        linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Se activo la sirena!, se detecto movimiento a"\
                        f" {(self.sensor.distance * 100)} centimetro(s)\n"
                        GPIO.output(self.sistemaAlarma.pinAlarma, True)
                        GPIO.output(self.sistemaAlarma.pinled, True)
                        self.sistemaAlarma.registrarEnBitacora(linea)
                    else:
                        GPIO.output(self.sistemaAlarma.pinAlarma, False)
                        GPIO.output(self.sistemaAlarma.pinled, False)
                except:
                    print('No se detecto ningun objeto')
                    GPIO.output(self.sistemaAlarma.pinAlarma, False)
                    time.sleep(1)

    def cambiarEstadoSistemaAcceso(self):
        if self.datosCache.usuarioEsAdministrador():
            codigo = simpledialog.askinteger('Atencion',
                                             'Ingrese el codigo de desactivacion' if self.sistemaAcceso.estaActivo() else 'Ingrese el codigo de activacion')
            if codigo == self.sistemaAcceso.codigoDesactivacion:
                self.sistemaAcceso.cambiarEstado()
                estado = "Activo" if self.sistemaAcceso.estaActivo() else "Inactivo"
                linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado del sistema de acceso: {estado}," \
                        f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
                self.lblEstadoSistemaAcceso['text'] = f"Estado del sistema de acceso: {estado}"
                self.btnDesactivar['text'] = "Desactivar" if self.sistemaAcceso.estaActivo() else "Activar"
                self.sistemaAcceso.registrarEnBitacora(linea)
                if not self.sistemaAcceso.estaActivo():
                    self.sistemaAcceso.cambiarEstadoServo()
                    self.sistemaAcceso.cambiarEstadoServo2()
                    estado = "Activa" if self.sistemaAcceso.servoActivo() else "Inactiva"
                    self.lblEstadoPluma.configure(text=f"Estado de la pluma de entrada: {estado}")
                    self.btnEstadoPluma['text'] = "Desactivar pluma" if self.sistemaAcceso.servoActivo() else "Activar pluma"
                    estado = "Activa" if self.sistemaAcceso.servo2Activo() else "Inactiva"
                    self.lblEstadoPluma2.configure(text=f"Estado de la pluma de salida: {estado}")
                    self.btnEstadoPluma2['text'] = "Desactivar pluma" if self.sistemaAcceso.servo2Activo() else "Activar pluma"
            else:
                messagebox.showerror("Error", "El codigo de desactivacion es invalido")
        else:
            messagebox.showerror("Error",
                                 "Lo sentimos, pero no puede realizar esta operacion, solo un administrador puede hacerlo")

    def cambiarEstadoSistemaAlarma(self):
        if self.datosCache.usuarioEsAdministrador():
            codigo = simpledialog.askinteger('Atencion','Ingrese el codigo de desactivacion' if self.sistemaAlarma.estaActivo() else 'Ingrese el codigo de activacion')
            if codigo == self.sistemaAlarma.codigoDesactivacion:
                self.sistemaAlarma.cambiarEstado()
                estado = "Activo" if self.sistemaAlarma.estaActivo() else "Inactivo"
                linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado del sistema: {estado}," \
                        f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
                self.lblEstadoSistemaAlarma['text'] = f"\tEstado del sistema de alarma: {estado}"
                self.btnDesactivarAlarma['text'] = "Desactivar" if self.sistemaAlarma.estaActivo() else "Activar"
                self.sistemaAlarma.registrarEnBitacora(linea)
                if not self.sistemaAlarma.estaActivo():
                    self.sistemaAlarma.cambiarEstadoSensor()
                    estado = "Activo" if self.sistemaAlarma.sensorActivo() else "Inactivo"
                    self.lblEstadoSensor.configure(text=f"Estado del sensor: {estado}")
                    self.btnEstadoSensor['text'] = "Desactivar sensor" if self.sistemaAlarma.sensorActivo() else "Activar sensor"
                    if self.sistemaAlarma.sensorActivo():
                        self.threadAlarma.start()
                    else:
                        self.threadAlarma = threading.Thread(target=self.lecturaSensor)
            else:
                messagebox.showerror("Error", "El codigo de desactivacion es invalido")
        else:
            messagebox.showerror("Error",
                                 "Lo sentimos, pero no puede realizar esta operacion, solo un administrador puede hacerlo")
    
    def cambiarEstadoSistemaAire(self):
        if self.datosCache.usuarioEsAdministrador():
            codigo = simpledialog.askinteger('Atencion',
                                             'Ingrese el codigo de desactivacion' if self.sistemaAire.estaActivo() else 'Ingrese el codigo de activacion')
            if codigo == self.sistemaAire.codigoDesactivacion:
                self.sistemaAire.cambiarEstado()
                estado = "Activo" if self.sistemaAire.estaActivo() else "Inactivo"
                linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado del sistema de control de aire: {estado}," \
                        f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
                self.lblEstadoSistemaAire['text'] = f"\tEstado del sistema de control de aire: {estado}"
                self.btnDesactivarAire['text'] = "Desactivar" if self.sistemaAire.estaActivo() else "Activar"
                self.sistemaAire.registrarEnBitacora(linea)
            else:
                messagebox.showerror("Error", "El codigo de desactivacion es invalido")
        else:
            messagebox.showerror("Error",
                                 "Lo sentimos, pero no puede realizar esta operacion, solo un administrador puede hacerlo")
            
    def cambiarAnguloPluma(self):
        if self.sistemaAcceso.estaActivo():
            try:
                angulo = simpledialog.askinteger('Cambiar angulo de pluma', 'Ingrese un angulo entre 1 y 90 grados')
                while angulo < 1 or angulo > 90:
                    angulo = simpledialog.askinteger('Cambiar angulo de pluma',
                                                     'Ingrese un angulo entre 1 y 90 grado(s)')
            except:
                angulo = 90
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Cambio el angulo de la pluma, ahora con un valor de {angulo} grado(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.sistemaAcceso.setAngulo(angulo, linea)
        else:
            messagebox.showerror('Error', 'El sistema debe estar activo')
            
    def cambiarAnguloPluma2(self):
        if self.sistemaAcceso.estaActivo():
            try:
                angulo = simpledialog.askinteger('Cambiar angulo de pluma', 'Ingrese un angulo entre 1 y 90 grados')
                while angulo < 1 or angulo > 90:
                    angulo = simpledialog.askinteger('Cambiar angulo de pluma',
                                                     'Ingrese un angulo entre 1 y 90 grado(s)')
            except:
                angulo = 90
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Cambio el angulo de la pluma de salida, ahora con un valor de {angulo} grado(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.sistemaAcceso.setAngulo2(angulo, linea)
        else:
            messagebox.showerror('Error', 'El sistema debe estar activo')

    def cambiarDistanciaSensor(self):
        if self.sistemaAcceso.estaActivo():
            try:
                distancia = simpledialog.askinteger('Cambiar rango de distancia',
                                                    'Ingrese una distancia entre 1 y 100 centimetros')
                while distancia < 1 or distancia > 100:
                    distancia = simpledialog.askinteger('Cambiar rango de distancia',
                                                        'Ingrese una distancia entre 1 y 100 centimetros')
            except:
                distancia = 50
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Cambio la distancia minima entre un objeto y el sensor {distancia} centimetro(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.sistemaAlarma.establecerDistanciaSensor(distancia, linea)
            self.lblDistancia.configure(text=f"Distancia establecida: {self.sistemaAlarma.distanciaSensor} cm")
        else:
            messagebox.showerror('Error', 'El sistema de alarma debe estar activo')

    def levantarPluma(self):
        if self.sistemaAcceso.estaActivo():
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Se esta levantando la pluma de entrada en un angulo de {self.sistemaAcceso.anguloDefault} grado(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            if self.sistemaAcceso.estadoServo:
                self.sistemaAcceso.levantarPluma(linea)
            else:
                messagebox.showerror('Error', 'La pluma esta desactivada')
        else:
            messagebox.showerror('Error', 'El sistema debe estar activo')
            
    def levantarPluma2(self):
        if self.sistemaAcceso.estaActivo():
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Se esta levantando la pluma de salida en un angulo de {self.sistemaAcceso.anguloDefault} grado(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            if self.sistemaAcceso.estadoServo2:
                self.sistemaAcceso.levantarPluma2(linea)
            else:
                messagebox.showerror('Error', 'La pluma esta desactivada')
        else:
            messagebox.showerror('Error', 'El sistema debe estar activo')


    def bajarPluma(self):
        if self.sistemaAcceso.estaActivo():
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Se esta bajando la pluma de salida en un angulo de {self.sistemaAcceso.anguloDefault} grado(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            if self.sistemaAcceso.servoActivo():
                self.sistemaAcceso.bajarPluma(linea)
            else:
                messagebox.showerror('Error', 'La pluma esta desactivada')
        else:
            messagebox.showerror('Error', 'El sistema de acceso debe estar activo')

    def bajarPluma2(self):
        if self.sistemaAcceso.estaActivo():
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Se esta bajando la pluma de salida en un angulo de {self.sistemaAcceso.anguloDefault} grado(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            if self.sistemaAcceso.servo2Activo():
                self.sistemaAcceso.bajarPluma2(linea)
            else:
                messagebox.showerror('Error', 'La pluma esta desactivada')
        else:
            messagebox.showerror('Error', 'El sistema de acceso debe estar activo')

    def cambiarEstadoPluma(self):
        if self.sistemaAcceso.estaActivo():
            self.sistemaAcceso.cambiarEstadoServo()
            estado = "Activa" if self.sistemaAcceso.estadoServo else "Inactiva"
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado de la pluma de entrada: {estado}," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.lblEstadoPluma.configure(text=f"Estado de la pluma de entrada: {estado}")
            self.btnEstadoPluma['text'] = "Desactivar pluma" if self.sistemaAcceso.servoActivo() else "Activar pluma"
            self.sistemaAcceso.registrarEnBitacora(linea)
        else:
            messagebox.showerror('Error', 'El sistema de acceso debe estar activo')
            
    def cambiarEstadoPluma2(self):
        if self.sistemaAcceso.estaActivo():
            self.sistemaAcceso.cambiarEstadoServo2()
            estado = "Activa" if self.sistemaAcceso.estadoServo2 else "Inactiva"
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado de la pluma de salida: {estado}," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.lblEstadoPluma2.configure(text=f"Estado de la pluma de salida: {estado}")
            self.btnEstadoPluma2['text'] = "Desactivar pluma" if self.sistemaAcceso.servo2Activo() else "Activar pluma"
            self.sistemaAcceso.registrarEnBitacora(linea)
        else:
            messagebox.showerror('Error', 'El sistema de acceso debe estar activo')
        
    def cambiarEstadoSensorAlarma(self):
        if self.sistemaAlarma.estaActivo():
            self.sistemaAlarma.cambiarEstadoSensor()
            estado = "Activo" if self.sistemaAlarma.sensorActivo() else "Inactivo"
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado de sensor de movimiento: {estado}," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.lblEstadoSensor.configure(text=f"Estado del sensor: {estado}")
            self.btnEstadoSensor['text'] = "Desactivar sensor" if self.sistemaAlarma.sensorActivo() else "Activar sensor"
            self.sistemaAlarma.registrarEnBitacora(linea)
            if self.sistemaAlarma.sensorActivo():
                self.threadAlarma.start()
            else:
                self.threadAlarma = threading.Thread(target=self.lecturaSensor)
        else:
            messagebox.showerror('Error', 'El sistema de alarma debe estar activo')

    def cambiarEstadoSensorTemperatura(self):
        if self.sistemaAire.estaActivo():
            self.sistemaAire.cambiarEstadoSensor()
            estado = "Activo" if self.sistemaAire.sensorActivo() else "Inactivo"
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado de sensor de temperatura: {estado}," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.lblEstadoSensorT.configure(text=f"Estado del sensor: {estado}")
            self.btnEstadoSensorT['text'] = "Desactivar sensor" if self.sistemaAire.sensorActivo() else "Activar sensor"
            self.sistemaAire.registrarEnBitacora(linea)
            if self.sistemaAire.sensorActivo():
                self.threadTemperatura.start()
            else:
                self.threadTemperatura = threading.Thread(target=self.lecturaSensorTemperatura)
        else:
            messagebox.showerror('Error', 'El sistema de aire acondicionado debe estar activo')

    def lecturaSensorTemperatura(self):
        while self.sistemaAire.sensorActivo():
            temp, humedad = self.sistemaAire.Dht11()
            self.lblLecturaSensorT.configure(text=f'Ultima lectura: {temp} °C')
            if temp > self.sistemaAire.gradosSensor:
                linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] La temperatura ambiente excedio la maxima establecida"\
                        f" con {temp} °C, se procedio a activar la refrigeracion\n"
                print('Encendiendo ventilador')
                GPIO.output(self.sistemaAlarma.pinled,True)
                self.sistemaAire.registrarEnBitacora(linea)
            else:
                GPIO.output(self.sistemaAlarma.pinled,True)
            
    def cambiarTemperatura(self):
        if self.sistemaAire.estaActivo():
            try:
                tmp = simpledialog.askinteger('Cambiar grados de temperatura maxima',
                                                    'Ingrese los grados de temperatura entre 1 y 100 °C')
                while tmp < 1 or tmp > 100:
                    tmp = simpledialog.askinteger('Cambiar grados de temperatura maxima',
                                                        'Ingrese los grados de temperatura entre 1 y 100 °C')
            except:
                tmp = 50
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Cambio el maximo de temperatura a {tmp} °C," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.sistemaAire.establecerGradosSensor(tmp, linea)
            self.lblTmpEstablecida.configure(text=f"Temperatura establecida: {self.sistemaAire.gradosSensor} °C")
        else:
            messagebox.showerror('Error', 'El sistema de aire acondicionado debe estar activo')