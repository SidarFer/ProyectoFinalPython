
import subprocess
import os
from tkinter import *
from tkinter import filedialog, messagebox

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo SQL",
        filetypes=[("SQL Files", "*.sql")]
    )
    if archivo:
        entrada_archivo.delete(0, END)
        entrada_archivo.insert(0, archivo)

def salir():
    ventana.destroy()

def restaurar_bd():
    usuario = entrada_usuario.get()
    contra = entrada_contra.get()
    bd = entrada_bd.get()
    archivo = entrada_archivo.get()

    if not all([usuario, bd, archivo]):
        messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
        return

    # Comando mysql
    comando = [
        "mysql",
        "-u", usuario,
        "-p" + contra,
        bd
    ]

    try:
        with open(archivo, "r", encoding="utf-8") as contenido:
            resultado = subprocess.run(
                comando,
                stdin=contenido,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        if resultado.returncode == 0:
            messagebox.showinfo("Éxito", "La base de datos fue restaurada correctamente.")
        else:
            messagebox.showerror("Error", f"Fallo al restaurar:\n{resultado.stderr}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Interfaz gráfica
ventana = Tk()
ventana.title("Restaurar Base de Datos - SISTECURCAP")
ventana.geometry("420x300")

Label(ventana, text="Usuario MySQL:", font=("Arial", 10, "bold")).pack()
entrada_usuario = Entry(ventana)
entrada_usuario.pack()

Label(ventana, text="Contraseña:", font=("Arial", 10, "bold")).pack()
entrada_contra = Entry(ventana, show="*")
entrada_contra.pack()

Label(ventana, text="Nombre de la Base de Datos:", font=("Arial", 10, "bold")).pack()
entrada_bd = Entry(ventana)
entrada_bd.pack()

Label(ventana, text="Archivo .sql a restaurar:", font=("Arial", 10, "bold")).pack()
frame_archivo = Frame(ventana)
frame_archivo.pack()

entrada_archivo = Entry(frame_archivo, width=35)
entrada_archivo.pack(side=LEFT)

Button(frame_archivo, text="Examinar", command=seleccionar_archivo, fg="blue", font=("Arial", 11, "bold")).pack(side=LEFT)
Button(ventana, text="Restaurar Base de Datos", command=restaurar_bd, fg="blue", font=("Arial", 11, "bold")).pack(pady=20)
Button(ventana, text="Salir", command=salir, fg="red", font=("Arial", 11, "bold")).pack(pady=5)

ventana.mainloop()