
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb


class CRUDCursos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Gestión de Cursos")
        self.geometry("900x600")
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

        # VARIABLES DEL CURSO
        self.var_idcurso = tk.StringVar()
        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_tipo = tk.StringVar()
        self.var_horas = tk.StringVar()
        self.var_fechainicio = tk.StringVar()
        self.var_fechafin = tk.StringVar()

        # UI CURSOS
        self.crear_form_cursos()
        self.crear_tabla_cursos()

        # Cargar cursos al iniciar
        self.cargar_cursos()

    # ----------- FORMULARIO DE CURSOS --------------
    def crear_form_cursos(self):
        frame = ttk.LabelFrame(self, text="Datos del Curso", padding=10)
        frame.place(x=10, y=10, width=880, height=250)

        labels = ["Id Curso:", "Código:", "Nombre:", "Tipo:", "Horas:",
                  "Fecha Inicio (AAAA-MM-DD):", "Fecha Fin (AAAA-MM-DD):"]

        vars = [self.var_idcurso, self.var_codigo, self.var_nombre,
                self.var_tipo, self.var_horas,
                self.var_fechainicio, self.var_fechafin]

        for i, (lbl, var) in enumerate(zip(labels, vars)):
            ttk.Label(frame, text=lbl).grid(row=i, column=0, sticky="e", pady=3)
            entry_state = "readonly" if i == 0 else "normal"
            ttk.Entry(frame, textvariable=var, width=40, state=entry_state).grid(row=i, column=1, pady=3, padx=5)

        ttk.Button(frame, text="Guardar", command=self.guardar_curso).grid(row=0, column=2, padx=10)
        ttk.Button(frame, text="Actualizar", command=self.actualizar_curso).grid(row=1, column=2, padx=10)
        ttk.Button(frame, text="Eliminar", command=self.eliminar_curso).grid(row=2, column=2, padx=10)
        ttk.Button(frame, text="Limpiar", command=self.limpiar_form).grid(row=3, column=2, padx=10)
        ttk.Button(frame, text="Unidades", command=self.abrir_unidades).grid(row=4, column=2, padx=10)
        
    # ----------- TABLA CURSOS ----------------
    def crear_tabla_cursos(self):
        frame = ttk.Frame(self)
        frame.place(x=10, y=250, width=880, height=350)

        columnas = ("ID", "Código", "Nombre", "Tipo", "Horas", "Inicio", "Fin")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=13)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)

    # ----------- CRUD DE CURSOS ----------------
    def cargar_cursos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.cursor.execute("SELECT idcurso, codigo, nombre, tipo, horas, fechainicio, fechafin FROM cursos")
        for fila in self.cursor.fetchall():
            self.tabla.insert("", tk.END, values=fila)

    def guardar_curso(self):
        datos = (
            self.var_codigo.get(),
            self.var_nombre.get(),
            self.var_tipo.get(),
            self.var_horas.get(),
            self.var_fechainicio.get(),
            self.var_fechafin.get()
        )

        sql = """INSERT INTO cursos (codigo, nombre, tipo, horas, fechainicio, fechafin)
                 VALUES (%s,%s,%s,%s,%s,%s)"""

        self.cursor.execute(sql, datos)
        self.conn.commit()
        messagebox.showinfo("Éxito", "Curso guardado.")
        self.cargar_cursos()
        self.limpiar_form()

    def actualizar_curso(self):
        if not self.var_idcurso.get():
            messagebox.showwarning("Atención", "Seleccione un curso.")
            return

        datos = (
            self.var_codigo.get(),
            self.var_nombre.get(),
            self.var_tipo.get(),
            self.var_horas.get(),
            self.var_fechainicio.get(),
            self.var_fechafin.get(),
            self.var_idcurso.get()
        )

        sql = """UPDATE cursos SET codigo=%s, nombre=%s, tipo=%s, horas=%s,
                 fechainicio=%s, fechafin=%s WHERE idcurso=%s"""

        self.cursor.execute(sql, datos)
        self.conn.commit()
        messagebox.showinfo("Éxito", "Curso actualizado.")
        self.cargar_cursos()
        self.limpiar_form()

    def eliminar_curso(self):
        if not self.var_idcurso.get():
            messagebox.showwarning("Atención", "Seleccione un curso.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar curso? También eliminará sus unidades."):
            return

        self.cursor.execute("DELETE FROM unidadescursos WHERE idcurso=%s", (self.var_idcurso.get(),))
        self.cursor.execute("DELETE FROM cursos WHERE idcurso=%s", (self.var_idcurso.get(),))
        self.conn.commit()

        messagebox.showinfo("Éxito", "Curso eliminado.")
        self.cargar_cursos()
        self.limpiar_form()

    def seleccionar_fila(self, event):
        item = self.tabla.focus()
        valores = self.tabla.item(item, "values")

        if valores:
            self.var_idcurso.set(valores[0])
            self.var_codigo.set(valores[1])
            self.var_nombre.set(valores[2])
            self.var_tipo.set(valores[3])
            self.var_horas.set(valores[4])
            self.var_fechainicio.set(valores[5])
            self.var_fechafin.set(valores[6])

    def limpiar_form(self):
        self.var_idcurso.set("")
        self.var_codigo.set("")
        self.var_nombre.set("")
        self.var_tipo.set("")
        self.var_horas.set("")
        self.var_fechainicio.set("")
        self.var_fechafin.set("")

    # ----------- ABRIR VENTANA DE UNIDADES -------------
    def abrir_unidades(self):
        if not self.var_idcurso.get():
            messagebox.showwarning("Atención", "Seleccione un curso para ver sus unidades.")
            return

        CRUDUnidades(self, self.var_idcurso.get())

class CRUDUnidades(tk.Toplevel):
    def __init__(self, master, idcurso):
        super().__init__(master)

        self.idcurso = idcurso
        self.title("Unidades del Curso")
        self.geometry("600x450")

        # BD
        self.conn = master.conn
        self.cursor = master.cursor

        # VARIABLES
        self.var_idunidad = tk.StringVar()
        self.var_nombreunidad = tk.StringVar()
        self.var_numero = tk.StringVar()

        self.crear_formulario()
        self.crear_tabla()
        self.cargar_unidades()

    def crear_formulario(self):
        frame = ttk.LabelFrame(self, text="Datos Unidad", padding=10)
        frame.pack(side="top", fill="x")

        ttk.Label(frame, text="ID Unidad:").grid(row=0, column=0)
        ttk.Entry(frame, textvariable=self.var_idunidad, state="readonly").grid(row=0, column=1)

        ttk.Label(frame, text="Nombre Unidad:").grid(row=1, column=0)
        ttk.Entry(frame, textvariable=self.var_nombreunidad, width=25).grid(row=1, column=1)

        ttk.Label(frame, text="Número Unidad:").grid(row=2, column=0)
        ttk.Entry(frame, textvariable=self.var_numero, width=10).grid(row=2, column=1)

        ttk.Button(frame, text="Guardar", command=self.guardar).grid(row=0, column=2, padx=10)
        ttk.Button(frame, text="Actualizar", command=self.actualizar).grid(row=1, column=2, padx=10)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=2, column=2, padx=10)
        #ttk.Button(frame, text="Salir", command=self.destroy()).grid(row=3, column=2, padx=10)

    def crear_tabla(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True)

        columnas = ("ID", "Nombre Unidad", "Número")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.tabla.pack(expand=True, fill="both")
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar)

    def cargar_unidades(self):
        self.tabla.delete(*self.tabla.get_children())
        sql = "SELECT idunidad, nombreunidad, numerounidad FROM unidadescursos WHERE idcurso=%s"
        self.cursor.execute(sql, (self.idcurso,))
        for fila in self.cursor.fetchall():
            self.tabla.insert("", tk.END, values=fila)

    def guardar(self):
        sql = "INSERT INTO unidadescursos(idcurso, nombreunidad, numerounidad) VALUES (%s,%s,%s)"
        self.cursor.execute(sql, (self.idcurso, self.var_nombreunidad.get(), self.var_numero.get()))
        self.conn.commit()
        self.cargar_unidades()

    def actualizar(self):
        sql = "UPDATE unidadescursos SET nombreunidad=%s, numerounidad=%s WHERE idunidad=%s"
        self.cursor.execute(sql, (self.var_nombreunidad.get(), self.var_numero.get(), self.var_idunidad.get()))
        self.conn.commit()
        self.cargar_unidades()

    def eliminar(self):
        sql = "DELETE FROM unidadescursos WHERE idunidad=%s"
        self.cursor.execute(sql, (self.var_idunidad.get(),))
        self.conn.commit()
        self.cargar_unidades()

    def seleccionar(self, event):
        item = self.tabla.focus()
        valores = self.tabla.item(item, "values")
        if valores:
            self.var_idunidad.set(valores[0])
            self.var_nombreunidad.set(valores[1])
            self.var_numero.set(valores[2])

    