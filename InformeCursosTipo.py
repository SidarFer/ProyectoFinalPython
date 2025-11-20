
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mariadb
from openpyxl import Workbook
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
    
    # ---------------------- Consulta BD ----------------------
def obtener_tipos_cursos():
    conn = obtener_conexion()
    if conn is None:
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT tipo FROM cursos ORDER BY tipo")
        tipos = [fila[0] for fila in cur.fetchall()]
        conn.close()
        return tipos
    except mariadb.Error as e:
        messagebox.showerror("Error", f"Error al obtener tipos: {e}")
        return []

def consultar_cursos_por_tipo(tipo):
    conn = obtener_conexion()
    if conn is None:
        return []
    cur = conn.cursor()
    query = """
        SELECT codigo, nombre, tipo, horas, fechainicio, fechafin
        FROM cursos
        WHERE tipo = ?
    """
    try:
        cur.execute(query, (tipo,))
        datos = cur.fetchall()
        conn.close()
        return datos
    except mariadb.Error as e:
        messagebox.showerror("Error", f"Error al consultar cursos: {e}")
        return []

# ---------------------- Exportar a Excel ----------------------
def generar_excel(datos, ruta_archivo):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cursos por Tipo"
    encabezados = ["Código", "Nombre", "Tipo", "Horas", "Fecha Inicio", "Fecha Fin"]
    ws.append(encabezados)
    for fila in datos:
        ws.append(fila)
    wb.save(ruta_archivo)

# ---------------------- Interfaz Tkinter ----------------------
class ReporteCursosPorTipo(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Informe de Cursos por Tipo")
        self.geometry("500x300")
        self.resizable(False, False)

        tk.Label(self, text="Seleccione un tipo de curso:", font=("Arial", 12)).pack(pady=10)

        self.combo_tipo = ttk.Combobox(self, state="readonly", width=30, font=("Arial", 11))
        self.combo_tipo.pack(pady=5)

        # Llenar tipos desde BD
        self.combo_tipo['values'] = obtener_tipos_cursos()

        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=20)

        tk.Button(frame_btn, text="Generar Informe", command=self.generar_informe,
        width=18, font=("Arial", 11), bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)

        tk.Button(frame_btn, text="Abrir Excel", command=self.abrir_excel,
        width=18, font=("Arial", 11), bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)

        tk.Button(frame_btn, text="Salir", command=self.salir,
        width=18, font=("Arial", 12), bg="#CE3737", fg="white").grid(row=1, column=0, padx=10)

        tk.Button(frame_btn, text="Limpiar", command=self.limpiar,
        width=18, font=("Arial", 12), bg="#FCF8F8", fg="blue").grid(row=1, column=1, padx=10)


        self.ruta_archivo = None

    # ---------------------- Generar informe ----------------------
    def generar_informe(self):
        tipo = self.combo_tipo.get().strip()
        if not tipo:
            messagebox.showwarning("Advertencia", "Debe seleccionar un tipo de curso.")
            return

        datos = consultar_cursos_por_tipo(tipo)
        if not datos:
            messagebox.showinfo("Informe", "No hay cursos registrados con ese tipo.")
            return

        ruta = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Archivos Excel", "*.xlsx")],
        title="Guardar Informe"
        )

        if not ruta:
            return

        generar_excel(datos, ruta)
        self.ruta_archivo = ruta
        messagebox.showinfo("Éxito", "Informe generado correctamente.")
    
    #Salir
    def salir(self):
        self.destroy()
    
    #limpiar
    def limpiar(self):
        self.combo_tipo.set("")
        self.combo_tipo.focus()

    # ---------------------- Abrir Excel ----------------------
    def abrir_excel(self):
        if not self.ruta_archivo or not os.path.exists(self.ruta_archivo):
            messagebox.showwarning("Advertencia", "Primero debe generar el informe.")
            return
        try:
            os.startfile(self.ruta_archivo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

if __name__ == "__main__":
    app = ReporteCursosPorTipo()
    app.mainloop()