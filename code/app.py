import tkinter as tk
from tkinter import ttk, StringVar, messagebox, Text, Scrollbar, Menu
import webbrowser
from data_operations import DataOperations
# from ui_components import UIComponents
# from modules.regression_analysis import RegressionAnalysis

class LaboratorySoftware:
    """Clase principal del Software de Laboratorio."""
    
    def __init__(self) -> None:
        """Inicializa la clase y configura la ventana principal del software.

        Crea instancias de las clases DataOperations, UIComponents y RegressionAnalysis.
        """
        self.root = tk.Tk()
        self.root.title("Software de Laboratorio - Leer y Procesar Datos")
        
        # Ajustar el tamaño de la ventana al 80% de la resolución de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.data_ops = DataOperations()
        # self.ui = UIComponents(self.root, self.data_ops)
        # self.regression = RegressionAnalysis(self.data_ops)

        self.setup_menus()

    def setup_menus(self) -> None:
        """Configura la barra de menús."""
        menubar = Menu(self.root)

        # Menú Archivo
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Importar", command=self.data_ops.load_file)
        file_menu.add_command(label="Exportar", command=self.data_ops.load_file)
        file_menu.add_command(label="Guardar", command=self.data_ops.load_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Edición
        edit_menu = Menu(menubar, tearoff=0)
        process_data_menu = Menu(edit_menu, tearoff=0)
        process_data_menu.add_command(label="Eliminar nulos", command=self.data_ops.remove_null_values)
        process_data_menu.add_command(label="Eliminar duplicados", command=self.data_ops.remove_duplicates)
        process_data_menu.add_command(label="Normalizar datos", command=self.data_ops.normalize_data)
        process_data_menu.add_command(label="Rellenar nulos con media", command=self.data_ops.fill_null_with_mean)
        edit_menu.add_cascade(label="Procesar datos", menu=process_data_menu)

        regressions_menu = Menu(edit_menu, tearoff=0)
        # regressions_menu.add_command(label="Regresión lineal", command=self.ui.linear_regression)
        # regressions_menu.add_command(label="Regresión polinómica", command=self.ui.polynomial_regression)
        # regressions_menu.add_command(label="Interpolación", command=self.ui.interpolation)
        edit_menu.add_cascade(label="Regresiones", menu=regressions_menu)
        menubar.add_cascade(label="Edición", menu=edit_menu)

        # Menú Acerca de
        about_menu = Menu(menubar, tearoff=0)
        # Falta hacer test de esta parte
        about_menu.add_command(label="Documentación", command=lambda: webbrowser.open("https://jsmanriquem.github.io/proyecto_final/"))
        about_menu.add_command(label="Autores", command=self.show_autores)
        menubar.add_cascade(label="Acerca de", menu=about_menu)

        # Añadir la barra de menús a la ventana principal
        self.root.config(menu=menubar)

    def show_autores(self):
        autores = "Andrés Gómez\nJorge Garzón\nJulián Aros\nLaura Oliveros\nLaura Triana\nSebastian Manrique"
        messagebox.showinfo("Autores", autores)

    def run(self) -> None:
        """Ejecuta el bucle principal de la interfaz gráfica."""
        self.root.mainloop()

if __name__ == "__main__":
    app = LaboratorySoftware()
    app.run()
