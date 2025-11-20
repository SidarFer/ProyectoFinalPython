import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mariadb
from openpyxl import Workbook
import subprocess
import os


# ---------------------- Conexión a MariaDB ----------------------
def obtener_conexion():
    try:
        conn = mariadb.connect(
        user="root",
        password="", # Ajustar según tu caso
        host="localhost",
        database="sistecurcap",
        port=3306
        )
        return conn

    except mariadb.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la Base de Datos: {e}")
        return None


# ---------------------- Consulta a la BD ----------------------
def consultar_cursos_finalizados(fecha_limite):
    conn = obtener_conexion()
    if conn is None:
        return []


    cursor = conn.cursor()
    query = """
        SELECT codigo, nombre, tipo, horas, fechainicio, fechafin
        FROM cursos
        WHERE fechafin <= ?
    """

    try:
        cursor.execute(query, (fecha_limite,))
        datos = cursor.fetchall()
        conn.close()
        return datos
    
    except mariadb.Error as e:
        messagebox.showerror("Error", f"Error al consultar cursos: {e}")
        return []

# ---------------------- Exportar a Excel ----------------------
def generar_excel(datos, ruta_archivo):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cursos Finalizados"

    # Encabezados
    encabezados = ["Código", "Nombre", "Tipo", "Horas", "Fecha Inicio", "Fecha Fin"]
    ws.append(encabezados)

    # Contenido
    for fila in datos:
        ws.append(fila)

    # Guardar archivo
    wb.save(ruta_archivo)

# ---------------------- Interfaz Tkinter ----------------------
class ReporteCursosFinalizados(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Informe de Cursos Finalizados")
        self.geometry("500x300")
        self.resizable(False, False)

        # Fecha límite
        tk.Label(self, text="Fecha límite (AAAA-MM-DD):", font=("Arial", 12)).pack(pady=10)
        self.fecha_entry = tk.Entry(self, width=20, font=("Arial", 12))
        self.fecha_entry.pack()

        # Botones
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

# Generar Informe
    def generar_informe(self):
        fecha = self.fecha_entry.get().strip()
        if not fecha:
            messagebox.showwarning("Advertencia", "Debe ingresar una fecha.")
            return

        datos = consultar_cursos_finalizados(fecha)
        if not datos:
            messagebox.showinfo("Informe", "No hay cursos finalizados antes de esa fecha.")
            return

        # Seleccionar ruta para guardar
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
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.focus()

    #--------------------------------------
    def abrir_excel(self):
        if not self.ruta_archivo or not os.path.exists(self.ruta_archivo):
            messagebox.showwarning("Advertencia", "Primero debe generar el informe.")
            return

        try:
            os.startfile(self.ruta_archivo)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

# ---------------------- Ejecutar ----------------------
if __name__ == "__main__":
    app = ReporteCursosFinalizados()
    app.mainloop()