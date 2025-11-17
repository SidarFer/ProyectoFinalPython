
import tkinter as tk
from tkinter import messagebox
import mariadb

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

        if resultado:
            id, username, rol = resultado
            messagebox.showinfo("Acceso concedido", f"Bienvenido: {username}\nRol: {rol}")
            ventana_login.destroy()

            if rol == "Administrador":
                #Usuario con privilegios de Administrador
                ventana_admin()
            else:
                #Usuario con privilegios normales
                ventana_usuario()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

        cursor.close()
        conexion.close()

    except mariadb.Error as e:
        messagebox.showerror("Error en el query", f"{e}")


# PANEL PARA ADMINISTRADORES
def ventana_admin():
    admin = tk.Tk()
    admin.title("Panel Administrador")

    tk.Label(admin, text="Bienvenido Administrador", font=("Arial", 16)).pack(pady=20)

    tk.Button(admin, text="Gestión de Usuarios", width=25).pack(pady=5)
    tk.Button(admin, text="Configuraciones del Sistema", width=25).pack(pady=5)
    tk.Button(admin, text="Salir", command=admin.destroy).pack(pady=20)

    admin.mainloop()


# PANEL PARA USUARIOS NORMALES
def ventana_usuario():
    user = tk.Tk()
    user.title("Panel Usuario")

    tk.Label(user, text="Bienvenido Usuario", font=("Arial", 16)).pack(pady=20)

    tk.Button(user, text="Ver Perfil", width=25).pack(pady=5)
    tk.Button(user, text="Salir", command=user.destroy).pack(pady=20)

    user.mainloop()


# VENTANA DE LOGIN
ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("300x230")
ventana_login.resizable(False, False)

tk.Label(ventana_login, text="Usuario:").pack(pady=5)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack()

tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
entry_password = tk.Entry(ventana_login, show="*")
entry_password.pack()

tk.Button(ventana_login, text="Iniciar sesión", command=login).pack(pady=20)

ventana_login.mainloop()