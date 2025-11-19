
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