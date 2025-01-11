import tkinter as tk
from tkinter import ttk, StringVar, messagebox, Text, Scrollbar, Menu, simpledialog, Toplevel
import webbrowser
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image, ImageTk  # Para manejar imágenes en Tkinter
import io, sys, subprocess
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
    """
    
    def __init__(self) -> None:
        """
        Inicializa la aplicación del Software de Laboratorio.
    
        Este método configura la ventana principal de la aplicación, establece las dimensiones
        basadas en el tamaño de la pantalla, inicializa los componentes de la interfaz gráfica
        (como los paneles y menús), y configura las pestañas para mostrar los contenidos de los experimentos.

        - Configura la ventana con un tamaño proporcional a la pantalla del usuario.
        - Establece un diseño de ventana con un panel horizontal que contiene dos áreas: 
            1. Un panel para mostrar los datos cargados.
            2. Un panel para mostrar la teoría con pestañas.
        - Inicializa y organiza los componentes para cargar y mostrar datos en la tabla, así como para mostrar la teoría.
        - Configura los menús y las interacciones de la interfaz gráfica.
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
        self.main_frame.add(self.data_frame, weight=3)  # Mayor peso para el panel izquierdo

        # Crear el Treeview con scrollbars en el panel de datos
        self.create_data_table()

        # Panel derecho para la Teoría
        fixed_width = 700  # Ancho fijo deseado
        self.frame_teoria = ttk.LabelFrame(self.main_frame, text="Teoría", padding="5 5 5 5")
        self.frame_teoria.pack_propagate(False)  # Evitar propagación del tamaño
        self.frame_teoria.configure(width=fixed_width)  # Establecer ancho fijo

        # Agregar al PanedWindow con peso menor
        self.main_frame.add(self.frame_teoria, weight=0)  # Peso 0 para mantener tamaño fijo

        # Configurar posición inicial del sash
        def configure_sash(event=None):
            total_width = self.main_frame.winfo_width()
            sash_position = total_width - fixed_width
            if sash_position > 0:
                self.main_frame.sashpos(0, sash_position)  # Usar sashpos para establecer la posición
            return "break"

        self.main_frame.bind("<Configure>", configure_sash)
        self.main_frame.bind("<B1-Motion>", lambda e: "break")  # Prevenir movimiento del sash

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
        self.regression = RegressionAnalysis(self.data_ops)
        
        # Configurar menús
        self.setup_menus()

        # Label para mostrar cuando no hay datos
        self.no_data_label = ttk.Label(self.data_frame, 
                                    text="No hay datos cargados. Use el menú Archivo -> Importar para cargar datos.", 
                                    font=('Helvetica', 10))
        self.no_data_label.pack(pady=20)

    def load_pdf(self, tab, pdf_path):
        """
        Carga un archivo PDF y lo muestra en un tab especificado en la interfaz gráfica.

        Args:
            tab (tk.Widget): El contenedor donde se mostrará el contenido del PDF.
            pdf_path (str): La ruta al archivo PDF que se desea cargar.

        Detalles:
            - Limpia el contenido existente del `tab` antes de cargar el nuevo PDF.
            - Calcula la escala del PDF basada en el ancho disponible del frame dentro del `tab`.
            - Renderiza cada página del PDF como una imagen y la agrega a un Canvas con barra de desplazamiento.

        Ejemplo:
            ```python
            # Supongamos que `tab` es un ttk.Frame y `pdf_path` es una ruta válida.
            my_app.load_pdf(tab, "documento.pdf")
            ```

        Notas:
            - Se utiliza el módulo `fitz` de PyMuPDF para cargar y procesar el PDF.
            - La visualización del PDF es responsiva y se adapta al ancho disponible del contenedor.
            - Cada página se renderiza como una imagen y se agrega a un Canvas dentro de un Frame desplazable.

        Requiere:
            - PyMuPDF (fitz)
            - PIL (Pillow)
        """
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
        """
        Maneja el evento de cambio de pestaña en el notebook y carga el PDF correspondiente.

        Args:
            event (tk.Event): El evento generado al cambiar de pestaña.

        Detalles:
            - Identifica la pestaña seleccionada por su etiqueta de texto.
            - Llama al método `load_pdf` para cargar el archivo PDF asociado a la pestaña seleccionada.

        Pestañas y PDFs asociados:
            - "Caída libre": Carga el archivo `caida_libre.pdf`.
            - "Ley de Hooke": Carga el archivo `ley_de_hooke.pdf`.

        Ejemplo:
            ```python
            notebook.bind("<<NotebookTabChanged>>", app.on_tab_change)
            ```

        Notas:
            - Se asume que `self.notebook` es un widget `ttk.Notebook` y que 
            las pestañas están configuradas correctamente con los nombres indicados.
            - Los archivos PDF deben estar disponibles en las rutas especificadas.

        Requiere:
            - El método `load_pdf` debe estar definido en la misma clase.
        """
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if selected_tab == "Caída libre":
            self.load_pdf(self.tab_cai_libre, "caida_libre.pdf")
        elif selected_tab == "Ley de Hooke":
            self.load_pdf(self.tab_ley_hooke, "ley_de_hooke.pdf")

    def create_data_table(self):
        """
        Crea y configura una tabla (`Treeview`) para mostrar datos con scrollbars vertical y horizontal.

        Este método inicializa un `Treeview` dentro de un contenedor (`Frame`), agrega barras de desplazamiento
        para navegación vertical y horizontal, y aplica estilos básicos a la tabla para mejorar su apariencia.

        Detalles:
            - La tabla se coloca dentro de un `Frame` en `self.data_frame`.
            - Las barras de desplazamiento se asocian con el desplazamiento horizontal y vertical del `Treeview`.
            - Se aplica un estilo personalizado para ajustar la altura de las filas y el formato de los encabezados.

        Notas:
            - Este método no incluye la carga de datos en la tabla, solo configura su estructura.
            - El `Treeview` se ajusta automáticamente al tamaño del contenedor.

        Requiere:
            - `self.data_frame`: Un contenedor existente en la interfaz donde se colocará la tabla.

        Ejemplo:
            ```python
            app.create_data_table()
            # Cargar datos en la tabla después de su creación:
            for row in data:
                app.data_table.insert('', 'end', values=row)
            ```
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
         Actualiza la tabla (`Treeview`) con nuevos datos proporcionados en un DataFrame.

        Args:
            data (pd.DataFrame): Un DataFrame con los datos a mostrar. 
                - Si el DataFrame es `None` o está vacío, se muestra un mensaje indicando la ausencia de datos.

        Detalles:
            - Limpia el contenido actual de la tabla antes de insertar nuevos datos.
            - Configura dinámicamente las columnas de la tabla basándose en los nombres de las columnas del DataFrame.
            - Inserta las filas del DataFrame en la tabla, formateando los valores como cadenas.

        Notas:
            - Si no hay datos disponibles, se muestra un label (`self.no_data_label`) indicando "No hay datos disponibles".
            - El ancho inicial de las columnas se establece en 100 unidades, pero puede ser ajustado por el usuario.

        Ejemplo:
            ```python
            # Actualizar la tabla con un nuevo DataFrame
            df = pd.DataFrame({'Columna1': [1, 2, 3], 'Columna2': ['A', 'B', 'C']})
            app.update_data_display(df)
            ```

        Requiere:
            - `self.data_table`: Un widget `Treeview` previamente inicializado para mostrar datos.
            - `self.no_data_label`: Un label para mostrar el mensaje de ausencia de datos.
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

    def setup_menus(self):
        menubar = tk.Menu(self.root)

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
        menubar.add_cascade(label="Edición", menu=edit_menu)
        

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

        # Submenú de regresiones dentro de Edición
        regression_submenu = Menu(edit_menu, tearoff=0)
        edit_menu.add_cascade(label="Regresiones", menu=regression_submenu)
        
        regression_submenu.add_command(label="Regresión Lineal", 
                                     command=self.linear_regression)
        regression_submenu.add_command(label="Regresión Polinómica", 
                                     command=self.polynomial_regression)
        regression_submenu.add_command(label="Interpolación de Lagrange", 
                                     command=self.interpolation)
        regression_submenu.add_command(label="Análisis de Errores", 
                                     command=self.error_analysis)
        # Menú Ver
        menubar.add_command(label="Ver", command=self.open_graficador)

        # Menú Acerca de
        about_menu = Menu(menubar, tearoff=0)
        about_menu.add_command(label="Documentación", 
                             command=lambda: webbrowser.open("https://jsmanriquem.github.io/NovaLabUD/"))
        about_menu.add_command(label="Autores", command=self.show_autores)
        menubar.add_cascade(label="Acerca de", menu=about_menu)

        self.root.config(menu=menubar)

    def show_autores(self):
        """Muestra los autores del software."""
        autores = "Andrés Gómez\nJorge Garzón\nJulián Aros\nLaura Oliveros\nLaura Triana\nSebastian Manrique"
        messagebox.showinfo("Autores", autores)

    def open_graficador(self):
        """Método para ejecutar graficador.py en una nueva ventana."""
        try:
            # Ejecutar el archivo graficador.py como un proceso independiente
            subprocess.Popen([sys.executable, 'graficador.py'])
        except Exception as e:
            print(f"Error al ejecutar graficador.py: {e}")

    def run(self) -> None:
        """
        Inicia el bucle principal de la aplicación gráfica.

        Este método lanza el bucle de eventos de Tkinter, manteniendo activa la ventana
        de la aplicación hasta que el usuario la cierre manualmente. 

        Detalles:
            - Debe ser llamado después de haber configurado todos los elementos 
            de la interfaz y la lógica de la aplicación.
            - Es el punto de entrada principal para iniciar la ejecución de la interfaz gráfica.

        Ejemplo:
            ```python
            app = MyApp()
            app.setup_menus()
            app.run()
            ```
        """
        self.root.mainloop()

    def perform_linear_regression(self):
        if self.data_ops.data is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return
        self.regression.linear_regression()

    def perform_polynomial_regression(self):
        if self.data_ops.data is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return
        self.regression.polynomial_regression()

    def perform_lagrange_interpolation(self):
        if self.data_ops.data is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return
        self.regression.interpolation()

    def linear_regression(self):
        if not self.check_data():
            return
            
        # Obtener columnas disponibles
        columns = list(self.data_ops.data.columns)
        
        # Diálogo para seleccionar variables
        dialog = VariableSelectionDialog(self.root, columns)
        if dialog.result:
            var_x, var_y = dialog.result
            try:
                self.regression.linear_regression(var_x, var_y)
            except Exception as e:
                messagebox.showerror("Error", f"Error en la regresión: {str(e)}")

    def polynomial_regression(self):
        if self.check_data():
            degree = simpledialog.askinteger("Grado", 
                                           "Ingrese el grado del polinomio:", 
                                           minvalue=1, maxvalue=10)
            if degree:
                self.regression.polynomial_regression(degree=degree)

    def interpolation(self):
        if self.check_data():
            self.regression.interpolation()

    def error_analysis(self):
        if self.check_data():
            self.regression.calculate_error_metrics()

    def export_regression_results(self):
        if self.check_data():
            self.regression.export_results()

    def check_data(self):
        if self.data_ops.data is None:
            messagebox.showwarning("Advertencia", 
                                 "No hay datos cargados para realizar el análisis")
            return False
        return True

class VariableSelectionDialog:
    def __init__(self, parent, columns):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Selección de Variables")
        self.result = None
        
        ttk.Label(self.dialog, text="Variable X:").grid(row=0, column=0, padx=5, pady=5)
        self.var_x = ttk.Combobox(self.dialog, values=columns)
        self.var_x.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Variable Y:").grid(row=1, column=0, padx=5, pady=5)
        self.var_y = ttk.Combobox(self.dialog, values=columns)
        self.var_y.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.dialog, text="Aceptar", 
                  command=self.on_accept).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.dialog.wait_window()
    
    def on_accept(self):
        if self.var_x.get() and self.var_y.get():
            self.result = (self.var_x.get(), self.var_y.get())
            self.dialog.destroy()

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

    def select_columns(self):
        """
        Muestra una ventana emergente con checkboxes para que el usuario seleccione columnas.

        Returns:
            list: Una lista de las columnas seleccionadas por el usuario. Si no se seleccionan columnas 
            o no hay datos cargados, retorna None.
        """
        if self.data is None:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos.")
            return None

        columns = list(self.data.columns)
        if not columns:
            messagebox.showwarning("Advertencia", "No hay columnas disponibles.")
            return None

        selected_columns = []

        popup = Toplevel()
        popup.title("Seleccionar columnas")
        popup.geometry("300x400")

        label = ttk.Label(popup, text="Seleccione las columnas:", font=("Helvetica", 12))
        label.pack(pady=10)

        # Crear checkboxes para cada columna
        column_vars = {}  # Diccionario para almacenar el estado de cada checkbox
        for col in columns:
            var = StringVar(value="")
            checkbox = ttk.Checkbutton(
                popup, 
                text=col, 
                variable=var, 
                onvalue=col, 
                offvalue=""
            )
            checkbox.pack(anchor="w", padx=20, pady=5)
            column_vars[col] = var

        def confirm_selection():
            # Guardar las columnas seleccionadas
            for col, var in column_vars.items():
                if var.get():
                    selected_columns.append(var.get())
            popup.destroy()

        btn_confirm = ttk.Button(popup, text="Confirmar", command=confirm_selection)
        btn_confirm.pack(pady=20)

        popup.wait_window()  # Espera hasta que el usuario cierre la ventana
        return selected_columns


    def normalize_data(self, ui_callback=None):
        """
        Normaliza las columnas seleccionadas según el método elegido por el usuario.

        Este método permite al usuario seleccionar las columnas que desea normalizar y luego elegir uno de los 
        tres métodos de normalización disponibles: Min-Max Scaling, Z-Score Scaling o Max Abs Scaling. Los valores 
        de las columnas seleccionadas serán transformados según el método seleccionado.

        Args:
            ui_callback (function, optional): Función de devolución de llamada que se ejecuta después de 
            completar la operación. Recibe los datos actualizados como argumento. Por defecto es None.

        Returns:
            None: Este método no retorna ningún valor, pero modifica los datos de la clase y muestra un mensaje de éxito.
        """
        # Seleccionar columnas
        selected_columns = self.select_columns()
        if not selected_columns:
            return

        methods = ["Min-Max Scaling", "Z-Score Scaling", "Max Abs Scaling"]
        selected_method = self.select_option("Método de Normalización", methods)

        if not selected_method:
            return

        # Copia de los datos originales para comparar al final
        original_data = self.data[selected_columns].copy()

        # Aplicar normalización según el método seleccionado
        for col in selected_columns:
            if self.data[col].notnull().any():  # Solo aplica si la columna no está completamente vacía
                if selected_method == "Min-Max Scaling":
                    min_val = self.data[col].min()
                    max_val = self.data[col].max()
                    if max_val != min_val:
                        self.data[col] = (self.data[col] - min_val) / (max_val - min_val)
                    else:
                        self.data[col] = 0  # Caso especial: todos los valores son iguales

                elif selected_method == "Z-Score Scaling":
                    mean_val = self.data[col].mean()
                    std_val = self.data[col].std()
                    if std_val != 0:
                        self.data[col] = (self.data[col] - mean_val) / std_val
                    else:
                        self.data[col] = 0  # Caso especial: desviación estándar es 0

                elif selected_method == "Max Abs Scaling":
                    max_abs_val = self.data[col].abs().max()
                    if max_abs_val != 0:
                        self.data[col] = self.data[col] / max_abs_val
                    else:
                        self.data[col] = 0  # Caso especial: todos los valores son 0

        # Comparar filas afectadas
        affected_rows = (self.data[selected_columns] != original_data).any(axis=1).sum()

        # Registrar y mostrar el mensaje
        self._add_to_history('normalize_data', f'Normalizadas las columnas {", ".join(selected_columns)} usando {selected_method}')
        messagebox.showinfo("Éxito", f"Datos normalizados. Se afectaron {affected_rows} filas.")
        if ui_callback:
            ui_callback(self.data)


    def fill_null_with_mean(self, ui_callback=None):
        """
        Rellena los valores nulos de las columnas seleccionadas con la media de cada columna.

        Este método permite al usuario seleccionar las columnas en las que desea reemplazar los valores nulos 
        por la media de cada columna. Si se seleccionan columnas y hay valores nulos, estos serán rellenados 
        automáticamente con la media correspondiente.

        Args:
            ui_callback (function, optional): Función de devolución de llamada que se ejecuta después de 
            completar la operación. Recibe los datos actualizados como argumento. Por defecto es None.

        Returns:
            None: Este método no retorna ningún valor, pero modifica los datos de la clase y muestra un mensaje de éxito.
        """
        selected_columns = self.select_columns()
        if not selected_columns:
            return

        for col in selected_columns:
            if self.data[col].isnull().any():
                self.data[col].fillna(self.data[col].mean(), inplace=True)

        self._add_to_history('fill_null_with_mean',
                             f'Rellenados valores nulos en columnas: {", ".join(selected_columns)}')

        if ui_callback:
            ui_callback(self.data)
        messagebox.showinfo("Éxito", "Valores nulos rellenados con la media.")

    def fill_null_values_with_dialog(self, ui_callback=None):
        """
        Abre una ventana de diálogo para seleccionar columnas y un método de rellenado de valores nulos.

        Este método permite al usuario seleccionar las columnas que desea procesar y elegir uno de los métodos disponibles 
        para rellenar los valores nulos en esas columnas. Los métodos disponibles incluyen: Media, Interpolación Lineal, 
        Interpolación Polinomial y KNN. Si se selecciona la interpolación polinomial, también se solicita el grado del polinomio.

        Args:
            ui_callback (function, optional): Función de devolución de llamada que se ejecuta después de 
            completar la operación. Recibe los datos actualizados como argumento. Por defecto es None.

        Returns:
            None: Este método no retorna ningún valor, pero modifica los datos de la clase y puede ejecutar una función
            adicional definida por el usuario a través de `ui_callback`.
        """
        # Seleccionar columnas
        selected_columns = self.select_columns()
        if not selected_columns:
            return

        # Opciones de métodos de rellenado
        methods = [
            "Media",
            "Interpolación Lineal",
            "Interpolación Polinomial",
            "KNN"
        ]
        selected_method = self.select_option("Método de Rellenado", methods)

        if not selected_method:
            return

        # Si se selecciona interpolación polinomial, pedir grado
        degree = None
        if selected_method == "Interpolación Polinomial":
            degree = askstring("Grado Polinomial", "Ingrese el grado para la interpolación polinomial:")
            if not degree or not degree.isdigit():
                messagebox.showerror("Error", "Grado no válido.")
                return
            degree = int(degree)

        # Mapear el método seleccionado al argumento para fill_null_values
        method_mapping = {
            "Media": "mean",
            "Interpolación Lineal": "linear",
            "Interpolación Polinomial": "polynomial",
            "KNN": "knn",
        }
        selected_method_key = method_mapping.get(selected_method)

        # Aplicar el método seleccionado solo a las columnas seleccionadas
        self.fill_null_values(method=selected_method_key, degree=degree, columns=selected_columns)
        if ui_callback:
            ui_callback(self.data)



    def select_option(self, title, options):
        """
        Muestra un cuadro de diálogo con botones de radio para seleccionar una opción.

        Args:
            title (str): Título del cuadro de diálogo.
            options (list): Opciones para mostrar en los botones de radio.

        Returns:
            str: La opción seleccionada por el usuario, o None si la ventana se cierra.
        """
        popup = Toplevel()
        popup.title(title)
        popup.geometry("300x300")

        selected_option = StringVar()
        selected_option.set(None)  # Ninguna selección inicial

        label = ttk.Label(popup, text="Seleccione un método:", font=("Helvetica", 12))
        label.pack(pady=10)

        # Crear botones de radio para cada opción
        for option in options:
            ttk.Radiobutton(
                popup,
                text=option,
                variable=selected_option,
                value=option
            ).pack(anchor="w", padx=20, pady=5)

        # Crear un Frame para alinear los botones
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=20)

        # Botón para confirmar
        btn_confirm = ttk.Button(button_frame, text="Confirmar", command=popup.destroy)
        btn_confirm.pack(side="left", padx=10)

        # Botón para cancelar
        btn_cancel = ttk.Button(button_frame, text="Salir", command=lambda: [selected_option.set(None), popup.destroy()])
        btn_cancel.pack(side="left", padx=10)

        # Manejar cierre con "X"
        popup.protocol("WM_DELETE_WINDOW", lambda: [selected_option.set(None), popup.destroy()])

        popup.wait_window()  # Espera hasta que el usuario cierre la ventana

        # Retorna la opción seleccionada (o None si se cierra sin confirmar)
        return selected_option.get() if selected_option.get() else None


if __name__ == "__main__":
    app = LaboratorySoftware()
    app.run()