
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb

# ---- CONEXIÓN A LA BASE DE DATOS ----
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
        messagebox.showerror("Error BD", f"No se pudo conectar a la base de datos:\n{e}")
        return None


# ---------- VENTANA CRUD MATRÍCULA ------------
class MatriculaWindow:

    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Gestión de Matrículas - SISTECURCAP")
        self.win.geometry("900x550")

        # === VARIABLES ===
        self.idmatricula = tk.StringVar()
        self.estudiante = tk.StringVar()
        self.curso = tk.StringVar()
        self.fechamatricula = tk.StringVar()
        self.estado = tk.StringVar()

        # Para almacenar los IDS reales
        self.dict_estudiantes = {}
        self.dict_cursos = {}

        self.crear_formulario()
        self.crear_tabla()
        self.cargar_listas()
        self.cargar_datos()

    # FORMULARIO
    def crear_formulario(self):

        frame = ttk.LabelFrame(self.win, text="Datos de Matrícula")
        frame.place(x=20, y=10, width=820, height=230)

        ttk.Label(frame, text="Estudiante:").grid(row=0, column=0, padx=5, pady=5)
        self.cmbEst = ttk.Combobox(frame, textvariable=self.estudiante, state="readonly", width=40)
        self.cmbEst.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Curso:").grid(row=1, column=0, padx=5, pady=5)
        self.cmbCur = ttk.Combobox(frame, textvariable=self.curso, state="readonly", width=40)
        self.cmbCur.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Fecha Matrícula (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.fechamatricula).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Estado:").grid(row=3, column=0, padx=5, pady=5)
        self.cmbEstado = ttk.Combobox(frame, textvariable=self.estado, state="readonly")
        self.cmbEstado["values"] = ("Cursando", "Retirado", "Finalizado")
        self.cmbEstado.grid(row=3, column=1, padx=5, pady=5)
        self.cmbEstado.current(0)

        # BOTONES
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", width=12, command=self.guardar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Actualizar", width=12, command=self.actualizar).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar", width=12, command=self.eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Limpiar", width=12, command=self.limpiar).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Salir", width=12, command=self.win.destroy).grid(row=0, column=4, padx=5)

    # TABLA TREEVIEW
    def crear_tabla(self):
        frame = ttk.Frame(self.win)
        frame.place(x=20, y=250, width=820, height=280)

        columnas = ("id", "estudiante", "curso", "fecha", "estado")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tabla.heading(col, text=col.title())
            self.tabla.column(col, width=150)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar)

        self.tabla.pack(fill="both", expand=True)

    # CARGAR LISTAS DESPLEGABLES
    def cargar_listas(self):
        conn = conectar()
        if not conn: return
        cursor = conn.cursor()

        # Estudiantes
        cursor.execute("SELECT idestudiante, nombres, apellidos FROM estudiantes")
        self.dict_estudiantes = {f"{n} {a}": i for i, n, a in cursor.fetchall()}
        self.cmbEst["values"] = list(self.dict_estudiantes.keys())

        # Cursos
        cursor.execute("SELECT idcurso, nombre FROM cursos")
        self.dict_cursos = {nombre: idc for idc, nombre in cursor.fetchall()}
        self.cmbCur["values"] = list(self.dict_cursos.keys())

        conn.close()

    # CARGAR DATOS EN TABLA
    def cargar_datos(self):
        conn = conectar()
        if not conn: return
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.idmatricula, 
                   CONCAT(e.nombres,' ',e.apellidos),
                   c.nombre,
                   m.fechamatricula,
                   m.estado
            FROM matriculas m
            JOIN estudiantes e ON m.idestudiante=e.idestudiante
            JOIN cursos c ON m.idcurso=c.idcurso
        """)

        registros = cursor.fetchall()
        conn.close()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for row in registros:
            self.tabla.insert("", tk.END, values=row)

    # GUARDAR MATRÍCULA
    def guardar(self):
        try:
            est_id = self.dict_estudiantes[self.estudiante.get()]
            cur_id = self.dict_cursos[self.curso.get()]
            #estado = self.dict_cursos[self.estado.get()]
        except:
            messagebox.showerror("Error", "Seleccione estudiante y curso válidos.")
            return

        conn = conectar()
        if not conn: return
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO matriculas(idestudiante, idcurso, fechamatricula, estado)
                VALUES (?, ?, ?, ?)
            """, (est_id, cur_id, self.fechamatricula.get(), self.estado.get()))

            conn.commit()
            messagebox.showinfo("Éxito", "Matrícula registrada.")
            self.cargar_datos()
            self.limpiar()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")
        finally:
            conn.close()

    # SELECCIONAR REGISTRO
    def seleccionar(self, event):
        item = self.tabla.selection()
        if not item:
            return
        
        fila = self.tabla.item(item)["values"]

        self.idmatricula.set(fila[0])
        self.estudiante.set(fila[1])
        self.curso.set(fila[2])
        self.fechamatricula.set(fila[3])
        self.estado.set(fila[4])

    # ACTUALIZAR
    def actualizar(self):
        if self.idmatricula.get() == "":
            messagebox.showwarning("Advertencia", "Seleccione una matrícula.")
            return

        est_id = self.dict_estudiantes.get(self.estudiante.get(), None)
        cur_id = self.dict_cursos.get(self.curso.get(), None)

        if not est_id or not cur_id:
            messagebox.showerror("Error", "Datos inválidos.")
            return

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE matriculas SET idestudiante=?, idcurso=?, fechamatricula=?, estado=?
                WHERE idmatricula=?
            """, (est_id, cur_id, self.fechamatricula.get(), self.estado.get(), self.idmatricula.get()))

            conn.commit()
            messagebox.showinfo("Éxito", "Matrícula actualizada.")
            self.cargar_datos()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")
        finally:
            conn.close()

    # ELIMINAR
    def eliminar(self):
        if self.idmatricula.get() == "":
            messagebox.showwarning("Advertencia", "Seleccione una matrícula.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar esta matrícula?"):
            return

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM matriculas WHERE idmatricula=?", (self.idmatricula.get(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro eliminado.")
            self.cargar_datos()
            self.limpiar()

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar.\n{e}")
        finally:
            conn.close()

    # LIMPIAR CAMPOS
    def limpiar(self):
        self.idmatricula.set("")
        self.estudiante.set("")
        self.curso.set("")
        self.fechamatricula.set("")
        self.estado.set("Cursando")