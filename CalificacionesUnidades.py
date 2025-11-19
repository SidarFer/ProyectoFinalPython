
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb


class CalificacionesUnidades(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Asignación de Calificaciones por Unidad")
        self.geometry("850x550")
        self.resizable(False, False)

        # Conexión DB
        self.conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="sistecurcap"
        )
        self.cursor = self.conn.cursor()

        # Variables
        self.var_idmatricula = tk.StringVar()
        self.var_idunidad = tk.StringVar()
        self.var_calificacion = tk.StringVar()
        self.var_promedio = tk.StringVar()

        # Combos
        self.var_curso = tk.StringVar()
        self.var_estudiante = tk.StringVar()
        self.var_unidad = tk.StringVar()

        # UI
        self.crear_formulario()
        self.crear_tabla()

        # Cargar cursos
        self.cargar_cursos()

    # =================== FORMULARIO ======================
    def crear_formulario(self):
        frame = ttk.LabelFrame(self, text="Asignar Calificación", padding=10)
        frame.place(x=10, y=10, width=830, height=220)

        # CURSO
        ttk.Label(frame, text="Curso:").grid(row=0, column=0, sticky="e")
        self.cmb_curso = ttk.Combobox(frame, textvariable=self.var_curso, width=40, state="readonly")
        self.cmb_curso.grid(row=0, column=1, padx=5)
        self.cmb_curso.bind("<<ComboboxSelected>>", self.cargar_estudiantes)

        # ESTUDIANTE
        ttk.Label(frame, text="Estudiante:").grid(row=1, column=0, sticky="e")
        self.cmb_estudiante = ttk.Combobox(frame, textvariable=self.var_estudiante, width=40, state="readonly")
        self.cmb_estudiante.grid(row=1, column=1, padx=5)
        self.cmb_estudiante.bind("<<ComboboxSelected>>", self.cargar_unidades)

        # UNIDADES
        ttk.Label(frame, text="Unidad:").grid(row=2, column=0, sticky="e")
        self.cmb_unidad = ttk.Combobox(frame, textvariable=self.var_unidad, width=40, state="readonly")
        self.cmb_unidad.grid(row=2, column=1, padx=5)

        # CALIFICACIÓN
        ttk.Label(frame, text="Calificación (0 - 100):").grid(row=3, column=0, sticky="e")
        ttk.Entry(frame, textvariable=self.var_calificacion, width=15).grid(row=3, column=1, sticky="w")

        ttk.Button(frame, text="Guardar", command=self.guardar).grid(row=4, column=0, pady=10)
        ttk.Button(frame, text="Calcular Promedio", command=self.calcular_promedio).grid(row=4, column=1, pady=10, sticky="w")
        ttk.Button(frame, text="Salir", command=self.salir).grid(row=4, column=2, pady=10)

        ttk.Label(frame, text="Promedio del Curso:").grid(row=5, column=0, sticky="e")
        ttk.Entry(frame, textvariable=self.var_promedio, state="readonly", width=15).grid(row=5, column=1, sticky="w")

    # =================== TABLA CALIFICACIONES ======================
    def crear_tabla(self):
        frame = ttk.Frame(self)
        frame.place(x=10, y=240, width=830, height=300)

        columnas = ("Unidad", "Calificación")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=13)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200)

        self.tabla.pack(fill="both", expand=True)

    # =================== CARGA CURSO, ESTUDIANTE, UNIDADES ======================

    def cargar_cursos(self, event=None):
        self.cursor.execute("SELECT idcurso, nombre FROM cursos ORDER BY nombre ASC")
        cursos = [f"{idc} - {nom}" for idc, nom in self.cursor.fetchall()]
        self.cmb_curso["values"] = cursos

    def cargar_estudiantes(self, event=None):
        idcurso = self.var_curso.get().split(" - ")[0]

        sql = """SELECT m.idmatricula, e.nombres, e.apellidos
                 FROM matriculas m
                 INNER JOIN estudiantes e ON m.idestudiante = e.idestudiante
                 WHERE m.idcurso = %s"""

        self.cursor.execute(sql, (idcurso,))
        datos = self.cursor.fetchall()

        self.estudiantes_dict = {f"{n} {a}": idm for idm, n, a in datos}
        self.cmb_estudiante["values"] = list(self.estudiantes_dict.keys())

    def cargar_unidades(self, event=None):
        estudiante = self.var_estudiante.get()

        if estudiante not in self.estudiantes_dict:
            return

        self.var_idmatricula.set(self.estudiantes_dict[estudiante])
        idcurso = self.var_curso.get().split(" - ")[0]

        sql = "SELECT idunidad, nombreunidad FROM unidadescursos WHERE idcurso=%s"
        self.cursor.execute(sql, (idcurso,))
        unidades = [f"{idu} - {nom}" for idu, nom in self.cursor.fetchall()]

        self.cmb_unidad["values"] = unidades

        self.cargar_calificaciones()

    # =================== CRUD CALIFICACIONES ======================

    def cargar_calificaciones(self):
        self.tabla.delete(*self.tabla.get_children())

        if not self.var_idmatricula.get():
            return

        sql = """SELECT u.nombreunidad, c.calificacion
                 FROM calificacionesunidad c
                 INNER JOIN unidadescursos u ON c.idunidad = u.idunidad
                 WHERE c.idmatricula = %s"""

        self.cursor.execute(sql, (self.var_idmatricula.get(),))
        for fila in self.cursor.fetchall():
            self.tabla.insert("", tk.END, values=fila)

    def guardar(self):
        if not self.var_unidad.get() or not self.var_calificacion.get():
            messagebox.showwarning("Atención", "Debe seleccionar unidad y calificación.")
            return

        idunidad = self.var_unidad.get().split(" - ")[0]
        idmatricula = self.var_idmatricula.get()

        sql = "INSERT INTO calificacionesunidad(idmatricula, idunidad, calificacion) VALUES (%s,%s,%s)"
        self.cursor.execute(sql, (idmatricula, idunidad, self.var_calificacion.get()))
        self.conn.commit()

        messagebox.showinfo("Éxito", "Calificación registrada.")
        self.cargar_calificaciones()

    # =================== PROMEDIO ======================
    def calcular_promedio(self):
        sql = "SELECT AVG(calificacion) FROM calificacionesunidad WHERE idmatricula=%s"
        self.cursor.execute(sql, (self.var_idmatricula.get(),))
        promedio = self.cursor.fetchone()[0]

        if promedio is None:
            self.var_promedio.set("N/A")
        else:
            self.var_promedio.set(f"{float(promedio):.2f}")
    
    def salir(self):
        self.destroy()
    