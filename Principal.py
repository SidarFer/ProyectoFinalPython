
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import CrudCursos
import CrudEstudiantes
import CrudMatriculas
import CrearUsuarios

class VentanaPrincipal(tk.Tk):

    def __init__(self, rol_usuario):
        super().__init__()

        if rol_usuario == "Administrador":
            self.title("Sistema de Registro de Cursos de Capacitación - Administrador")
        else:
            self.title("Sistema de Registro de Cursos de Capacitación - Usuario")

        self.geometry("900x600")

        self.rol = rol_usuario  # "Administrador" o "UsuarioNormal"

        # Crear menú
        self.crear_menu()

        # Crear barra de herramientas
        self.crear_toolbar()

        # Área principal
        self.frame_contenido = ttk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)

    # MENÚ PRINCIPAL
    def crear_menu(self):
        barra_menu = tk.Menu(self)

        # ---------- Menú Ingresar ----------
        menu_ingresar = tk.Menu(barra_menu, tearoff=0)
        menu_ingresar.add_command(label="Cursos", command=self.cursos)
        menu_ingresar.add_command(label="Matrícula", command=self.matricula)
        menu_ingresar.add_command(label="Estudiantes", command=self.estudiantes)
        menu_ingresar.add_command(label="Graduación", command=self.graduacion)
        menu_ingresar.add_command(label="Unidades de Cursos", command=self.unidades_curso)
       
        # Solo administradores pueden gestionar usuarios
        if self.rol == "Administrador":
            menu_ingresar.add_command(label="Usuarios", command=self.usuarios)

        menu_ingresar.add_separator()
        menu_ingresar.add_command(label="Salir", command=self.salir)

        barra_menu.add_cascade(label="Ingresar", menu=menu_ingresar)

        # ---------- Menú Calificaciones ----------
        menu_calificaciones = tk.Menu(barra_menu, tearoff=0)
        menu_calificaciones.add_command(label="Calificaciones por unidad", command=self.calificaciones)
        barra_menu.add_cascade(label="Calificaciones", menu=menu_calificaciones)

        # ---------- Menú Informes ----------
        menu_informes = tk.Menu(barra_menu, tearoff=0)
        menu_informes.add_command(label="Estudiantes activos por curso", command=self.inf_activos)
        menu_informes.add_command(label="Estudiantes inactivos por curso", command=self.inf_inactivos)
        menu_informes.add_command(label="Cursos activos a una fecha", command=self.inf_cursos_activos)
        menu_informes.add_command(label="Cursos finalizados a una fecha", command=self.inf_cursos_finalizados)
        menu_informes.add_command(label="Cursos por tipo", command=self.inf_cursos_tipo)

        barra_menu.add_cascade(label="Informes", menu=menu_informes)

         # ---------- Menú Respaldo BD ----------
        menu_respaldo = tk.Menu(barra_menu, tearoff=0)
        menu_respaldo.add_command(label="Respaldar Base de Datos", command=self.respaldar)
        if self.rol == "Administrador":
            menu_respaldo.add_command(label="Restaurar Base de Datos", command=self.restaurar)
        barra_menu.add_cascade(label="Base de Datos", menu=menu_respaldo)

        # ---------- Menú Ayuda ----------
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "Sistema Académico v1.0"))
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=barra_menu)

    # BARRA DE HERRAMIENTAS
    def crear_toolbar(self):
        toolbar = ttk.Frame(self, padding=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Botones de ejemplo
        btn_estudiantes = ttk.Button(toolbar, text="Estudiantes", command=self.estudiantes)
        btn_estudiantes.pack(side=tk.LEFT, padx=3)

        btn_cursos = ttk.Button(toolbar, text="Cursos", command=self.cursos)
        btn_cursos.pack(side=tk.LEFT, padx=3)

        btn_calif = ttk.Button(toolbar, text="Calificaciones", command=self.calificaciones)
        btn_calif.pack(side=tk.LEFT, padx=3)

        # Solo admin puede ver el botón Usuarios
        if self.rol == "Administrador":
            btn_users = ttk.Button(toolbar, text="Usuarios", command=self.usuarios)
            btn_users.pack(side=tk.LEFT, padx=3)

        btn_calif = ttk.Button(toolbar, text="Salir", command=self.salir)
        btn_calif.pack(side=tk.LEFT, padx=3)

    # MÉTODOS DE ACCIÓN (placeholder)
    def cursos(self):
        CrudCursos.CursosWindow()
        
    def matricula(self):
        CrudMatriculas.MatriculaWindow()
        
    def estudiantes(self):
        CrudEstudiantes.EstudiantesWindow()
        
    def graduacion(self):
        messagebox.showinfo("Graduación", "Ventana de Graduación")

    def unidades_curso(self):
        messagebox.showinfo("Unidades de Curso", "Gestión de Unidades")

    def usuarios(self):
        
        #messagebox.showinfo("Usuarios", "Administración de Usuarios")
        
    #def calificaciones(self):
        messagebox.showinfo("Calificaciones", "Calificaciones por Unidad")
    
    def calificaciones(self):
        messagebox.showinfo("Calificaciones", "Calificaciones por Unidad")

    def inf_activos(self):
        messagebox.showinfo("Informe", "Estudiantes Activos por Curso")

    def inf_inactivos(self):
        messagebox.showinfo("Informe", "Estudiantes Inactivos por Curso")

    def inf_cursos_activos(self):
        messagebox.showinfo("Informe", "Cursos activos a una fecha")

    def inf_cursos_finalizados(self):
        messagebox.showinfo("Informe", "Cursos finalizados a una fecha")

    def inf_cursos_tipo(self):
        messagebox.showinfo("Informe", "Cursos por tipo")
    
    def respaldar(self):
        messagebox.showinfo("Respaldo de BD")
    
    def restaurar(self):
        messagebox.showinfo("Restauración de BD")

    def salir(self):
        exit()


# EJEMPLO DE ARRANQUE
parametro_recibido = sys.argv[1]
if len(sys.argv) > 1:
    parametro_recibido = sys.argv[1]
    print(f"Script destino: Parámetro recibido: {parametro_recibido}")
else:
    print("Script destino: No se recibieron parámetros.")


if __name__ == "__main__":
    # Cambia esto por el rol recibido desde tu sistema de login
    app = VentanaPrincipal(rol_usuario=parametro_recibido)
    app.mainloop()

