
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb

class Graduaciones(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Gestión de Graduaciones")
        self.geometry("850x550")
        self.resizable(False, False)

        # Conexión BD
        self.conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="sistecurcap"
        )
        self.cursor = self.conn.cursor()

        # Variables
        self.var_idgraduacion = tk.StringVar()
        self.var_fechagraduacion = tk.StringVar()
        self.var_resultado = tk.StringVar()
        self.var_idmatricula = tk.StringVar()

        self.var_curso = tk.StringVar()
        self.var_estudiante = tk.StringVar()

        # UI
        self.crear_formulario()
        self.crear_tabla()
        self.cargar_cursos()  # Cargar cursos al iniciar

    # =================== FORMULARIO ======================
    def crear_formulario(self):
        frame = ttk.LabelFrame(self, text="Registro de Graduación", padding=10)
        frame.place(x=10, y=10, width=830, height=180)

        # CURSO
        ttk.Label(frame, text="Curso:").grid(row=0, column=0, sticky="e")
        self.cmb_curso = ttk.Combobox(frame, textvariable=self.var_curso, width=40, state="readonly")
        self.cmb_curso.grid(row=0, column=1, padx=5)
        self.cmb_curso.bind("<<ComboboxSelected>>", self.cargar_estudiantes)

        # ESTUDIANTE
        ttk.Label(frame, text="Estudiante:").grid(row=1, column=0, sticky="e")
        self.cmb_estudiante = ttk.Combobox(frame, textvariable=self.var_estudiante, width=40, state="readonly")
        self.cmb_estudiante.grid(row=1, column=1, padx=5)
        self.cmb_estudiante.bind("<<ComboboxSelected>>", self.cargar_graduaciones)

        # FECHA GRADUACIÓN
        ttk.Label(frame, text="Fecha de Graduación (AAAA-MM-DD):").grid(row=2, column=0, sticky="e")
        ttk.Entry(frame, textvariable=self.var_fechagraduacion, width=20).grid(row=2, column=1, sticky="w")

        # RESULTADO
        ttk.Label(frame, text="Resultado:").grid(row=3, column=0, sticky="e")
        ttk.Entry(frame, textvariable=self.var_resultado, width=20).grid(row=3, column=1, sticky="w")

        # Botones
        ttk.Button(frame, text="Guardar", command=self.guardar).grid(row=0, column=2, padx=10)
        ttk.Button(frame, text="Actualizar", command=self.actualizar).grid(row=1, column=2, padx=10)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=2, column=2, padx=10)
        ttk.Button(frame, text="Limpiar", command=self.limpiar_form).grid(row=3, column=2, padx=10)

    # =================== TABLA ======================
    def crear_tabla(self):
        frame = ttk.Frame(self)
        frame.place(x=10, y=200, width=830, height=330)

        columnas = ("Estudiante", "Fecha Graduación", "Resultado")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=13)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar)

    # =================== CARGA CURSOS Y ESTUDIANTES ======================
    def cargar_cursos(self):
        self.cursor.execute("SELECT idcurso, nombre FROM cursos ORDER BY nombre ASC")
        cursos = [f"{idc} - {nom}" for idc, nom in self.cursor.fetchall()]
        self.cmb_curso["values"] = cursos

        # Seleccionar primer curso automáticamente
        if cursos:
            self.cmb_curso.current(0)
            self.cargar_estudiantes()

    def cargar_estudiantes(self, event=None):
        curso = self.var_curso.get()
        if not curso:
            return

        idcurso = curso.split(" - ")[0]

        sql = """SELECT m.idmatricula, e.nombres, e.apellidos
                 FROM matriculas m
                 INNER JOIN estudiantes e ON m.idestudiante = e.idestudiante
                 WHERE m.idcurso = %s"""
        self.cursor.execute(sql, (idcurso,))
        datos = self.cursor.fetchall()
        self.estudiantes_dict = {f"{n} {a}": idm for idm, n, a in datos}
        self.cmb_estudiante["values"] = list(self.estudiantes_dict.keys())

        # Seleccionar primer estudiante automáticamente
        if datos:
            primer_est = list(self.estudiantes_dict.keys())[0]
            self.cmb_estudiante.set(primer_est)
            self.cargar_graduaciones()

    def cargar_graduaciones(self, event=None):
        estudiante = self.var_estudiante.get()
        if estudiante not in self.estudiantes_dict:
            self.tabla.delete(*self.tabla.get_children())
            self.var_idmatricula.set("")
            return

        self.var_idmatricula.set(self.estudiantes_dict[estudiante])

        sql = """SELECT g.idgraduacion, e.nombres, e.apellidos, g.fechagraduacion, g.resultado
                 FROM graduaciones g
                 INNER JOIN matriculas m ON g.idmatricula = m.idmatricula
                 INNER JOIN estudiantes e ON m.idestudiante = e.idestudiante
                 WHERE g.idmatricula = %s"""
        self.cursor.execute(sql, (self.var_idmatricula.get(),))
        self.tabla.delete(*self.tabla.get_children())
        for fila in self.cursor.fetchall():
            est = f"{fila[1]} {fila[2]}"
            self.tabla.insert("", tk.END, values=(est, fila[3], fila[4]))
            self.var_idgraduacion.set(fila[0])

    # =================== CRUD ======================
    def guardar(self):
        if not self.var_idmatricula.get() or not self.var_fechagraduacion.get() or not self.var_resultado.get():
            messagebox.showwarning("Atención", "Complete todos los campos.")
            return

        sql = "INSERT INTO graduaciones(idmatricula, fechagraduacion, resultado) VALUES (%s,%s,%s)"
        self.cursor.execute(sql, (self.var_idmatricula.get(), self.var_fechagraduacion.get(), self.var_resultado.get()))
        self.conn.commit()
        messagebox.showinfo("Éxito", "Graduación registrada.")
        self.cargar_graduaciones()

    def actualizar(self):
        if not self.var_idgraduacion.get():
            messagebox.showwarning("Atención", "Seleccione un registro.")
            return

        sql = "UPDATE graduaciones SET fechagraduacion=%s, resultado=%s WHERE idgraduacion=%s"
        self.cursor.execute(sql, (self.var_fechagraduacion.get(), self.var_resultado.get(), self.var_idgraduacion.get()))
        self.conn.commit()
        messagebox.showinfo("Éxito", "Registro actualizado.")
        self.cargar_graduaciones()

    def eliminar(self):
        if not self.var_idgraduacion.get():
            messagebox.showwarning("Atención", "Seleccione un registro.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar este registro?"):
            return

        sql = "DELETE FROM graduaciones WHERE idgraduacion=%s"
        self.cursor.execute(sql, (self.var_idgraduacion.get(),))
        self.conn.commit()
        messagebox.showinfo("Éxito", "Registro eliminado.")
        self.cargar_graduaciones()

    # =================== SELECCIONAR FILA ======================
    def seleccionar(self, event):
        item = self.tabla.focus()
        valores = self.tabla.item(item, "values")
        if valores:
            self.var_estudiante.set(valores[0])
            self.var_fechagraduacion.set(valores[1])
            self.var_resultado.set(valores[2])

            # Obtener idgraduacion correspondiente
            sql = """SELECT g.idgraduacion
                     FROM graduaciones g
                     INNER JOIN matriculas m ON g.idmatricula = m.idmatricula
                     INNER JOIN estudiantes e ON m.idestudiante = e.idestudiante
                     WHERE CONCAT(e.nombres, ' ', e.apellidos) = %s AND g.fechagraduacion = %s"""
            self.cursor.execute(sql, (valores[0], valores[1]))
            fila = self.cursor.fetchone()
            if fila:
                self.var_idgraduacion.set(fila[0])

    # =================== LIMPIAR FORMULARIO ======================
    def limpiar_form(self):
        self.var_idgraduacion.set("")
        self.var_fechagraduacion.set("")
        self.var_resultado.set("")
        if self.cmb_estudiante["values"]:
            self.cmb_estudiante.current(0)
            self.cargar_graduaciones()