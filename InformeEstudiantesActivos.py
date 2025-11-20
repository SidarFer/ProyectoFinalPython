
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mariadb
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

# ---------------------- Conexión MariaDB ----------------------
def obtener_conexion():
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
        messagebox.showerror("Error", f"No se pudo conectar a la Base de Datos: {e}")
        return None

# ---------------------- Consultas BD ----------------------
def obtener_cursos():
    conn = obtener_conexion()
    if conn is None:
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT idcurso, nombre FROM cursos ORDER BY nombre")
        datos = cur.fetchall()
        conn.close()
        return datos
    except mariadb.Error as e:
        messagebox.showerror("Error", f"Error al obtener cursos: {e}")
        return []

def estudiantes_activos_por_curso(idcurso):
    conn = obtener_conexion()
    if conn is None:
        return []

    cur = conn.cursor()
    query = """
        SELECT e.idestudiante, e.nombres, e.apellidos, e.direccion
        FROM matriculas m
        INNER JOIN estudiantes e ON m.idestudiante = e.idestudiante
        WHERE m.idcurso = ? AND e.estado = 'Inactivo'
        ORDER BY e.apellidos
    """

    try:
        cur.execute(query, (idcurso,))
        datos = cur.fetchall()
        conn.close()
        return datos
    except mariadb.Error as e:
        messagebox.showerror("Error", f"Error al consultar estudiantes: {e}")
        return []

# ---------------------- Exportar a Excel ----------------------
def generar_excel(datos, ruta, nombre_curso):
    wb = Workbook()
    ws = wb.active
    ws.title = f"Activos {nombre_curso}"[:30]

    encabezados = ["ID", "Nombres", "Apellidos", "Teléfono"]
    ws.append(encabezados)

    for fila in datos:
        ws.append(fila)

    wb.save(ruta)

# ---------------------- Exportar a PDF ----------------------
def generar_pdf(datos, ruta, nombre_curso):
    doc = SimpleDocTemplate(ruta, pagesize=letter)
    styles = getSampleStyleSheet()

    contenido = []

    titulo = Paragraph(f"Estudiantes Inactivos - {nombre_curso}", styles['Title'])
    contenido.append(titulo)

    tabla_datos = [["ID", "Nombres", "Apellidos", "Teléfono"]]
    for fila in datos:
        tabla_datos.append(list(fila))

    tabla = Table(tabla_datos)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    contenido.append(tabla)

    doc.build(contenido)

# ---------------------- Interfaz Tkinter ----------------------
class ReporteEstudiantesActivos(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Estudiantes Inactivos por Curso")
        self.geometry("550x350")
        self.resizable(False, False)

        tk.Label(self, text="Seleccione un curso:", font=("Arial", 12)).pack(pady=10)

        self.combo_cursos = ttk.Combobox(self, state="readonly", width=40, font=("Arial", 11))
        self.combo_cursos.pack(pady=5)

        cursos = obtener_cursos()
        self.cursos_dict = {c[1]: c[0] for c in cursos}
        self.combo_cursos['values'] = list(self.cursos_dict.keys())

        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=20)

        tk.Button(frame_btn, text="Generar Excel", command=self.generar_excel,
                  width=15, font=("Arial", 11), bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)

        tk.Button(frame_btn, text="Generar PDF", command=self.generar_pdf,
                  width=15, font=("Arial", 11), bg="#9C27B0", fg="white").grid(row=0, column=1, padx=10)

        tk.Button(frame_btn, text="Abrir Archivo", command=self.abrir_archivo,
                  width=15, font=("Arial", 11), bg="#2196F3", fg="white").grid(row=0, column=2, padx=10)
        
        tk.Button(frame_btn, text="Salir", command=self.salir,
                  width=15, font=("Arial", 11), bg="#2196F3", fg="white").grid(row=2, column=1, padx=10)

        self.ruta_archivo = None

    # ---------------------- Generar EXCEL ----------------------
    def generar_excel(self):
        curso = self.combo_cursos.get().strip()
        if not curso:
            messagebox.showwarning("Advertencia", "Debe seleccionar un curso.")
            return

        datos = estudiantes_activos_por_curso(self.cursos_dict[curso])
        if not datos:
            messagebox.showinfo("Informe", "No hay estudiantes Inactivos en este curso.")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                            filetypes=[("Excel", "*.xlsx")],
                                            title="Guardar Informe Excel")
        if not ruta:
            return

        generar_excel(datos, ruta, curso)
        self.ruta_archivo = ruta
        messagebox.showinfo("Éxito", "Informe Excel generado correctamente.")

    # ---------------------- Generar PDF ----------------------
    def generar_pdf(self):
        curso = self.combo_cursos.get().strip()
        if not curso:
            messagebox.showwarning("Advertencia", "Debe seleccionar un curso.")
            return

        datos = estudiantes_activos_por_curso(self.cursos_dict[curso])
        if not datos:
            messagebox.showinfo("Informe", "No hay estudiantes Inactivos en este curso.")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".pdf",
                                            filetypes=[("PDF", "*.pdf")],
                                            title="Guardar Informe PDF")
        if not ruta:
            return

        generar_pdf(datos, ruta, curso)
        self.ruta_archivo = ruta
        messagebox.showinfo("Éxito", "Informe PDF generado correctamente.")

    # ---------------------- Abrir archivo ----------------------
    def abrir_archivo(self):
        if not self.ruta_archivo or not os.path.exists(self.ruta_archivo):
            messagebox.showwarning("Advertencia", "No hay archivo generado aún.")
            return
        os.startfile(self.ruta_archivo)
    def salir(self):
        self.destroy()

# ---------------------- Ejecutar ----------------------
if __name__ == "__main__":
    app = ReporteEstudiantesActivos()
    app.mainloop()
