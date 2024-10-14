import tkinter as tk
from tkinter import ttk, StringVar, messagebox
from tkinter.ttk import Progressbar

class UIComponents:
    """Clase para crear y manejar componentes de interfaz de usuario en una aplicación Tkinter.

    Esta clase permite la creación de una barra de progreso, un menú de navegación y ventanas para leer,
    procesar y mostrar datos. Además, proporciona la selección de variables para realizar análisis de regresión.

    Attributes:
        root (tk.Tk): La ventana principal de la aplicación.
        data_ops (DataOperations): Objeto que contiene las operaciones de datos necesarias.
        var_x (StringVar): Variable de texto que almacena la selección de la variable independiente.
        var_y (StringVar): Variable de texto que almacena la selección de la variable dependiente.
    """

    def __init__(self, root, data_ops):
        """Inicializa la clase con la ventana principal y operaciones de datos.

        Args:
            root (tk.Tk): La ventana principal de la aplicación.
            data_ops (DataOperations): Objeto que contiene las operaciones de datos necesarias.
        """
        self.root = root
        self.data_ops = data_ops
        self.var_x = StringVar()
        self.var_y = StringVar()

    def create_progress_bar(self):
        """Crea una barra de progreso en la ventana principal.

        Esta barra de progreso se utiliza para indicar el progreso de las operaciones
        que pueden tomar tiempo, como la lectura y procesamiento de datos.
        """
        self.progress = Progressbar(self.root, length=200, mode='indeterminate')
        self.progress.pack(pady=10)

    def create_navbar(self, read_command, process_command, regression_command):
        """Crea una barra de navegación con botones para leer, procesar datos y realizar regresiones.

        Args:
            read_command (callable): Función que se ejecuta al hacer clic en el botón "Leer Datos".
            process_command (callable): Función que se ejecuta al hacer clic en el botón "Procesar Datos".
            regression_command (callable): Función que se ejecuta al hacer clic en el botón "Regresiones".
        """
        navbar = tk.Frame(self.root, bg="#2196F3")
        navbar.pack(fill=tk.X)

        btn_read = tk.Button(navbar, text="Leer Datos", command=read_command, bg="#4CAF50", fg="white", width=15)
        btn_read.pack(side=tk.LEFT, padx=5, pady=5)

        btn_process = tk.Button(navbar, text="Procesar Datos", command=process_command, bg="#FF5722", fg="white", width=15)
        btn_process.pack(side=tk.LEFT, padx=5, pady=5)

        btn_regressions = tk.Button(navbar, text="Regresiones", command=regression_command, bg="#FF9800", fg="white", width=15)
        btn_regressions.pack(side=tk.LEFT, padx=5, pady=5)

        btn_teoria = tk.Button(navbar, text="Teoria",  bg="#9C27B0", fg="white", width=15)
        btn_teoria.pack(side=tk.LEFT, padx=5, pady=5)

        btn_graficadora = tk.Button(navbar, text="Graficadora",  bg="#2196F3", fg="white", width=15)
        btn_graficadora.pack(side=tk.LEFT, padx=5, pady=5)

        btn_materiales = tk.Button(navbar, text="Materiales de laboratorio",  bg="#607D8B", fg="white", width=20)
        btn_materiales.pack(side=tk.LEFT, padx=5, pady=5)

        btn_autores = tk.Button(navbar, text="Autores", command=self.show_autores, width=20,  bg="#FFEB3B", fg="white")
        btn_autores.pack(side=tk.LEFT, padx=5, pady=5)

    def show_read_data_window(self):
        """Muestra la ventana para leer datos desde un archivo.

        La ventana permite al usuario seleccionar un archivo (CSV, TXT, Excel) para cargar los datos.
        """
        window = tk.Toplevel(self.root)
        window.title("Leer Datos")
        window.geometry("500x400")
        window.config(bg="white")

        lbl = tk.Label(window, text="Módulo: Leer Datos", font=("Helvetica", 16), bg="white")
        lbl.pack(pady=20)
        
        btn_read_data = tk.Button(window, text="Seleccionar Archivo (CSV, TXT, Excel)", 
                                  command=lambda: self.data_ops.load_file(self.show_data), 
                                  width=30, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        btn_read_data.pack(pady=10)

    def show_process_data_window(self):
        """Muestra la ventana para procesar datos cargados.

        La ventana ofrece opciones para eliminar valores nulos, eliminar duplicados,
        normalizar datos y rellenar nulos con la media.
        """
        window = tk.Toplevel(self.root)
        window.title("Procesar Datos")
        window.geometry("500x400")
        window.config(bg="white")

        lbl = tk.Label(window, text="Módulo: Procesar Datos", font=("Helvetica", 16), bg="white")
        lbl.pack(pady=20)

        btn_remove_null = tk.Button(window, text="Eliminar Nulos", command=self.data_ops.remove_null_values, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
        btn_remove_null.pack(pady=5)

        btn_remove_duplicates = tk.Button(window, text="Eliminar Duplicados", command=self.data_ops.remove_duplicates, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
        btn_remove_duplicates.pack(pady=5)

        btn_normalize = tk.Button(window, text="Normalizar Datos", command=self.data_ops.normalize_data, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
        btn_normalize.pack(pady=5)

        btn_fill_null = tk.Button(window, text="Rellenar Nulos con Media", command=self.data_ops.fill_null_with_mean, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
        btn_fill_null.pack(pady=5)

        

    def show_regressions_window(self, regression):
        """Muestra la ventana para realizar análisis de regresión.

        En esta ventana, el usuario puede seleccionar las variables independiente y dependiente,
        y realizar regresiones lineales, polinómicas o interpolaciones.

        Args:
            regression (RegressionAnalysis): Objeto para realizar análisis de regresión.
        """
        window = tk.Toplevel(self.root)
        window.title("Regresiones")
        window.geometry("500x400")
        window.config(bg="white")

        lbl = tk.Label(window, text="Módulo: Regresiones", font=("Helvetica", 16), bg="white")
        lbl.pack(pady=20)

        lbl_x = tk.Label(window, text="Selecciona variable independiente (X):", bg="white")
        lbl_x.pack(pady=5)
        options_x = ttk.Combobox(window, textvariable=self.var_x)
        options_x['values'] = list(self.data_ops.data.columns) if self.data_ops.data is not None else []
        options_x.pack(pady=5)

        lbl_y = tk.Label(window, text="Selecciona variable dependiente (Y):", bg="white")
        lbl_y.pack(pady=5)
        options_y = ttk.Combobox(window, textvariable=self.var_y)
        options_y['values'] = list(self.data_ops.data.columns) if self.data_ops.data is not None else []
        options_y.pack(pady=5)

        btn_linear = tk.Button(window, text="Regresión Lineal", command=lambda: regression.linear_regression(self.var_x.get(), self.var_y.get()), width=25, font=("Helvetica", 12), bg="#FF9800", fg="white")
        btn_linear.pack(pady=5)

        btn_polynomial = tk.Button(window, text="Regresión Polinómica", command=lambda: regression.polynomial_regression(self.var_x.get(), self.var_y.get()), width=25, font=("Helvetica", 12), bg="#FF9800", fg="white")
        btn_polynomial.pack(pady=5)

        btn_interpolation = tk.Button(window, text="Interpolación", command=lambda: regression.interpolation(self.var_x.get(), self.var_y.get()), width=25, font=("Helvetica", 12), bg="#FF9800", fg="white")
        btn_interpolation.pack(pady=5)

        



    def show_data(self, data):
        """Muestra los datos cargados en una ventana con una tabla.

        Args:
            data (DataFrame): El DataFrame que contiene los datos cargados.
        """
        window = tk.Toplevel(self.root)
        window.title("Datos Cargados")
        window.geometry("800x400")

        frame_table = ttk.Frame(window)
        frame_table.pack(fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(frame_table, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = ttk.Scrollbar(frame_table, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        columns = list(data.columns)
        table = ttk.Treeview(frame_table, columns=columns, show='headings', 
                             yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.config(command=table.yview)
        scrollbar_x.config(command=table.xview)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100)

        for _, row in data.iterrows():
            table.insert('', tk.END, values=list(row))

        table.pack(fill=tk.BOTH, expand=True)

    def show_autores(self):
        autores = "Andres Gomez\nJulian Aros\nJorge Garzon\nLaura Triana\nSebastian Manrique"
        messagebox.showinfo("Autores", autores)
