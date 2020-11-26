from SistemaAcceso import SistemaAcceso
import tkinter as tk
from tkinter import messagebox,simpledialog
from Cache import Cache
import time

class App():

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Centro de Datos")
        self.datosCache = Cache("Ivan","Administrador")
        self.sistemaAcceso = SistemaAcceso(2349)
        self.window.geometry("1000x800")
        self.buildApp()
        self.buildLabels()
        self.window.mainloop()

    def buildLabels(self):
        estadoSistema = "Activo" if self.sistemaAcceso.estaActivo() else "Inactivo"
        estadoServo = "Activa" if self.sistemaAcceso.servoActivo() else "Inactiva"
        frame_nombre = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_nombre.grid(row=0, column=0)
        self.lblEstadoSistemaAcceso = tk.Label(master=frame_nombre, text=f"Estado del Sistema: {estadoSistema}")
        self.lblEstadoSistemaAcceso.pack()
        frame_pluma = tk.Frame(
            master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_pluma.grid(row=9, column=0)
        self.lblEstadoPluma = tk.Label(master=frame_pluma, text=f"Estado de la pluma: {estadoServo}")
        self.lblEstadoPluma.pack()

    def buildApp(self):
        frame_1 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_1.grid(row=1, column=0)
        self.btnDesactivar = tk.Button(master=frame_1, text="Desactivar", command=self.cambiarEstadoSistemaAcceso)
        self.btnDesactivar.pack()
        frame_2 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_2.grid(row=2, column=0)
        self.btnCambiarAngulo = tk.Button(master=frame_2, text="Cambiar angulo de pluma", command=self.cambiarAnguloPluma)
        self.btnCambiarAngulo.pack()
        frame_3 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_3.grid(row=3, column=0)
        self.btnLevantarPluma= tk.Button(master=frame_3, text="Levantar pluma",
                                          command=self.levantarPluma)
        self.btnLevantarPluma.pack()
        frame_4 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_4.grid(row=4, column=0)
        self.btnLevantarPluma = tk.Button(master=frame_4, text="Bajar pluma",
                                          command=self.bajarPluma)
        self.btnLevantarPluma.pack()
        frame_5 = tk.Frame(master=self.window, relief=tk.RAISED, borderwidth=0)
        frame_5.grid(row=10, column=0)
        self.btnEstadoPluma = tk.Button(master=frame_5, text="Desactivar pluma",
                                          command=self.cambiarEstadoPluma)
        self.btnEstadoPluma.pack()

    def cambiarEstadoSistemaAcceso(self):
        if self.datosCache.usuarioEsAdministrador():
            codigo = simpledialog.askinteger('Atencion','Ingrese el codigo de desactivacion' if self.sistemaAcceso.estaActivo() else 'Ingrese el codigo de activacion')
            if codigo == self.sistemaAcceso.codigoDesactivacion:
                self.sistemaAcceso.cambiarEstado()
                estado = "Activo" if self.sistemaAcceso.estaActivo() else "Inactivo"
                linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado del sistema: {estado}," \
                                        f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
                self.lblEstadoSistemaAcceso['text'] = f"Estado del Sistema: {estado}"
                self.btnDesactivar['text'] = "Desactivar" if self.sistemaAcceso.estaActivo() else "Activar"
                self.sistemaAcceso.registrarEnBitacora(linea)
            else:
                messagebox.showerror("Error","El codigo de desactivacion es invalido")
        else:
            messagebox.showerror("Error","Lo sentimos, pero no puede realizar esta operacion, solo un administrador puede hacerlo")

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
            messagebox.showerror('Error','El sistema debe estar activo')


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
                estado = "Activa" if self.sistemaAcceso.estaActivo() else "Inactiva"
                linea = f"[{time.strftime('%d-%b-%Y %H:%M:%S')}] Estado de la pluma: {estado}," \
                                        f" operacion realizada por: {self.datosCache.usuario} con rol {self.datosCache.rol}\n"
                self.lblEstadoPluma['text'] = f"Estado de la Pluma: {estado}"
                self.btnEstadoPluma['text'] = "Desactivar pluma" if self.sistemaAcceso.servoActivo() else "Activar pluma"
                self.sistemaAcceso.registrarEnBitacora(linea)
        else:
            messagebox.showerror('Error', 'El sistema debe estar activo')

App()