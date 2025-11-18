
import tkinter as tk
from tkinter import messagebox
import mariadb
import sys
import subprocess
import os

# FUNCIÓN PARA CONECTAR A MARIADB
def conectar():
    try:
        conexion = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="sistecurcap"
        )
        return conexion
    
    except mariadb.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a MariaDB\n{e}")
        return None


# FUNCIÓN PARA INICIAR SESIÓN
def login():
    usuario = entry_usuario.get()
    password = entry_password.get()

    if usuario == "" or password == "":
        messagebox.showwarning("Campos vacíos", "Debe llenar usuario y contraseña por favor.")
        return

    conexion = conectar()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()
        query = """
            SELECT u.id, u.usuario, r.nombre 
            FROM usuarios u 
            INNER JOIN roles r ON u.rolid = r.id 
            WHERE u.usuario=%s AND u.clave=%s
        """
        
        cursor.execute(query, (usuario, password))
        resultado = cursor.fetchone()
        rol = resultado[-1]
        ventana_login.destroy()
        
        if resultado:
            #id, username, rol = rol1
            #messagebox.showinfo("Acceso concedido", f"Bienvenido: {username}\nRol: {rol}")
            
            if rol == "Administrador":
                #Usuario con privilegios de Administrador
                parametro_a_pasar = "Administrador"
                comando = ["python", "Principal.py", parametro_a_pasar]
                subprocess.run(comando)
                sys.exit()
                #ventana_admin()
            else:
                #Usuario con privilegios normales
                parametro_a_pasar = "Usuario"
                comando = ["python", "Principal.py", parametro_a_pasar]
                subprocess.run(comando)
                sys.exit()
                #ventana_usuario()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        
        
        cursor.close()
        conexion.close()

    except mariadb.Error as e:
        messagebox.showerror("Error en el query", f"{e}")


# VENTANA DE LOGIN
ventana_login = tk.Tk()
ventana_login.title("Login - Inicio de sesión")
ventana_login.geometry("300x180")
ventana_login.configure(bg='lightblue')
ventana_login.resizable(False, False)
icono_imagen = tk.PhotoImage(file="usuario.ico")
ventana_login.iconphoto(True, icono_imagen)

tk.Label(ventana_login, text="Usuario:", bg='lightblue', font=('Helvetica', 12, 'bold')).pack(pady=5)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack()
entry_usuario.focus()

tk.Label(ventana_login, text="Contraseña:", bg='lightblue', font=('Helvetica', 12, 'bold')).pack(pady=5)
entry_password = tk.Entry(ventana_login, show="*")
entry_password.pack()

tk.Button(ventana_login, text="Iniciar sesión", command=login, font=('Helvetica', 12, 'bold')).pack(pady=20)

ventana_login.mainloop()