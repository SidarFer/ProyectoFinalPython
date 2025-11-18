
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb

# FUNCIÓN DE CONEXIÓN A MARIA DB
def conectar():
    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="sistecurcap"
        )
        return conn
    except mariadb.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
        return None


# CRUD COMPLETO DE ESTUDIANTES
class EstudiantesWindow:

    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Gestión de Estudiantes - SISTECURCAP")
        self.win.geometry("950x520")
        self.win.resizable(False, False)

        # -------- VARIABLES --------
        self.idestudiante = tk.StringVar()
        self.ncarnet = tk.StringVar()
        self.nombres = tk.StringVar()
        self.apellidos = tk.StringVar()
        self.direccion = tk.StringVar()
        self.fechanacimiento = tk.StringVar()
        self.estado = tk.StringVar()

        # UI
        self.crear_formulario()
        self.crear_tabla()
        self.cargar_datos()

    # FORMULARIO
    def crear_formulario(self):

        frame = ttk.LabelFrame(self.win, text="Datos del Estudiante")
        frame.place(x=10, y=10, width=920, height=230)

        # Fila 1
        ttk.Label(frame, text="Carnet:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.ncarnet, width=25).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Nombres:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.nombres, width=30).grid(row=0, column=3, padx=5, pady=5)

        # Fila 2
        ttk.Label(frame, text="Apellidos:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.apellidos, width=25).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Dirección:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.direccion, width=30).grid(row=1, column=3, padx=5, pady=5)

        # Fila 3
        ttk.Label(frame, text="Fecha Nacimiento (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.fechanacimiento, width=25).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Estado:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        estado_cmb = ttk.Combobox(frame, textvariable=self.estado, width=28, state="readonly")
        estado_cmb["values"] = ("Activo", "Inactivo")
        estado_cmb.grid(row=2, column=3, padx=5, pady=5)
        estado_cmb.current(0)

        # BOTONES
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, columnspan=4, pady=10)

        ttk.Button(btn_frame, text="Guardar", width=15, command=self.guardar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Actualizar", width=15, command=self.actualizar).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar", width=15, command=self.eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Limpiar", width=15, command=self.limpiar).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Salir", width=15, command=self.win.destroy).grid(row=0, column=4, padx=5)

    # TABLA TREEVIEW
    def crear_tabla(self):

        frame_tabla = ttk.Frame(self.win)
        frame_tabla.place(x=10, y=250, width=920, height=250)

        columnas = (
            "idestudiante", "ncarnet", "nombres", "apellidos",
            "direccion", "fechanacimiento", "estado"
        )

        titulos = (
            "ID", "Carnet", "Nombres", "Apellidos",
            "Dirección", "Nacimiento", "Estado"
        )

        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

        for col, title in zip(columnas, titulos):
            self.tabla.heading(col, text=title)
            self.tabla.column(col, width=130)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.tabla.pack(fill="both", expand=True)

    # CARGAR DATOS
    def cargar_datos(self):
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiantes")
            registros = cursor.fetchall()

            self.tabla.delete(*self.tabla.get_children())

            for row in registros:
                self.tabla.insert("", tk.END, values=row)

            conn.close()

    # GUARDAR NUEVO
    def guardar(self):
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO estudiantes (ncarnet, nombres, apellidos, direccion, fechanacimiento, estado)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self.ncarnet.get(),
                    self.nombres.get(),
                    self.apellidos.get(),
                    self.direccion.get(),
                    self.fechanacimiento.get(),
                    self.estado.get()
                ))

                conn.commit()
                messagebox.showinfo("Éxito", "Estudiante guardado correctamente.")
                self.cargar_datos()
                self.limpiar()

            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")
            finally:
                conn.close()

    # SELECCIONAR FILA
    def seleccionar_fila(self, event):
        item = self.tabla.selection()
        if not item:
            return

        fila = self.tabla.item(item)["values"]

        self.idestudiante.set(fila[0])
        self.ncarnet.set(fila[1])
        self.nombres.set(fila[2])
        self.apellidos.set(fila[3])
        self.direccion.set(fila[4])
        self.fechanacimiento.set(fila[5])
        self.estado.set(fila[6])

    # ACTUALIZAR
    def actualizar(self):
        if self.idestudiante.get() == "":
            messagebox.showwarning("Advertencia", "Seleccione un estudiante.")
            return

        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE estudiantes
                    SET ncarnet=?, nombres=?, apellidos=?, direccion=?, fechanacimiento=?, estado=?
                    WHERE idestudiante=?
                """, (
                    self.ncarnet.get(),
                    self.nombres.get(),
                    self.apellidos.get(),
                    self.direccion.get(),
                    self.fechanacimiento.get(),
                    self.estado.get(),
                    self.idestudiante.get()
                ))

                conn.commit()
                messagebox.showinfo("Éxito", "Estudiante actualizado.")
                self.cargar_datos()

            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")
            finally:
                conn.close()

    # ELIMINAR
    def eliminar(self):
        if self.idestudiante.get() == "":
            messagebox.showwarning("Advertencia", "Seleccione un estudiante.")
            return

        if not messagebox.askyesno("Confirmar", "¿Desea eliminar este estudiante?"):
            return

        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM estudiantes WHERE idestudiante=?", (self.idestudiante.get(),))
                conn.commit()
                messagebox.showinfo("Éxito", "Estudiante eliminado.")
                self.cargar_datos()
                self.limpiar()

            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
            finally:
                conn.close()

    # LIMPIAR FORMULARIO
    def limpiar(self):
        self.idestudiante.set("")
        self.ncarnet.set("")
        self.nombres.set("")
        self.apellidos.set("")
        self.direccion.set("")
        self.fechanacimiento.set("")
        self.estado.set("Activo")  # valor por defecto