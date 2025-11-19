
import subprocess
import datetime
import os
from tkinter import *
from tkinter import filedialog, messagebox

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        entrada_ruta.delete(0, END)
        entrada_ruta.insert(0, carpeta)

def salir():
    ventana.destroy()

def respaldar_bd():
    usuario = entrada_usuario.get()
    #contra = entrada_contra.get()
    bd = entrada_bd.get()
    ruta = entrada_ruta.get()

    if not all([usuario,  bd, ruta]):
        messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
        return

    fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = os.path.join(ruta, f"respaldo_{bd}_{fecha}.sql")

    comando = ["C:\\xampp\\mysql\\bin\\mysqldump.exe", "-u", usuario,  bd]

    try:
        with open(archivo, "w", encoding="utf-8") as salida:
            resultado = subprocess.run(comando, stdout=salida, stderr=subprocess.PIPE, text=True)

        if resultado.returncode == 0:
            messagebox.showinfo("Éxito", f"Respaldo generado:\n{archivo}")
        else:
            messagebox.showerror("Error", f"Fallo al respaldar:\n{resultado.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Interfaz gráfica
ventana = Tk()
ventana.title("Respaldo de Base de Datos - SISTECURCAP")
ventana.geometry("420x310")

Label(ventana, text="Usuario MySQL:", font=("Arial", 10, "bold")).pack()
entrada_usuario = Entry(ventana)
entrada_usuario.pack(pady=4)

Label(ventana, text="Contraseña:", font=("Arial", 10, "bold")).pack()
entrada_contra = Entry(ventana, show="*")
entrada_contra.pack(pady=4)

Label(ventana, text="Nombre de la Base de Datos:", font=("Arial", 10, "bold")).pack()
entrada_bd = Entry(ventana)
entrada_bd.pack(pady=4)

Label(ventana, text="Carpeta de respaldo:", font=("Arial", 10, "bold")).pack()
frame_ruta = Frame(ventana)
frame_ruta.pack(pady=4)
entrada_ruta = Entry(frame_ruta, width=35)
entrada_ruta.pack(side=LEFT)
Button(frame_ruta, text="Examinar", command=seleccionar_carpeta, fg="blue", font=("Arial", 11, "bold")).pack(side=LEFT)

Button(ventana, text="Generar Respaldo", command=respaldar_bd, fg="blue", font=("Arial", 11, "bold")).pack(pady=5)
Button(ventana, text="Salir", command=salir, fg="red", font=("Arial", 11, "bold")).pack(pady=5)

ventana.mainloop()
