import tkinter as tk
from tkinter import ttk, StringVar, messagebox, Text, Scrollbar, Menu, simpledialog, Toplevel
import webbrowser, pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

    Atributos:
        root (tk.Tk): Ventana principal de la aplicación.
        main_frame (ttk.PanedWindow): Panel principal dividido que contiene la tabla de datos y resultados.
        data_frame (ttk.LabelFrame): Marco para la tabla de datos.
        results_frame (ttk.LabelFrame): Marco para mostrar resultados y gráficas.
        data_table (ttk.Treeview): Tabla para visualizar los datos cargados.
        data_ops (DataOperationsWithUI): Instancia para operaciones de datos con UI.
        no_data_label (ttk.Label): Etiqueta mostrada cuando no hay datos cargados.
        regression_canvas (tk.Canvas): Canvas donde se muestran las gráficas generadas por las regresiones y análisis.
        regression (RegressionAnalysis): Instancia encargada de realizar los análisis estadísticos como regresión lineal y polinómica.

    Requiere:
        - `VariableSelectionDialog`: Diálogo para la selección de variables en los análisis de regresión.
        - `DataOperationsWithUI`: Clase encargada de las operaciones de carga, procesamiento y exportación de datos.
    """
    
    def __init__(self) -> None:
        """
        Inicializa la aplicación del Software de Laboratorio.

        Este método configura la interfaz gráfica de usuario utilizando `tkinter`. Establece las dimensiones de la ventana principal
        según el tamaño de la pantalla del usuario, organiza los paneles principales, las pestañas para visualización de datos y teoría,
        y configura los menús para manejar acciones como importar, exportar y realizar análisis de regresión.

        Detalles:
        --------
        - La ventana principal (`self.root`) se ajusta dinámicamente al 80% del ancho y alto de la pantalla y se centra.
        - Se utiliza un `PanedWindow` horizontal (`self.main_frame`) para dividir la interfaz en dos secciones:
            1. **Panel izquierdo** (`self.data_frame`): Contiene un `Notebook` con pestañas para una tabla de datos y una sección de regresión.
            2. **Panel derecho** (`self.frame_teoria`): Un área de ancho fijo para mostrar documentos PDF relacionados con la teoría.
        - Se inicializan métodos y componentes adicionales para mejorar la interacción con la interfaz:
            - `self.create_data_table(self.tab_datos)`: Configura la tabla de datos dentro de la pestaña "Tabla".
            - `self.regression_canvas`: Un `Frame` que contendrá las gráficas de regresión, embebido en la pestaña "Regresión".
            - `self.notebook`: Contiene las pestañas de teoría para "Caída Libre" y "Ley de Hooke", con carga diferida del PDF correspondiente.
        - Los módulos `DataOperationsWithUI` y `RegressionAnalysis` se inicializan para manejar las operaciones de datos y análisis de regresión.
        - Un mensaje de texto inicial (`self.no_data_label`) informa al usuario sobre la necesidad de cargar datos.

        Eventos Configurados:
        ---------------------
        - `<Configure>`: Ajusta la posición del separador (`sash`) del `PanedWindow` para mantener el ancho fijo del panel de teoría.
        - `<<NotebookTabChanged>>`: Llama a `self.on_tab_change` para cargar el PDF correspondiente al cambiar de pestaña en la teoría.
        - `WM_DELETE_WINDOW`: Asocia el evento de cierre de la ventana con `self.on_close` para realizar limpieza antes de cerrar.

        Menú:
        -----
        - Configurado mediante `self.setup_menus()`, incluye opciones para importar datos, exportar, procesar, y realizar regresiones.

        Notas:
        ------
        - La estructura y los componentes de la interfaz gráfica están diseñados para ofrecer una navegación intuitiva y eficaz entre
        la visualización de datos y teoría.
        - La inicialización establece las bases para la interacción entre los módulos de manipulación de datos y gráficos personalizados.
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

        # Crear el Notebook en el panel de datos
        self.data_notebook = ttk.Notebook(self.data_frame)
        self.data_notebook.pack(fill=tk.BOTH, expand=True)

        # Crear las pestañas dentro del Notebook de datos
        self.tab_datos = ttk.Frame(self.data_notebook)
        self.tab_regresion = ttk.Frame(self.data_notebook)

        self.data_notebook.add(self.tab_datos, text="Tabla")
        self.data_notebook.add(self.tab_regresion, text="Regresión")

        # Crear la tabla de datos en la pestaña "Tabla"
        self.create_data_table(self.tab_datos)  # Puedes modificar el método create_data_table para aceptar un marco como argumento

        # Crear un Canvas para mostrar las gráficas en la pestaña de Regresión
        self.regression_canvas = ttk.Frame(self.tab_regresion)
        self.regression_canvas.pack(fill=tk.BOTH, expand=True)

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

        # Crear el Notebook para la teoría
        self.notebook = ttk.Notebook(self.frame_teoria)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Crear las pestañas en el Notebook de teoría
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

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """
        Maneja el evento de cierre de la aplicación.

        Este método realiza las tareas de limpieza necesarias antes de finalizar la ejecución del programa.
        - Detiene el bucle de eventos de la interfaz gráfica llamando a `self.root.quit()`.
        - Destruye la ventana principal con `self.root.destroy()`, liberando los recursos asociados.

        Notas:
        ------
        - Se recomienda usar este método para asegurarse de que los procesos abiertos se cierren correctamente
        y evitar errores de cierre incorrecto o bloqueos en la terminal.
        - Este método está vinculado al protocolo `WM_DELETE_WINDOW`, lo que permite manejar el evento de cierre de
        la ventana con un comportamiento personalizado.
        """
        # Aquí puedes realizar cualquier acción de limpieza antes de cerrar
        self.root.quit()  # Termina el bucle de eventos de Tkinter
        self.root.destroy()  # Cierra la ventana

    def load_pdf(self, tab, pdf_path):
        """
        Carga un archivo PDF y lo visualiza dentro de una pestaña específica en la interfaz gráfica.

        Args:
            tab (tk.Widget): Contenedor en el que se mostrará el contenido del PDF.
            pdf_path (str): Ruta del archivo PDF que se desea visualizar.

        Descripción:
            - Elimina cualquier contenido existente dentro del contenedor antes de cargar el nuevo PDF.
            - Utiliza la librería `fitz` (PyMuPDF) para cargar y procesar el PDF.
            - Escala cada página del PDF basándose en el ancho del contenedor para lograr una visualización adaptada.
            - Renderiza cada página como una imagen y la coloca dentro de un Canvas con barra de desplazamiento.

        Detalles Técnicos:
            - Las imágenes renderizadas se generan utilizando `get_pixmap` de `fitz` para aplicar un factor de escala adecuado.
            - Se utiliza un Canvas dentro de un Frame para permitir desplazamiento vertical, proporcionando una experiencia fluida.
            - Cada imagen de página es almacenada como referencia en el atributo `image` de los widgets para evitar la recolección de basura.

        Ejemplo:
            ```python
            app.load_pdf(tab_frame, "manual_usuario.pdf")
            ```

        Notas:
            - Es necesario tener instalados los paquetes `PyMuPDF` (fitz) y `Pillow` (PIL).
            - Si el archivo PDF contiene muchas páginas, la carga puede tomar algo de tiempo dependiendo del sistema.

        Requiere:
            - fitz (PyMuPDF)
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
        Gestiona el evento de cambio de pestaña en el cuaderno de teoría y carga el PDF correspondiente.

        Args:
            event (tk.Event): El evento generado al cambiar de pestaña en el widget `ttk.Notebook`.

        Descripción:
            - Este método detecta la pestaña activa en el `Notebook` y carga el archivo PDF asociado a la pestaña seleccionada.
            - Utiliza el método `load_pdf` para renderizar el contenido del PDF dentro de cada pestaña específica.
        
        Mapeo de pestañas a archivos PDF:
            - "Caída libre" → `caida_libre.pdf`
            - "Ley de Hooke" → `ley_de_hooke.pdf`

        Ejemplo de uso:
            ```python
            # Vincula el evento de cambio de pestaña al método
            self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
            ```

        Notas:
            - Se asume que las pestañas tienen etiquetas de texto coincidentes con los nombres definidos.
            - Los archivos PDF deben estar accesibles en las rutas especificadas.
            - El método `load_pdf` debe estar implementado en la misma clase.

        Requiere:
            - PyMuPDF (fitz)
            - PIL (Pillow)
        """
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if selected_tab == "Caída libre":
            self.load_pdf(self.tab_cai_libre, "caida_libre.pdf")
        elif selected_tab == "Ley de Hooke":
            self.load_pdf(self.tab_ley_hooke, "ley_de_hooke.pdf")

    def create_data_table(self, parent=None):
        """
        Crea y configura una tabla de tipo `Treeview` dentro de un contenedor, con soporte para barras de desplazamiento vertical y horizontal.

        Este método inicializa un widget `Treeview` para mostrar datos en formato tabular, con barras de desplazamiento
        asociadas al desplazamiento tanto horizontal como vertical. También aplica estilos básicos a la tabla para mejorar
        la visualización, como el ajuste de la altura de las filas y el formato de los encabezados.

        Args:
            parent (tk.Widget, opcional): El contenedor en el que se colocará la tabla. Si no se proporciona, se usa el contenedor predeterminado.
        
        Descripción:
            - Crea un `Frame` dentro del contenedor proporcionado para albergar la tabla.
            - Configura barras de desplazamiento tanto verticales como horizontales que permiten navegar por la tabla.
            - Aplica un estilo básico para mejorar la apariencia de la tabla y los encabezados.
            - El tamaño de la tabla se ajusta dinámicamente al tamaño del contenedor.

        Notas:
            - Este método solo configura la estructura de la tabla. Los datos deben ser insertados posteriormente con el método `insert`.
            - El tamaño de la tabla se adapta automáticamente al contenedor donde se coloca.

        Ejemplo:
            ```python
            # Crear la tabla dentro de un contenedor específico
            app.create_data_table(tab_datos)
            
            # Insertar datos en la tabla
            for row in data:
                app.data_table.insert('', 'end', values=row)
            ```

        Requiere:
            - Ninguna librería adicional para la creación de la tabla y los controles de desplazamiento.
        """
        if parent is None:
            parent = self.data_frame  # Usar el panel por defecto si no se pasa uno

        # Frame para contener la tabla y scrollbars
        self.table_frame = ttk.Frame(parent)
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
        Actualiza la tabla de tipo `Treeview` con los nuevos datos proporcionados en un DataFrame.

        Este método limpia el contenido actual de la tabla y la actualiza con los datos del DataFrame proporcionado.
        Si el DataFrame es `None` o está vacío, se muestra un mensaje indicando la ausencia de datos.

        Args:
            data (pd.DataFrame): Un DataFrame con los datos a mostrar. 
                - Si el DataFrame es `None` o está vacío, se muestra un mensaje de "No hay datos disponibles".

        Detalles:
            - Se limpia el contenido actual de la tabla antes de insertar nuevos datos.
            - Se configuran dinámicamente las columnas de la tabla basándose en los nombres de las columnas del DataFrame.
            - Se insertan las filas del DataFrame en la tabla, formateando los valores como cadenas.
            - Si no hay datos disponibles, se muestra un label con el mensaje correspondiente.

        Notas:
            - El ancho inicial de las columnas se establece en 100 unidades, pero puede ser ajustado por el usuario.
            - Se utiliza `self.no_data_label` para mostrar un mensaje de ausencia de datos cuando sea necesario.

        Ejemplo:
            ```python
            # Crear un DataFrame
            df = pd.DataFrame({'Columna1': [1, 2, 3], 'Columna2': ['A', 'B', 'C']})
            
            # Actualizar la tabla con el DataFrame
            app.update_data_display(df)
            ```

        Requiere:
            - `self.data_table`: Un widget `Treeview` previamente inicializado para mostrar los datos.
            - `self.no_data_label`: Un label para mostrar el mensaje de "No hay datos disponibles".
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
        """
        Configura la barra de menús de la interfaz gráfica de la aplicación.

        Este método crea un menú con las siguientes opciones:
        - **Archivo**: Para importar, exportar y salir de la aplicación.
        - **Edición**: Para procesar datos, como eliminar nulos, eliminar duplicados, normalizar datos, y rellenar valores nulos con la media.
        - **Regresiones**: Submenú dentro de Edición para realizar regresión lineal, polinómica e interpolación de Lagrange.
        - **Ver**: Para abrir el componente de graficación de la aplicación.
        - **Acerca de**: Para acceder a la documentación y mostrar información sobre los autores.

        Ejemplo de uso:
            ```python
            app.setup_menus()  # Configura la barra de menús en la ventana principal
            ```

        Requiere:
            - Métodos asociados a las opciones de menú como `self.data_ops.load_file`, `self.data_ops.export_results`, etc.
        """
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
        """
        Muestra una ventana de información con los nombres de los autores del software.

        Este método usa un cuadro de mensaje (`messagebox`) para mostrar los nombres de los autores cuando se selecciona la opción
        "Autores" en el menú "Acerca de" de la aplicación.

        Ejemplo de uso:
            ```python
            app.show_autores()  # Muestra la información de los autores
            ```

        Requiere:
            - `messagebox.showinfo` de la librería `tkinter` para mostrar la ventana emergente con los autores.
        """
        autores = "Andrés Gómez\nJorge Garzón\nJulián Aros\nLaura Oliveros\nLaura Triana\nSebastian Manrique"
        messagebox.showinfo("Autores", autores)

    def open_graficador(self):
        """
        Abre una nueva ventana ejecutando `graficador.py` y exporta los datos actuales a un archivo temporal `tmp_graph.pkl`.

        Este método guarda los datos del DataFrame cargado en la aplicación en un archivo `tmp_graph.pkl` y luego ejecuta 
        el script `graficador.py` en un proceso independiente. Si no hay datos disponibles, muestra un mensaje de error.

        Retorna:
            bool: `True` si se ejecuta correctamente, `False` si ocurre algún error.

        Ejemplo de uso:
            ```python
            app.open_graficador()  # Ejecuta graficador.py y exporta los datos
            ```

        Requiere:
            - `pickle` para guardar el DataFrame en un archivo.
            - `subprocess.Popen` para ejecutar `graficador.py` en un proceso independiente.
            - `sys` para obtener la ruta del ejecutable de Python.
            - `messagebox.showerror` para mostrar mensajes de error.
        """
        try:
            # Exportar a tmp_graph.pkl
            if self.data_ops.data is None:
                messagebox.showerror("Error", "No hay datos para exportar")
                return False
            
            # Guardar el DataFrame en un archivo .pkl
            with open('tmp_graph.pkl', 'wb') as f:
                pickle.dump(self.data_ops.data, f)

            # Ejecutar el archivo graficador.py como un proceso independiente
            subprocess.Popen([sys.executable, 'graficador.py'])
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar graficador.py o exportar los datos: {str(e)}")
            return False

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

        Requiere:
            - `self.root`: El widget raíz de la ventana de Tkinter.
        """
        self.root.mainloop()

    def perform_linear_regression(self):
        """
        Realiza una regresión lineal sobre los datos cargados.

        Este método verifica si hay datos disponibles en `self.data_ops.data` y, en caso afirmativo,
        llama al método `linear_regression` del objeto `self.regression` para realizar la regresión lineal.

        Detalles:
            - Si no hay datos cargados, muestra una advertencia.
            - La regresión lineal se realiza utilizando los datos actuales.

        Ejemplo:
            ```python
            app.perform_linear_regression()
            ```

        Requiere:
            - `self.data_ops.data`: Los datos que deben ser procesados.
            - `self.regression.linear_regression`: El método que ejecuta la regresión lineal.
        """
        if self.data_ops.data is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return
        self.regression.linear_regression()

    def perform_polynomial_regression(self):
        """
        Realiza una regresión polinómica sobre los datos cargados.

        Este método verifica si hay datos disponibles en `self.data_ops.data` y, en caso afirmativo,
        llama al método `polynomial_regression` del objeto `self.regression` para realizar la regresión polinómica.

        Detalles:
            - Si no hay datos cargados, muestra una advertencia.
            - La regresión polinómica se realiza utilizando los datos actuales.

        Ejemplo:
            ```python
            app.perform_polynomial_regression()
            ```

        Requiere:
            - `self.data_ops.data`: Los datos que deben ser procesados.
            - `self.regression.polynomial_regression`: El método que ejecuta la regresión polinómica.
        """
        if self.data_ops.data is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return
        self.regression.polynomial_regression()

    def perform_lagrange_interpolation(self):
        """
        Realiza una interpolación de Lagrange sobre los datos cargados.

        Este método verifica si hay datos disponibles en `self.data_ops.data` y, en caso afirmativo,
        llama al método `interpolation` del objeto `self.regression` para realizar la interpolación de Lagrange.

        Detalles:
            - Si no hay datos cargados, muestra una advertencia.
            - La interpolación de Lagrange se realiza utilizando los datos actuales.

        Ejemplo:
            ```python
            app.perform_lagrange_interpolation()
            ```

        Requiere:
            - `self.data_ops.data`: Los datos que deben ser procesados.
            - `self.regression.interpolation`: El método que ejecuta la interpolación de Lagrange.
        """
        if self.data_ops.data is None:
            messagebox.showwarning("Advertencia", "No hay datos cargados")
            return
        self.regression.interpolation()

    def linear_regression(self):
        """
        Realiza una regresión lineal sobre los datos seleccionados por el usuario.

        Este método muestra un cuadro de diálogo para que el usuario seleccione las variables para la regresión
        (una independiente `var_x` y una dependiente `var_y`). Luego, realiza la regresión lineal utilizando el
        método `linear_regression` de la clase `RegressionAnalysis` y muestra la gráfica resultante.

        Detalles:
            - Verifica que los datos estén disponibles utilizando el método `check_data()`.
            - Permite al usuario seleccionar las variables para la regresión.
            - Muestra la gráfica de la regresión en un `Canvas` de la interfaz.

        Ejemplo:
            ```python
            app.linear_regression()
            ```

        Requiere:
            - `self.check_data()`: Verifica que los datos estén disponibles.
            - `VariableSelectionDialog`: Un cuadro de diálogo para seleccionar las variables.
            - `self.regression.linear_regression`: Realiza la regresión lineal.
            - `self.show_plot_in_canvas`: Muestra la gráfica generada en el `Canvas`.
        """
        if not self.check_data():
            return

        # Obtener columnas disponibles
        columns = list(self.data_ops.data.columns)
        
        # Diálogo para seleccionar variables
        dialog = VariableSelectionDialog(self.root, columns)
        if dialog.result:
            var_x, var_y = dialog.result
            try:
                # Llamar al método de regresión lineal desde RegressionAnalysis y obtener la figura
                fig = self.regression.linear_regression(var_x, var_y, ax1=None, return_metrics=True)

                # Mostrar la gráfica en el Canvas de la pestaña de Regresión
                self.show_plot_in_canvas(fig)

            except Exception as e:
                messagebox.showerror("Error", f"Error en la regresión: {str(e)}")

    def polynomial_regression(self):
        """
        Realiza una regresión polinómica sobre los datos seleccionados por el usuario.

        Este método muestra un cuadro de diálogo para que el usuario seleccione las variables para la regresión
        (una independiente `var_x` y una dependiente `var_y`). Luego, realiza la regresión polinómica utilizando el
        método `polynomial_regression` de la clase `RegressionAnalysis` y muestra la gráfica resultante.

        Detalles:
            - Verifica que los datos estén disponibles utilizando el método `check_data()`.
            - Permite al usuario seleccionar las variables para la regresión.
            - Muestra la gráfica de la regresión polinómica en un `Canvas` de la interfaz.

        Ejemplo:
            ```python
            app.polynomial_regression()
            ```

        Requiere:
            - `self.check_data()`: Verifica que los datos estén disponibles.
            - `VariableSelectionDialog`: Un cuadro de diálogo para seleccionar las variables.
            - `self.regression.polynomial_regression`: Realiza la regresión polinómica.
            - `self.show_plot_in_canvas`: Muestra la gráfica generada en el `Canvas`.
        """
        if not self.check_data():
            return

        # Obtener columnas disponibles
        columns = list(self.data_ops.data.columns)
        
        # Diálogo para seleccionar variables
        dialog = VariableSelectionDialog(self.root, columns)
        if dialog.result:
            var_x, var_y = dialog.result
            try:
                # Llamar al método de regresión polinómica desde RegressionAnalysis y obtener la figura
                fig = self.regression.polynomial_regression(var_x, var_y, ax1=None, return_metrics=True)

                # Mostrar la gráfica en el Canvas de la pestaña de Regresión
                self.show_plot_in_canvas(fig)

            except Exception as e:
                messagebox.showerror("Error", f"Error en la regresión polinómica: {str(e)}")

    def interpolation(self):
        """
        Realiza una interpolación de Lagrange sobre los datos seleccionados por el usuario.

        Este método muestra un cuadro de diálogo para que el usuario seleccione las variables para la interpolación
        (una independiente `var_x` y una dependiente `var_y`). Luego, realiza la interpolación utilizando el método
        `interpolation` de la clase `RegressionAnalysis` y muestra la gráfica resultante.

        Detalles:
            - Verifica que los datos estén disponibles utilizando el método `check_data()`.
            - Permite al usuario seleccionar las variables para la interpolación.
            - Muestra la gráfica de la interpolación en un `Canvas` de la interfaz.

        Ejemplo:
            ```python
            app.interpolation()
            ```

        Requiere:
            - `self.check_data()`: Verifica que los datos estén disponibles.
            - `VariableSelectionDialog`: Un cuadro de diálogo para seleccionar las variables.
            - `self.regression.interpolation`: Realiza la interpolación de Lagrange.
            - `self.show_plot_in_canvas`: Muestra la gráfica generada en el `Canvas`.
        """
        if not self.check_data():
            return

        # Obtener columnas disponibles
        columns = list(self.data_ops.data.columns)
        
        # Diálogo para seleccionar variables
        dialog = VariableSelectionDialog(self.root, columns)
        if dialog.result:
            var_x, var_y = dialog.result
            try:
                # Llamar al método de interpolación desde RegressionAnalysis y obtener la figura
                fig = self.regression.interpolation(var_x, var_y, ax1=None, return_metrics=True)

                # Mostrar la gráfica en el Canvas de la pestaña de Regresión
                self.show_plot_in_canvas(fig)

            except Exception as e:
                messagebox.showerror("Error", f"Error en la interpolación: {str(e)}")

    def check_data(self):
        """
        Verifica si hay datos cargados en la aplicación antes de realizar cualquier análisis.

        Este método revisa si el atributo `self.data_ops.data` contiene datos. Si no es así, muestra una advertencia
        al usuario indicando que no hay datos cargados, y retorna `False`. Si hay datos, retorna `True`.

        Detalles:
            - Es útil para asegurarse de que haya datos antes de ejecutar análisis como regresiones o interpolaciones.

        Ejemplo:
            ```python
            if app.check_data():
                app.linear_regression()
            ```

        Requiere:
            - `self.data_ops.data`: Un atributo que debe contener los datos cargados en la aplicación.
        """
        if self.data_ops.data is None:
            messagebox.showwarning("Advertencia", 
                                "No hay datos cargados para realizar el análisis")
            return False
        return True

    def show_plot_in_canvas(self, fig):
        """
        Muestra la gráfica en el Canvas de la pestaña de Regresión.

        Este método limpia cualquier gráfico previo que se haya mostrado en el Canvas y luego
        dibuja el nuevo gráfico generado. La gráfica se crea a partir de un objeto `fig` (Figura de Matplotlib)
        y se muestra en el canvas asociado a la pestaña de Regresión.

        Detalles:
            - El método primero limpia cualquier gráfico previamente mostrado en el Canvas.
            - Luego, utiliza `FigureCanvasTkAgg` de Matplotlib para convertir la figura en un widget de Tkinter.
            - Finalmente, se empaqueta el widget del Canvas en el frame para que sea visible.

        Ejemplo:
            ```python
            fig = some_matplotlib_figure  # Figura generada por un análisis
            app.show_plot_in_canvas(fig)  # Mostrar la figura en el canvas
            ```

        Requiere:
            - `self.regression_canvas`: Un `Frame` de Tkinter donde se mostrará la gráfica.
            - `fig`: Un objeto `matplotlib.figure.Figure` que contiene el gráfico a mostrar.
        """
        # Limpiar cualquier gráfico anterior en la pestaña
        for widget in self.regression_canvas.winfo_children():
            widget.destroy()

        # Mostrar la nueva gráfica en el Canvas de la pestaña de Regresión
        canvas = FigureCanvasTkAgg(fig, master=self.regression_canvas)  # Crear canvas con la figura
        canvas.draw()  # Dibujar la figura en el canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Empacar el widget canvas en el frame

class VariableSelectionDialog:
    """
    Clase para crear un cuadro de diálogo modal que permite al usuario seleccionar dos variables (X e Y)
    de un conjunto de columnas disponibles. El usuario puede seleccionar las variables a través de menús
    desplegables y luego confirmar su selección con un botón de "Aceptar".

    Attributes:
        dialog (tk.Toplevel): Ventana emergente del cuadro de diálogo para la selección de variables.
        result (tuple): Tupla que almacena la selección de las variables X e Y, o None si no se ha realizado
                        ninguna selección.
        var_x (ttk.Combobox): Menú desplegable para seleccionar la variable X.
        var_y (ttk.Combobox): Menú desplegable para seleccionar la variable Y.
    """

    def __init__(self, parent, columns):
        """
        Inicializa el cuadro de diálogo con menús desplegables para seleccionar las variables X e Y.

        Args:
            parent (tk.Tk): La ventana principal o widget padre que invoca el diálogo.
            columns (list): Lista de columnas disponibles para seleccionar las variables.
        """
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
        """
        Método que se llama cuando el usuario hace clic en el botón de "Aceptar".
        
        Si ambas variables X e Y son seleccionadas, almacena las selecciones en el atributo `result` 
        y cierra el diálogo.
        """
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
            degree = simpledialog.askstring("Grado Polinomial", "Ingrese el grado para la interpolación polinomial:")
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