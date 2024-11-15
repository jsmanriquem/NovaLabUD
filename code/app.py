import tkinter as tk
from tkinter import ttk, StringVar, messagebox, Text, Scrollbar, Menu, simpledialog, messagebox
import webbrowser
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image, ImageTk  # Para manejar imágenes en Tkinter
import io
from data_operations import DataOperations
from regression_analysis import RegressionAnalysis

class LaboratorySoftware:
    """
    Clase principal del Software de Laboratorio para análisis y procesamiento de datos.
    Esta clase implementa la interfaz gráfica principal y coordina todas las funcionalidades
    del software, incluyendo la carga de datos, visualización, procesamiento y análisis.
    
    Attributes:
        root (tk.Tk): Ventana principal de la aplicación.
        main_frame (ttk.PanedWindow): Panel principal dividido que contiene la tabla de datos y resultados.
        data_frame (ttk.LabelFrame): Marco para la tabla de datos.
        results_frame (ttk.LabelFrame): Marco para mostrar resultados y gráficas.
        data_table (ttk.Treeview): Tabla para visualizar los datos cargados.
        data_ops (DataOperationsWithUI): Instancia para operaciones de datos con UI.
        no_data_label (ttk.Label): Etiqueta mostrada cuando no hay datos cargados.
    Clase principal del Software de Laboratorio.
    """
    
    def __init__(self) -> None:
        """
        Inicializa la aplicación del Software de Laboratorio.
        Configura la ventana principal, establece las dimensiones basadas en la pantalla,
        inicializa los componentes de la UI y configura los menús.
        Inicializa la clase y configura la ventana principal del software.
        """
        self.root = tk.Tk()
        self.root.title("Software de Laboratorio")
        
        # Configuración de la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Cambiar el frame principal a disposición horizontal
        self.main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Panel izquierdo para la tabla de datos
        self.data_frame = ttk.LabelFrame(self.main_frame, text="Datos Cargados", padding="5 5 5 5")
        self.main_frame.add(self.data_frame, weight=1)

        # Crear el Treeview con scrollbars en el panel de datos
        self.create_data_table()

        # Panel derecho para la Teoría
        self.frame_teoria = ttk.LabelFrame(self.main_frame, text="Teoría", padding="5 5 5 5")
        self.main_frame.add(self.frame_teoria, weight=1)  # Asignamos más espacio a la teoría

        # Crear el Notebook
        self.notebook = ttk.Notebook(self.frame_teoria)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Crear las pestañas
        self.tab_cai_libre = ttk.Frame(self.notebook)
        self.tab_ley_hooke = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_cai_libre, text="Caída libre")
        self.notebook.add(self.tab_ley_hooke, text="Ley de Hooke")

        # Cargar PDF solo cuando se seleccione la pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Cargar el PDF de Caída Libre por defecto (si la primera pestaña es la activa)
        self.load_pdf(self.tab_cai_libre, "caida_libre.pdf")

        # Inicializar módulos
        self.data_ops = DataOperationsWithUI(self)
        self.regression_analysis = RegressionAnalysis(self.data_ops)  # Instancia de la clase RegressionAnalysis
        
        # Configurar menús
        self.setup_menus()

        # Label para mostrar cuando no hay datos
        self.no_data_label = ttk.Label(self.data_frame, 
                                    text="No hay datos cargados. Use el menú Archivo -> Importar para cargar datos.", 
                                    font=('Helvetica', 10))
        self.no_data_label.pack(pady=20)

    def load_pdf(self, tab, pdf_path):
        """Carga el PDF en el tab especificado."""
        # Limpiar el contenido del tab antes de cargar el nuevo PDF
        for widget in tab.winfo_children():
            widget.destroy()

        # Cargar el documento PDF
        pdf_document = fitz.open(pdf_path)
        first_page = pdf_document.load_page(0)
        width = first_page.rect.width  # Obtener el ancho del PDF
        height = first_page.rect.height

        # Crear un Frame dentro del tab para mostrar el PDF
        frame = ttk.Frame(tab)
        frame.pack(fill=tk.BOTH, expand=True)

        # Forzar la actualización de tareas pendientes para obtener el ancho correcto del frame
        self.root.update_idletasks()

        # Obtener el ancho del frame después de su renderizado
        frame_width = frame.winfo_width()

        # Calcular el factor de escala basado en el ancho del frame
        scale_factor = frame_width / width
        adjusted_width = int(width * scale_factor)
        adjusted_height = int(height * scale_factor)

        # Crear un Canvas para mostrar el PDF
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Cargar cada página del PDF como imagen y agregarla al Canvas
        for i in range(len(pdf_document)):
            page = pdf_document.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(scale_factor, scale_factor))  # Aplicar la escala
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(scrollable_frame, image=img_tk, bg="white")
            label.image = img_tk
            label.pack(fill=tk.BOTH)

    def on_tab_change(self, event):
        """Cuando se cambia de pestaña, se carga el PDF correspondiente"""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if selected_tab == "Caída libre":
            self.load_pdf(self.tab_cai_libre, "caida_libre.pdf")
        elif selected_tab == "Ley de Hooke":
            self.load_pdf(self.tab_ley_hooke, "ley_de_hooke.pdf")

    def create_data_table(self):
        """
        Inicializa un Treeview con scrollbars vertical y horizontal para mostrar
        los datos cargados de manera organizada y navegable.
        Crea la tabla para mostrar los datos con scrollbars.
        """
        # Frame para contener la tabla y scrollbars
        self.table_frame = ttk.Frame(self.data_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Crear scrollbars
        self.scrollbar_y = ttk.Scrollbar(self.table_frame)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Crear Treeview
        self.data_table = ttk.Treeview(self.table_frame, 
                                     yscrollcommand=self.scrollbar_y.set,
                                     xscrollcommand=self.scrollbar_x.set)
        self.data_table.pack(fill=tk.BOTH, expand=True)

        # Configurar scrollbars
        self.scrollbar_y.config(command=self.data_table.yview)
        self.scrollbar_x.config(command=self.data_table.xview)

        # Estilo para la tabla
        style = ttk.Style()
        style.configure("Treeview", rowheight=20)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

    def update_data_display(self, data: pd.DataFrame):
        """
        Actualiza la tabla de datos con nueva información.
        
        Args:
            data (pd.DataFrame): DataFrame con los nuevos datos a mostrar.
                               Si es None o está vacío, se muestra el mensaje de no datos.
        """
        # Limpiar tabla existente
        self.data_table.delete(*self.data_table.get_children())
        
        if data is not None and not data.empty:
            # Ocultar el label de no datos
            self.no_data_label.pack_forget()
            
            # Configurar columnas
            columns = list(data.columns)
            self.data_table['columns'] = columns
            
            # Formatear columnas
            self.data_table['show'] = 'headings'
            for col in columns:
                self.data_table.heading(col, text=col)
                self.data_table.column(col, width=100)  # Ancho inicial
            
            # Insertar datos
            for idx, row in data.iterrows():
                values = [str(value) for value in row]
                self.data_table.insert('', tk.END, values=values)
        else:
            # Mostrar el label de no datos
            self.no_data_label.pack(pady=20)

    def setup_menus(self) -> None:
        """
        Configura la barra de menús de la aplicación.
        
        Crea y configura los menús principales:
        - Archivo: Para operaciones de importación/exportación
        - Edición: Para procesamiento de datos
        - Acerca de: Para información y documentación
        """
        menubar = Menu(self.root)

        # Menú Archivo
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Importar", 
                              command=lambda: self.data_ops.load_file(self.update_data_display))
        file_menu.add_command(label="Exportar", command=self.data_ops.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Edición
        edit_menu = Menu(menubar, tearoff=0)
        process_data_menu = Menu(edit_menu, tearoff=0)
        process_data_menu.add_command(label="Eliminar nulos", 
                                    command=lambda: self.data_ops.remove_null_values(self.update_data_display))
        process_data_menu.add_command(label="Eliminar duplicados", 
                                    command=lambda: self.data_ops.remove_duplicates(self.update_data_display))
        process_data_menu.add_command(label="Normalizar datos", 
                                    command=lambda: self.data_ops.normalize_data(self.update_data_display))
        process_data_menu.add_command(label="Rellenar nulos con media", 
                                    command=lambda: self.data_ops.fill_null_with_mean(self.update_data_display))
        edit_menu.add_cascade(label="Procesar datos", menu=process_data_menu)
        regression_menu = Menu(edit_menu, tearoff=0)
        regression_menu.add_command(label="Regresión lineal", 
                                    command=lambda: self.run_regression('linear'))
        regression_menu.add_command(label="Regresión polinómica", 
                                    command=lambda: self.run_regression('polynomial'))
        regression_menu.add_command(label="Interpolación", 
                                    command=lambda: self.run_regression('interpolation'))
        edit_menu.add_cascade(label="Regresiones", menu=regression_menu)
        menubar.add_cascade(label="Edición", menu=edit_menu)

        # Menú Acerca de
        about_menu = Menu(menubar, tearoff=0)
        about_menu.add_command(label="Documentación", 
                             command=lambda: webbrowser.open("https://jsmanriquem.github.io/proyecto_final/"))
        about_menu.add_command(label="Autores", command=self.show_autores)
        menubar.add_cascade(label="Acerca de", menu=about_menu)

        self.root.config(menu=menubar)

    def show_autores(self):
        """Muestra los autores del software."""
        autores = "Andrés Gómez\nJorge Garzón\nJulián Aros\nLaura Oliveros\nLaura Triana\nSebastian Manrique"
        messagebox.showinfo("Autores", autores)

    def show_warning(self, message):
        """Muestra una advertencia usando Tkinter."""
        messagebox.showwarning("Advertencia", message)

    def run_regression(self, regression_type: str):
        """Ejecuta la regresión seleccionada con los datos cargados."""
        if self.data_ops.data is None:
            self.show_warning("No hay datos cargados. Primero importa los datos.")
            return

        # Obtener las variables a través de un cuadro de diálogo o un sistema de selección
        var_x, var_y = self.select_variables()  # Aquí seleccionamos las variables

        if regression_type == 'linear':
            self.regression_analysis.linear_regression(var_x, var_y)
        elif regression_type == 'polynomial':
            self.regression_analysis.polynomial_regression(var_x, var_y)
        elif regression_type == 'interpolation':
            self.regression_analysis.interpolation(var_x, var_y)
        else:
            self.show_warning("Tipo de regresión no válido")

    def select_variables(self):
        """Permite al usuario seleccionar las variables para la regresión."""
        # Aquí puedes cambiar esto según cómo quieras que se seleccionen las variables.
        # Por ejemplo, podrías usar un cuadro de diálogo para pedir el nombre de las variables.

        var_x = simpledialog.askstring("Selecciona la variable independiente",
                                       "Ingresa el nombre de la variable independiente:")
        var_y = simpledialog.askstring("Selecciona la variable dependiente",
                                       "Ingresa el nombre de la variable dependiente:")
        return var_x, var_y

    def run(self) -> None:
        """
        Inicia el bucle principal de la aplicación.
        
        Este método debe ser llamado después de la inicialización para comenzar
        la ejecución de la interfaz gráfica.
        """
        self.root.mainloop()

class DataOperationsWithUI(DataOperations):
    """
    Extensión de DataOperations que integra callbacks para la interfaz de usuario.
    
    Esta clase extiende las operaciones de datos básicas para actualizar
    automáticamente la interfaz de usuario cuando se realizan operaciones.
    
    Attributes:
        ui_container: Referencia al contenedor de UI principal.
        
    Inherits:
        DataOperations: Clase base con operaciones de datos fundamentales.
    """
    
    def __init__(self, ui_container):
        """
        Inicializa la clase con una referencia al contenedor de UI.
        
        Args:
            ui_container: Referencia al objeto que contiene los elementos de la UI.
        """
        super().__init__()
        self.ui_container = ui_container

    def load_file(self, ui_callback=None):
        """
        Carga un archivo y actualiza la UI si es exitoso.
        
        Args:
            ui_callback (callable, optional): Función a llamar para actualizar la UI con los datos cargados.
        
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario
        """
        success = super().load_file()
        if success and ui_callback:
            ui_callback(self.data)
        return success

    def remove_null_values(self, ui_callback=None):
        """
        Elimina los valores nulos del conjunto de datos y actualiza la UI si se proporciona un callback.

        Args:
        ui_callback (callable, optional): Función que se llama para actualizar la UI con los datos modificados, si se proporciona.
        """
        super().remove_null_values()
        if ui_callback:
            ui_callback(self.data)

    def remove_duplicates(self, ui_callback=None):
        """
        Elimina las filas duplicadas del conjunto de datos y actualiza la UI si se proporciona un callback.

        Args:
        ui_callback (callable, optional): Función que se llama para actualizar la UI con los datos modificados, si se proporciona.
        """
        super().remove_duplicates()
        if ui_callback:
            ui_callback(self.data)

    def normalize_data(self, ui_callback=None):
        """
        Normaliza las columnas numéricas del conjunto de datos y actualiza la UI si se proporciona un callback.

        Args:
        ui_callback (callable, optional): Función que se llama para actualizar la UI con los datos modificados, si se proporciona.
        """
        super().normalize_data()
        if ui_callback:
            ui_callback(self.data)

    def fill_null_with_mean(self, ui_callback=None):
        """
        Rellena los valores nulos en columnas numéricas con la media de cada columna y actualiza la UI si se proporciona un callback.

        Args:
        ui_callback (callable, optional): Función que se llama para actualizar la UI con los datos modificados, si se proporciona.
        """
        super().fill_null_with_mean()
        if ui_callback:
            ui_callback(self.data)

if __name__ == "__main__":
    app = LaboratorySoftware()
    app.run()