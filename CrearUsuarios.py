
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb


class CRUDUsuarios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Gestión de Usuarios")
        self.geometry("780x520")
        self.resizable(False, False)

        # CONEXIÓN BD
        self.conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="sistecurcap"
        )
        self.cursor = self.conn.cursor()

        # VARIABLES
        self.var_id = tk.StringVar()
        self.var_usuario = tk.StringVar()
        self.var_password = tk.StringVar()
        self.var_rol = tk.StringVar()

        # UI
        self.crear_formulario()
        self.crear_tabla()

        # Cargar datos al iniciar
        self.cargar_usuarios()

    # FORMULARIO
    def crear_formulario(self):
        frame = ttk.LabelFrame(self, text="Datos del Usuario", padding=10)
        frame.place(x=10, y=10, width=760, height=250)

        ttk.Label(frame, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.var_id, width=20, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Usuario:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.var_usuario, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.var_password, width=30, show="*").grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Rol:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        roles = ttk.Combobox(frame, textvariable=self.var_rol, width=27, state="readonly")
        roles["values"] = ("Administrador", "Usuario")
        roles.grid(row=3, column=1, padx=5, pady=5)
        roles.current(0)

        # ---------- Botones ----------
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=5)

        ttk.Button(btn_frame, text="Guardar", command=self.guardar_usuario).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_usuario).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_usuario).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario).grid(row=0, column=3, padx=10)
        ttk.Button(btn_frame, text="Salir", command=self.salir).grid(row=0, column=4, padx=10)

    # TABLA
    def crear_tabla(self):
        frame_tabla = ttk.Frame(self)
        frame_tabla.place(x=10, y=200, width=760, height=290)

        columnas = ("ID", "Usuario", "Rolid")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=11)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.tabla.pack(fill="both", expand=True)

    # CRUD FUNCIONES
    def cargar_usuarios(self):
        self.tabla.delete(*self.tabla.get_children())

        sql = "SELECT id, usuario, rolid FROM usuarios"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall()

        for fila in filas:
            self.tabla.insert("", tk.END, values=fila)

    def guardar_usuario(self):
        usuario = self.var_usuario.get()
        password = self.var_password.get()
        rol = self.var_rol.get()

        if rol == "Administrador":
            rol = 1
        else:
            rol = 2    

        if usuario == "" or password == "":
            messagebox.showwarning("Advertencia", "Debe llenar todos los campos")
            return

        sql = "INSERT INTO usuarios (usuario, clave, rolid) VALUES (%s, %s, %s)"
        valores = (usuario, password, rol)
        self.cursor.execute(sql, valores)
        self.conn.commit()

        messagebox.showinfo("Éxito", "Usuario registrado")
        self.cargar_usuarios()
        self.limpiar_formulario()

    def actualizar_usuario(self):
        if self.var_id.get() == "":
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return

        sql = "UPDATE usuarios SET usuario=%s, clave=%s, rolid=%s WHERE id=%s"
        valores = (
            self.var_usuario.get(),
            self.var_password.get(),
            self.var_rol.get(),
            self.var_id.get()
        )

        self.cursor.execute(sql, valores)
        self.conn.commit()

        messagebox.showinfo("Éxito", "Usuario actualizado")
        self.cargar_usuarios()
        self.limpiar_formulario()

    def eliminar_usuario(self):
        if self.var_id.get() == "":
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario?"):
            return

        sql = "DELETE FROM usuarios WHERE id=%s"
        self.cursor.execute(sql, (self.var_id.get(),))
        self.conn.commit()

        messagebox.showinfo("Éxito", "Usuario eliminado")
        self.cargar_usuarios()
        self.limpiar_formulario()

    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        valores = self.tabla.item(seleccionado, "values")

        if valores:
            self.var_id.set(valores[0])
            self.var_usuario.set(valores[1])
            self.var_rol.set(valores[2])

            # Obtener contraseña desde la BD
            sql = "SELECT clave FROM usuarios WHERE id=%s"
            self.cursor.execute(sql, (valores[0],))
            fila = self.cursor.fetchone()
            if fila:
                self.var_password.set(fila[0])

    def limpiar_formulario(self):
        self.var_id.set("")
        self.var_usuario.set("")
        self.var_password.set("")
        self.var_rol.set("Administrador")

    def salir(self):
        self.destroy()

# Prueba independiente (ejecutar solo este archivo)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    CRUDUsuarios(root)
    root.mainloop()