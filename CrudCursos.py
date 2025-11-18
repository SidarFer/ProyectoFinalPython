
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb

# CONEXIÓN A LA BASE DE DATOS
def conectar():
    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            database="sistecurcap",
            port=3306
        )
        return conn
    except mariadb.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la BD\n{e}")
        return None


#        CLASE PRINCIPAL DEL CRUD DE CURSOS
class CursosWindow:

    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Gestión de Cursos - SISTECURCAP")
        self.win.geometry("900x500")

        # === VARIABLES ===
        self.idcurso = tk.StringVar()
        self.codigo = tk.StringVar()
        self.nombre = tk.StringVar()
        self.tipo = tk.StringVar()
        self.horas = tk.StringVar()
        self.fechainicio = tk.StringVar()
        self.fechafin = tk.StringVar()

        # Construcción UI
        self.crear_formulario()
        self.crear_tabla()
        self.cargar_datos()

    # CREAR FORMULARIO
    def crear_formulario(self):

        frame = ttk.LabelFrame(self.win, text="Datos del Curso")
        frame.place(x=10, y=10, width=760, height=250)
        #frame.pack(fill="x", padx=10, pady=10)

        # Código
        ttk.Label(frame, text="Código:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.codigo).grid(row=0, column=1, padx=5, pady=5)

        # Nombre
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.nombre).grid(row=1, column=1, padx=5, pady=5)

        # Tipo
        ttk.Label(frame, text="Tipo:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.tipo).grid(row=2, column=1, padx=5, pady=5)

        # Horas
        ttk.Label(frame, text="Horas:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.horas).grid(row=3, column=1, padx=5, pady=5)

        # Fecha Inicio
        ttk.Label(frame, text="Fecha Inicio (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.fechainicio).grid(row=4, column=1, padx=5, pady=5)

        # Fecha Fin
        ttk.Label(frame, text="Fecha Fin (YYYY-MM-DD):").grid(row=5, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.fechafin).grid(row=5, column=1, padx=5, pady=5)

        # BOTONES
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self.guardar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Salir", command=self.salir).grid(row=0, column=4, padx=5)

    # TABLA TREEVIEW
    def crear_tabla(self):

        frame_tabla = ttk.Frame(self.win)  # ← CORREGIDO
        frame_tabla.place(x=10, y=270, width=860, height=200)

        columnas = ("idcurso", "codigo", "nombre", "tipo", "horas", "inicio", "fin")
        titulos = ["ID", "Código", "Nombre", "Tipo", "Horas", "Inicio", "Fin"]

        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=9)

        for col, title in zip(columnas, titulos):
            self.tabla.heading(col, text=title)
            self.tabla.column(col, width=120)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.tabla.pack(fill="both", expand=True)

    
    # CARGAR DATOS
    def cargar_datos(self):
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cursos")
            registros = cursor.fetchall()

            for item in self.tabla.get_children():
                self.tabla.delete(item)

            for row in registros:
                self.tabla.insert("", tk.END, values=row)

            conn.close()

    # GUARDAR NUEVO CURSO
    def guardar(self):
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO cursos (codigo, nombre, tipo, horas, fechainicio, fechafin)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.codigo.get(), self.nombre.get(), self.tipo.get(),
                      self.horas.get(), self.fechainicio.get(), self.fechafin.get()))

                conn.commit()
                messagebox.showinfo("Éxito", "Curso guardado correctamente.")
                self.cargar_datos()
                self.limpiar()

            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar.\n{e}")
            finally:
                conn.close()

    # SELECCIONAR FILA
    def seleccionar_fila(self, event):
        item = self.tabla.selection()
        if not item:
            return

        fila = self.tabla.item(item)["values"]

        self.idcurso.set(fila[0])
        self.codigo.set(fila[1])
        self.nombre.set(fila[2])
        self.tipo.set(fila[3])
        self.horas.set(fila[4])
        self.fechainicio.set(fila[5])
        self.fechafin.set(fila[6])

    # ACTUALIZAR REGISTRO
    def actualizar(self):
        if self.idcurso.get() == "":
            messagebox.showwarning("Advertencia", "Seleccione un curso.")
            return

        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE cursos SET codigo=?, nombre=?, tipo=?, horas=?, 
                        fechainicio=?, fechafin=? WHERE idcurso=?
                """, (self.codigo.get(), self.nombre.get(), self.tipo.get(),
                      self.horas.get(), self.fechainicio.get(),
                      self.fechafin.get(), self.idcurso.get()))

                conn.commit()
                messagebox.showinfo("Éxito", "Curso actualizado.")
                self.cargar_datos()
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo actualizar.\n{e}")
            finally:
                conn.close()

    # ELIMINAR REGISTRO
    def eliminar(self):
        if self.idcurso.get() == "":
            messagebox.showwarning("Advertencia", "Seleccione un curso.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar este curso?"):
            return

        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cursos WHERE idcurso=?", (self.idcurso.get(),))
                conn.commit()
                messagebox.showinfo("Éxito", "Curso eliminado.")
                self.cargar_datos()
                self.limpiar()
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar.\n{e}")
            finally:
                conn.close()

    # LIMPIAR CAMPOS
    def limpiar(self):
        self.idcurso.set("")
        self.codigo.set("")
        self.nombre.set("")
        self.tipo.set("")
        self.horas.set("")
        self.fechainicio.set("")
        self.fechafin.set("")

    def salir(self):
        self.win.destroy()
