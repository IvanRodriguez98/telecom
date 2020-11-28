from main import App
import tkinter as tk
from tkinter import messagebox,StringVar

def ingresar():
    user = usuario.get()
    clave = password.get()
    with open('usuarios.txt','r') as file:
        match = False
        for cadena in file.readlines():
            nombre,rol,contrasenia,codigo1,codigo2,codigo3 = cadena.split(',')
            if nombre == user and clave == contrasenia:
                match = True
                break
            else:
                pass
        if match:
            login.destroy()
            App(usuario=nombre,rol=rol,codigo1=int(codigo1),codigo2=int(codigo2),codigo3=int(codigo3))
        else:
            messagebox.showwarning('Advertencia','Usuario o contraseña incorrectos')

global login,usuario,password
login = tk.Tk()
login.geometry('300x250')
usuario = StringVar()
password = StringVar()
lblNombre = tk.Label(text='Usuario').pack()
txtUsuario = tk.Entry(login,textvariable=usuario).pack()
lblPass = tk.Label(login,text='Contraseña').pack()
txtPass = tk.Entry(login,textvariable=password).pack()
btn = tk.Button(login,text='Ingresar',command=ingresar).pack()
login.title('Login')
login.mainloop()