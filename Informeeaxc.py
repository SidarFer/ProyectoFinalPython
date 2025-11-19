
import mariadb
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from openpyxl import Workbook

# ------------------------------------------
# CONEXIÓN A LA BD
# ------------------------------------------
def conectar_db():
    try:
        return mariadb.connect(
            user="root",
            password="",
            host="localhost",
            database="sistecurcap"
        )
    except mariadb.Error as e:
        messagebox.showerror("Error BD", str(e))
        return None


# ------------------------------------------
# VENTANA INFORME – VERSIÓN PROBADA
# ------------------------------------------
def ventana_informe_activos():
    print(">>> Cargando ventana de informe...")  # DEBUG
    ventana = Toplevel()
    ventana.title("Informe – Estudiantes activos por curso")
    ventana.geometry("500x250")
    ventana.grab_set()   # Garantiza que se vea SIEMPRE
    ventana.focus_force()

    Label(ventana, text="Seleccione un curso:", font=("Arial", 11)).pack(pady=10)

    combo_cursos = ttk.Combobox(ventana, width=45, state="readonly")
    combo_cursos.pack(pady=5)

    # --------------------------------------
    # Cargar cursos
    # --------------------------------------
    conn = conectar_db()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute("SELECT idcurso, nombre FROM cursos")
        datos_cursos = cur.fetchall()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        conn.close()
        return

    conn.close()

    if not datos_cursos:
        messagebox.showinfo("Aviso", "No hay cursos registrados.")
        return

    # Diccionario para relacionar nombre → idcurso
    cursos_dict = {nombre: idcurso for idcurso, nombre in datos_cursos}
    combo_cursos["values"] = list(cursos_dict.keys())

    #Salir
    def salir():
        ventana.destroy()

    # --------------------------------------
    # FUNCIÓN PARA GENERAR EXCEL
    # --------------------------------------
    def generar_excel():
        curso_nombre = combo_cursos.get()

        if curso_nombre == "":
            messagebox.showwarning("Falta seleccionar", "Debes elegir un curso.")
            return

        idcurso = cursos_dict[curso_nombre]

        conn = conectar_db()
        if conn is None:
            return

        cur = conn.cursor()

        consulta = """
            SELECT 
                c.codigo,
                c.nombre,
                e.ncarnet,
                e.nombres,
                e.apellidos,
                e.direccion,
                m.fechamatricula
            FROM matriculas m
            JOIN estudiantes e ON m.idestudiante = e.idestudiante
            JOIN cursos c ON m.idcurso = c.idcurso
            WHERE m.estado = 'Cursando'
              AND m.idcurso = ?
        """

        try:
            cur.execute(consulta, (idcurso,))
            datos = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            conn.close()
            return

        conn.close()

        if not datos:
            messagebox.showinfo("Sin resultados", "No hay estudiantes activos en este curso.")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivo Excel", "*.xlsx")],
            title="Guardar informe"
        )

        if not archivo:
            return

        # Crear Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Estudiantes Activos"

        columnas = [
            "Código Curso",
            "Nombre Curso",
            "Carnet",
            "Nombres",
            "Apellidos",
            "Dirección",
            "Fecha Matrícula"
        ]
        ws.append(columnas)

        for fila in datos:
            ws.append(fila)

        wb.save(archivo)
        messagebox.showinfo("Éxito", "Informe generado correctamente.")

    Button(ventana, text="Generar Informe", bg="#1E90FF", fg="white", width=20, command=generar_excel).pack(pady=5)
    Button(ventana, text="Salir", bg="#1E90FF", fg="white", width=20, command=salir).pack(pady=20)
    
#if __name__ == "__main__":
    #root = Tk()
    #Button(root, text="Abrir informe", command=ventana_informe_activos).pack(pady=30)
    #root.mainloop()    