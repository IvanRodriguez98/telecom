from SistemaAcceso import SistemaAcceso
from SistemaAlarma import SistemaAlarma
import tkinter as tk
from tkinter import messagebox, simpledialog
from Cache import Cache
import time
import threading


class App():

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sistemas Integrados")
        self.datosCache = Cache("Ivan", "Administrador")
        self.sistemaAcceso = SistemaAcceso(2349)
        self.sistemaAlarma = SistemaAlarma(1234)
        self.window.geometry("1000x450")
        self.buildApp()
        self.buildLabels()
        self.update_clock()
        self.threadAlarma = threading.Thread(target=self.lecturaSensor)
        self.threadAlarma.start()
        self.window.mainloop()

    def update_clock(self):
        now = time.strftime("%d/%m/%y %H:%M:%S")
        self.lblReloj.configure(text=now)
        self.window.after(1000, self.update_clock)

    def buildLabels(self):
        estadoSistema = "Activo" if self.sistemaAcceso.estaActivo() else "Inactivo"
        estadoServo = "Activa" if self.sistemaAcceso.servoActivo() else "Inactiva"
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
                                               text=f"Estado del sistema de alarma: {estadoSistemaAlerta}")
        self.lblEstadoSistemaAlarma.pack()
        frame_pluma = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_pluma.grid(row=9, column=0)
        self.lblEstadoPluma = tk.Label(master=frame_pluma, text=f"Estado de la pluma: {estadoServo}")
        self.lblEstadoPluma.pack()
        frame_pluma = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_pluma.grid(row=9, column=1)
        self.lblEstadoSensor = tk.Label(master=frame_pluma, text=f"Estado de sensor: {estadoSensorAlarma}")
        self.lblEstadoSensor.pack()
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
        frame_1_6 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_1_6.grid(row=10, column=1)
        self.btnEstadoSensor = tk.Button(master=frame_1_6, text="Desactivar sensor",
                                         command=self.cambiarEstadoSensorAlarma)
        self.btnEstadoSensor.pack()

        frame_2 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2.grid(row=2, column=0)
        self.btnCambiarAngulo = tk.Button(master=frame_2, text="Cambiar angulo de pluma",
                                          command=self.cambiarAnguloPluma)
        self.btnCambiarAngulo.pack()
        frame_2_1 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2_1.grid(row=2, column=1)
        self.btnCambiarDistancia = tk.Button(master=frame_2_1, text="Cambiar distancia del sensor",
                                          command=self.cambiarDistanciaSensor)
        self.btnCambiarDistancia.pack()
        frame_3 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_3.grid(row=3, column=0)
        self.btnLevantarPluma = tk.Button(master=frame_3, text="Levantar pluma",
                                          command=self.levantarPluma)
        self.btnLevantarPluma.pack()
        frame_4 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_4.grid(row=4, column=0)
        self.btnLevantarPluma = tk.Button(master=frame_4, text="Bajar pluma",
                                          command=self.bajarPluma)
        self.btnLevantarPluma.pack()
        frame_5 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_5.grid(row=10, column=0)
        self.btnEstadoPluma = tk.Button(master=frame_5, text="Desactivar pluma", command=self.cambiarEstadoPluma)
        self.btnEstadoPluma.pack()

    def lecturaSensor(self):
        dato = 0
        while self.sistemaAlarma.sensorActivo():
            print(f'Leyendo en segundo plano {dato} distancia establecida de {self.sistemaAlarma.distanciaSensor} centimetros')
            time.sleep(2)
            dato = dato + 1

    def cambiarEstadoSistemaAcceso(self):
        if self.datosCache.usuarioEsAdministrador():
            codigo = simpledialog.askinteger('Atencion',
                                             'Ingrese el codigo de desactivacion' if self.sistemaAcceso.estaActivo() else 'Ingrese el codigo de activacion')
            if codigo == self.sistemaAcceso.codigoDesactivacion:
                self.sistemaAcceso.cambiarEstado()
                estado = "Activo" if self.sistemaAcceso.estaActivo() else "Inactivo"
                linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado del sistema: {estado}," \
                        f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
                self.lblEstadoSistemaAcceso['text'] = f"Estado del sistema de acceso: {estado}"
                self.btnDesactivar['text'] = "Desactivar" if self.sistemaAcceso.estaActivo() else "Activar"
                self.sistemaAcceso.registrarEnBitacora(linea)
            else:
                messagebox.showerror("Error", "El codigo de desactivacion es invalido")
        else:
            messagebox.showerror("Error",
                                 "Lo sentimos, pero no puede realizar esta operacion, solo un administrador puede hacerlo")

    def cambiarEstadoSistemaAlarma(self):
        if self.datosCache.usuarioEsAdministrador():
            codigo = simpledialog.askinteger('Atencion',
                                             'Ingrese el codigo de desactivacion' if self.sistemaAlarma.estaActivo() else 'Ingrese el codigo de activacion')
            if codigo == self.sistemaAlarma.codigoDesactivacion:
                self.sistemaAlarma.cambiarEstado()
                estado = "Activo" if self.sistemaAlarma.estaActivo() else "Inactivo"
                linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado del sistema: {estado}," \
                        f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
                self.lblEstadoSistemaAlarma['text'] = f"Estado del sistema de acceso: {estado}"
                self.btnDesactivarAlarma['text'] = "Desactivar" if self.sistemaAlarma.estaActivo() else "Activar"
                self.sistemaAlarma.registrarEnBitacora(linea)
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
        else:
            messagebox.showerror('Error', 'El sistema de alarma debe estar activo')

    def levantarPluma(self):
        if self.sistemaAcceso.estaActivo():
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Se esta levantando la pluma en un angulo de {self.sistemaAcceso.anguloDefault} grado(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            if self.sistemaAcceso.estadoServo:
                self.sistemaAcceso.levantarPluma(linea)
            else:
                messagebox.showerror('Error', 'La pluma esta desactivada')
        else:
            messagebox.showerror('Error', 'El sistema debe estar activo')


    def bajarPluma(self):
        if self.sistemaAcceso.estaActivo():
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Se esta levantando la pluma en un angulo de {self.sistemaAcceso.anguloDefault} grado(s)," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            if self.sistemaAcceso.estadoServo:
                self.sistemaAcceso.bajarPluma(linea)
            else:
                messagebox.showerror('Error', 'La pluma esta desactivada')
        else:
            messagebox.showerror('Error', 'El sistema debe estar activo')


    def cambiarEstadoPluma(self):
        if self.sistemaAcceso.estaActivo():
            self.sistemaAcceso.cambiarEstadoServo()
            estado = "Activa" if self.sistemaAcceso.estadoServo else "Inactiva"
            linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado de la pluma: {estado}," \
                    f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
            self.lblEstadoPluma.configure(text=f"Estado de la Pluma: {estado}")
            self.btnEstadoPluma['text'] = "Desactivar pluma" if self.sistemaAcceso.servoActivo() else "Activar pluma"
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


App()