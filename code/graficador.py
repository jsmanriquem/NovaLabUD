# Librerías necesarias para realizar un graficador
from tkinter import Tk, Frame, Button, Label, Menu, Toplevel, StringVar, ttk, Entry, filedialog, colorchooser, Scale, HORIZONTAL , IntVar, Checkbutton, messagebox, colorchooser, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from regression_analysis import RegressionAnalysis
import os, pickle, webbrowser

# Ventana principal
raiz = Tk()
raiz.geometry("735x800")  # Tamaño de la pantalla
raiz.config(bg="gray")  # Color de fondo
raiz.wm_title('Gráfica de datos')  # Título de la gráfica
regresiones = []  # Lista para almacenar los de regresión

def centrar_ventana(ventana_principal, ventana_emergente):
    raiz.update_idletasks()

    # Obtener dimensiones y posición de la ventana principal
    ancho_principal = raiz.winfo_width()
    alto_principal = raiz.winfo_height()
    pos_x_principal = raiz.winfo_x()
    pos_y_principal = raiz.winfo_y()

    # Obtener dimensiones de la ventana emergente
    ancho_emergente = ventana_emergente.winfo_width()
    alto_emergente = ventana_emergente.winfo_height()

    # Calcular posición centrada con respecto a la ventana principal
    x_centrado = pos_x_principal + (ancho_principal - ancho_emergente) // 2
    y_centrado = pos_y_principal + (alto_principal - alto_emergente) // 2

    # Establecer geometría centrada
    ventana_emergente.geometry(f"{ancho_emergente}x{alto_emergente}+{x_centrado}+{y_centrado}")

def limpiar_grafica():
    """
    Limpia la gráfica actual y restablece sus parámetros a los valores predeterminados.

    Esta función restablece todas las configuraciones visuales de la gráfica, como el título, 
    los colores, los estilos y los tamaños de los ejes. También se desactiva la cuadrícula si está 
    activada y se reinician los límites de los ejes. La gráfica se redibuja con estos valores predeterminados.

    Además, se restaura el estado de las variables globales que controlan las configuraciones visuales
    y otros parámetros gráficos.

    Variables globales:
    ------------------
    x_limits : list
        Lista con los límites actuales del eje 'x' en la forma [xmin, xmax].
    y_limits : list
        Lista con los límites actuales del eje 'y' en la forma [ymin, ymax].
    marker_color : str
        Color predeterminado del marcador en la gráfica.
    marker_type : str
        Tipo de marcador utilizado para los puntos en la gráfica.
    show_grid : bool
        Indicador de si la cuadrícula de la gráfica está activada.
    point_size : int
        Tamaño de los puntos de marcador en la gráfica.
    titulo_grafica : tkinter.StringVar
        Título de la gráfica como variable de texto.
    title_fuente : str
        Tipo de fuente para el título de la gráfica.
    title_size : int
        Tamaño de la fuente para el título de la gráfica.
    ejex_shape : str
        Tipo de fuente del título del eje 'x'.
    ejex_size : int
        Tamaño de la fuente del título del eje 'x'.
    ejex_titulo : tkinter.StringVar
        Título del eje 'x' como variable de texto.
    ejey_shape : str
        Tipo de fuente del título del eje 'y'.
    ejey_size : int
        Tamaño de la fuente del título del eje 'y'.
    ejey_titulo : tkinter.StringVar
        Título del eje 'y' como variable de texto.
    line_color : str
        Color de la línea de la gráfica.
    line_width : int
        Grosor de la línea de la gráfica.
    bg_color : str
        Color de fondo de la gráfica.

    Retorna:
    --------
    None: La función no retorna valor, modifica directamente la configuración visual de la gráfica.

    Uso:
    ----
    Esta función es útil para restablecer los parámetros de la gráfica a sus valores predeterminados,
    permitiendo una visualización limpia y estándar antes de realizar nuevas representaciones gráficas.
    """
    global y_limits, x_limits, origx_lim, origy_lim, marker_color, marker_type, show_grid, point_size, titulo_grafica, title_fuente, title_size, ejex_shape, ejex_size, ejex_titulo, ejey_shape, ejey_size, ejey_titulo, line_color, line_width, bg_color, regresiones

    titulo_grafica = StringVar(value="Título de la Gráfica")
    title_fuente = "DejaVu Sans"
    title_size = 12
    
    ejex_titulo = StringVar(value="")
    ejex_shape = "DejaVu Sans"
    ejex_size = 10

    ejey_titulo = StringVar(value="")
    ejey_shape = "DejaVu Sans"
    ejey_size = 10

    line_color = 'blue' 
    line_width = 2       
    bg_color = "white"
    marker_type = "o"
    marker_color = "blue"
    show_grid = False  
    point_size = 5  

    zoom(reset=True)

    regresiones.clear()  # Vaciar la lista de regresiones

    ax.clear() 
    x_limits = None
    y_limits = None
    origx_lim = None
    origy_lim = None
    
    ax.grid(show_grid)  
    ax.set_facecolor(bg_color)

    canvas.draw() 
    limpio_si()

def confirmar_limpiar_grafica():
    """
    Muestra una ventana emergente de confirmación para limpiar la gráfica.

    Esta función crea una ventana emergente que pregunta al usuario si desea limpiar la gráfica actual. 
    Ofrece dos opciones: "Sí, limpiar" y "No, Cancelar". Si el usuario elige "Sí, limpiar", se llama 
    a la función `limpiar_grafica` y se cierra la ventana de confirmación. Si el usuario elige "No, Cancelar", 
    la ventana se cierra sin modificar la gráfica.

    La ventana de confirmación se centra con respecto a la ventana principal y es modal, lo que significa 
    que bloquea la interacción con otras ventanas de la aplicación hasta que se tome una decisión.

    Variables globales:
    ------------------
    raiz : tkinter.Tk
        Ventana principal de la interfaz gráfica, sobre la cual se despliega la ventana de 
        confirmación.

    Retorna:
    --------
    None: La función no retorna ningún valor. Solo muestra una ventana de confirmación y actúa 
    en función de la respuesta del usuario.

    Uso:
    ----
    Esta función es útil cuando se desea solicitar una confirmación al usuario antes de realizar una 
    acción que modifique la visualización de la gráfica.
    """
    ventana_confirmacion = Toplevel(raiz)
    ventana_confirmacion.title("Confirmación de limpieza")

    mensaje = Label(ventana_confirmacion, text="¿Está seguro que desea limpiar la gráfica?")
    mensaje.pack(pady=10)

    boton_si = Button(ventana_confirmacion, text="Sí, limpiar", command=lambda: [limpiar_grafica(), ventana_confirmacion.destroy()])
    boton_si.pack(side="left", padx=10, pady=10)

    boton_no = Button(ventana_confirmacion, text="No, Cancelar", command=ventana_confirmacion.destroy)
    boton_no.pack(side="right", padx=10, pady=10)

    # Actualizar para obtener las dimensiones de la ventana emergente
    ventana_confirmacion.update_idletasks()

    centrar_ventana(raiz, ventana_confirmacion)

    # Hacer que la ventana emergente sea modal
    ventana_confirmacion.transient(raiz)
    ventana_confirmacion.grab_set()

def limpio_si():
    """
    Muestra una ventana emergente de confirmación indicando que la gráfica ha sido limpiada exitosamente.

    Esta función crea una ventana emergente que informa al usuario que la gráfica ha sido limpiada correctamente. 
    Incluye un mensaje de éxito y un botón de "Aceptar" que cierra la ventana emergente cuando se presiona.

    La ventana emergente se centra con respecto a la ventana principal y es modal, lo que impide la interacción 
    con otras partes de la aplicación hasta que se cierre la ventana de confirmación.

    Variables globales:
    ------------------
    raiz : tkinter.Tk
        Ventana principal de la interfaz gráfica, sobre la cual se despliega la ventana de confirmación.

    Retorna:
    --------
    None: La función no retorna ningún valor. Solo muestra una ventana de confirmación de éxito.

    Uso:
    ----
    Esta función es útil para notificar al usuario que la acción de limpieza de la gráfica se ha realizado con éxito.
    """
    ventana_hecho = Toplevel(raiz)
    ventana_hecho.title("Éxito")

    Label(ventana_hecho, text="La gráfica ha sido limpiada.", pady=20).pack()
    Button(ventana_hecho, text="Aceptar", command=ventana_hecho.destroy).pack(pady=10)

    # Actualizar para obtener las dimensiones de la ventana emergente
    ventana_hecho.update_idletasks()

    centrar_ventana(raiz, ventana_hecho)

    # Hacer que la ventana emergente sea modal
    ventana_hecho.transient(raiz)
    ventana_hecho.grab_set()

# Menú de opciones para el usuario
barraMenu = Menu(raiz)
raiz.config(menu=barraMenu)

# Menú Exportar
exportarMenu = Menu(barraMenu, tearoff=0)
exportarMenu.add_command(label="PDF", command=lambda: guardar_grafica('pdf'))
exportarMenu.add_command(label="JPG", command=lambda: guardar_grafica('jpg'))
exportarMenu.add_command(label="PNG", command=lambda: guardar_grafica('png'))
barraMenu.add_cascade(label="Exportar", menu=exportarMenu)

# Opción Limpiar
barraMenu.add_command(label="Limpiar", command=confirmar_limpiar_grafica)

# Menú Regresiones
regresionMenu = Menu(barraMenu, tearoff=0)
regresionMenu.add_command(label="R. Lineal", command=lambda: graficar_regresion('lineal'))
regresionMenu.add_command(label="R. Polinomial", command=lambda: graficar_regresion('polinomial'))
regresionMenu.add_command(label="Interpolación", command=lambda: graficar_regresion('interpolacion'))
barraMenu.add_cascade(label="Regresiones", menu=regresionMenu)

# Menú Personalización
personalizarMenu = Menu(barraMenu, tearoff=0)
personalizarMenu.add_command(label="Editar gráfica", command=lambda: grafica_ventana(raiz))
# Opciones para personalizar las líneas de regresión
personalizarMenu.add_command(label="Editar Regresión Lineal", command=lambda: grafica_ventana_regresion(raiz, 'Lineal'))
personalizarMenu.add_command(label="Editar Regresión Polinomial", command=lambda: grafica_ventana_regresion(raiz, 'Polinomial'))
personalizarMenu.add_command(label="Editar Regresión por Interpolación", command=lambda: grafica_ventana_regresion(raiz, 'Interpolación de Lagrange'))
barraMenu.add_cascade(label="Personalizar", menu=personalizarMenu)

# Menú Ayuda (abre un enlace en el navegador)
barraMenu.add_command(label="Ayuda", command=lambda: webbrowser.open("http://tulink.com"))

# Crear el frame para las columnas
frame_columnas = Frame(raiz)
frame_columnas.grid(column=0, row=2, padx=10, pady=5, columnspan=3)

# Frame para la gráfica
frame = Frame(raiz, bg='gray22', bd=3)
frame.grid(column=0, row=0, sticky='nsew')

# Crear la figura y el canvas
fig, ax = plt.subplots(dpi=90, figsize=(8, 6), facecolor='#D3D3D3')
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(column=0, row=0, padx=5, pady=5)

# Variables predeterminadas para los títulos
titulo_grafica = StringVar(value="Título de la Gráfica")
title_fuente = "DejaVu Sans"
title_size = 12
personal_ventana_title = None  # Inicializamos la ventana emergente como None

ejex_titulo = StringVar(value="")
ejex_shape = "DejaVu Sans"
ejex_size = 10
ventana_ejex = None # Venta emergente edición eje x
ventana_lim_x = None # Venta emergente edición límites eje x

ejey_titulo = StringVar(value="")
ejey_shape = "DejaVu Sans"
ejey_size = 10
ventana_ejey = None # Ventana emerjente edición eje y
ventana_lim_y = None # Venta emergente edición límites eje y

# Variables de personalización
line_color = 'blue' 
line_width = 2       
bg_color = "white"
marker_type = "o"
marker_color = "blue"
show_grid = False  # Variable para controlar si la grilla está activa o no
point_size = 5  # Tamaño de los puntos
line = None
personalizacion_ventana= None

# Inicializar variables para manejo del zoom y desplazamiento
x_limits = None
y_limits = None
is_dragging = False
start_x, start_y = 0, 0
points = None  # Objeto necesario para almacenamiento de puntos y posterior edición

# Variables para las columnas
columna_x = StringVar()
columna_y = StringVar()

# Widgets de selección
columna_x_combo = None
columna_y_combo = None
graficar_button = None

# Guardar límites originales para reestablecer al tamaño original
origx_lim = None
origy_lim = None

# Variable global para almacenar los datos cargados
data = pd.DataFrame()  # Inicializar como DataFrame vacío

def cargar_datos():
    """
    Carga los datos desde un archivo temporal llamado 'tmp_graph.pkl' al iniciar la aplicación.
    Si el archivo existe, los datos se cargan en la variable global `data`. Si no existe,
    muestra un mensaje de advertencia.

    Almacena los datos en la variable global `data` para ser utilizados en toda la aplicación.
    """
    global data

    if os.path.exists("tmp_graph.pkl"):
        try:
            # Cargar archivo temporal .pkl en un DataFrame
            with open("tmp_graph.pkl", 'rb') as f:
                data = pickle.load(f)

            if not data.empty:
                actualizar_columnas()  # Actualizar opciones de columnas
            else:
                messagebox.showerror("Error", "El archivo 'tmp_graph.pkl' está vacío.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
    else:
        messagebox.showwarning("Advertencia", "No se encontró el archivo 'tmp_graph.pkl'.")

reg_analysis = RegressionAnalysis(data)

def actualizar_columnas():
    """
    Obtiene los nombres de las columnas del archivo de datos cargado y actualiza los elementos 
    de la interfaz para permitir la selección de columnas para graficar.

    Esta función obtiene los nombres de las columnas del archivo de datos actualmente cargado en 
    la variable global `data`. Luego, actualiza o crea los ComboBox para que el usuario pueda 
    seleccionar las columnas para los ejes 'X' e 'Y'. Además, coloca un botón que permite iniciar 
    la graficación de los datos seleccionados. Si no hay columnas disponibles, se muestra un mensaje 
    de error indicando que no se pueden graficar los datos.

    Variables globales:
    ------------------
    columna_x_combo : ttk.Combobox
        Widget de tipo Combobox para la selección de la columna en el eje X.
    
    columna_y_combo : ttk.Combobox
        Widget de tipo Combobox para la selección de la columna en el eje Y.
    
    graficar_button : tkinter.Button
        Botón para iniciar la acción de graficar los datos seleccionados.
    
    frame_columnas : tkinter.Frame
        Frame en el que se colocan los widgets de selección de columnas y el botón de graficado.

    Retorna:
    --------
    None: La función no retorna ningún valor. Solo actualiza los widgets de la interfaz gráfica.
    
    Uso:
    ----
    Esta función es útil para permitir al usuario seleccionar las columnas que desea graficar 
    y controlar el inicio de la graficación desde la interfaz.
    """
    global columna_x_combo, columna_y_combo, graficar_button, frame_columnas

    # Eliminar widgets previos del frame
    for widget in frame_columnas.winfo_children():
        widget.destroy()

    # Obtener las columnas del archivo de datos
    columns = data.columns.tolist()

    # Solo crear los ComboBox si hay columnas disponibles
    if columns:
        # ComboBox para columna X
        columna_x_combo = ttk.Combobox(frame_columnas, textvariable=columna_x, values=columns)
        columna_x_combo.grid(column=0, row=0, padx=5, pady=5)
        columna_x_combo.set("Selecciona la columna X")
        
        # ComboBox para columna Y
        columna_y_combo = ttk.Combobox(frame_columnas, textvariable=columna_y, values=columns)
        columna_y_combo.grid(column=1, row=0, padx=5, pady=5)
        columna_y_combo.set("Selecciona la columna Y")
        
        # Botón para graficar
        graficar_button = Button(frame_columnas, text="Graficar", command=graficar_datos)
        graficar_button.grid(column=3, row=0, columnspan=2, pady=10)
    else:
        messagebox.showerror("Error", "No se encontraron columnas para graficar.")

def guardar_grafica(formato): 
    """
    Muestra un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo 
    donde se guardará la gráfica actual, y la guarda en el formato especificado por el usuario.

    Esta función permite al usuario elegir dónde guardar la gráfica generada en la aplicación, 
    especificando el formato de archivo en el que desea guardarla. La gráfica se guarda utilizando 
    la figura de matplotlib (`fig`) y el formato especificado. Si el usuario selecciona una ubicación 
    y un nombre de archivo, la gráfica se guarda en ese archivo.

    Parámetros
    ----------
    formato : str
        El formato en el que se desea guardar la gráfica (por ejemplo, "png", "jpg", "pdf").

    Variables globales
    ------------------
    fig : matplotlib.figure.Figure
        La figura de matplotlib que contiene la gráfica que se va a guardar.

    Retorna
    -------
    None: La función no retorna ningún valor. Solo guarda la gráfica en el archivo especificado.

    Uso
    ---
    Esta función es útil para guardar una copia de la gráfica generada en la aplicación en el formato deseado 
    por el usuario.
    """
    archivo = filedialog.asksaveasfilename(defaultextension=f".{formato}",
                                           filetypes=[(f"{formato.upper()} files", f"*.{formato}"),
                                                      ("All files", "*.*")])

    if archivo:
        fig.savefig(archivo, format=formato)
        print(f"Gráfica guardada como {archivo}")

def graficar_datos():
    """
    Dibuja o actualiza la gráfica de datos en el canvas de Matplotlib dentro de la interfaz gráfica. 
    La función limpia la gráfica anterior, dibuja una nueva basada en los datos actuales y actualiza 
    los títulos y límites de los ejes según las selecciones del usuario.

    Esta función se encarga de graficar los datos seleccionados por el usuario para los ejes X e Y. 
    Verifica que las columnas seleccionadas sean válidas y numéricas, luego crea una nueva gráfica 
    con los datos correspondientes, ajustando los límites de los ejes y el formato de la gráfica 
    según las configuraciones de la interfaz.

    Variables globales
    ------------------
    ax : matplotlib.axes.Axes
        El objeto de los ejes en los que se dibuja la gráfica.
    canvas : FigureCanvasTkAgg
        El widget de Matplotlib que renderiza la gráfica en la interfaz gráfica de usuario.
    x : numpy.ndarray
        El arreglo de valores en el eje X que serán graficados.
    y : numpy.ndarray
        El arreglo de valores en el eje Y que serán graficados.
    x_limits : list
        Lista que contiene los límites actuales del eje 'x' en la forma [xmin, xmax].
    y_limits : list
        Lista que contiene los límites actuales del eje 'y' en la forma [ymin, ymax].
    titulo_grafica : tkinter.StringVar
        Variable que almacena el texto del título de la gráfica, el cual puede ser editado por el usuario.
    titulo_eje_x : tkinter.StringVar
        Variable que almacena el texto del título del eje X, editable por el usuario.
    titulo_eje_y : tkinter.StringVar
        Variable que almacena el texto del título del eje Y, editable por el usuario.

    Retorna
    -------
    None
        No retorna ningún valor. Solo actualiza la gráfica en el canvas y los elementos de la interfaz.

    Errores
    -------
    Muestra un mensaje de error si las columnas seleccionadas no son válidas o no son numéricas.

    Uso
    ---
    Esta función se utiliza para graficar los datos seleccionados por el usuario desde el archivo cargado 
    y ajustar los títulos y límites de los ejes en la gráfica.
    """
    
    x_col = columna_x.get()
    y_col = columna_y.get()

    global origx_lim, origy_lim, x_limits, y_limits

    if x_col not in data.columns or y_col not in data.columns:
        messagebox.showerror("Error", "Una o ambas columnas seleccionadas no son válidas.")
        return

    if not pd.api.types.is_numeric_dtype(data[x_col]) or not pd.api.types.is_numeric_dtype(data[y_col]):
        messagebox.showerror("Error", "Las columnas seleccionadas deben ser numéricas.")
        return
        
    datos_x = data[x_col]
    datos_y = data[y_col]

    # Restablecer límites originales si es la primera vez que se grafican
    if origx_lim is None or origy_lim is None:
        origx_lim = [datos_x.min(), datos_x.max()]
        origy_lim = [datos_y.min(), datos_y.max()]
        x_limits = origx_lim.copy()
        y_limits = origy_lim.copy()

    # Restablecer límites automáticamente según los datos actuales
    x_limits = [datos_x.min(), datos_x.max()]
    y_limits = [datos_y.min(), datos_y.max()]

    # Actualizar títulos de los ejes con los nombres de las columnas seleccionadas
    ejex_titulo.set(x_col)
    ejey_titulo.set(y_col)
    
    ax.clear()

    x = data[x_col]  # Usar la columna seleccionada para X
    y = data[y_col]  # Usar la columna seleccionada para Y
    line, = ax.plot(x, y, color=line_color, marker=marker_type, markersize=point_size, markerfacecolor=marker_color, linewidth=line_width, label="Datos")
    ax.set_xlim(x_limits)  # Límites del eje X
    ax.set_ylim(y_limits)  # Límites del eje Y
    ax.set_title(titulo_grafica.get(), fontname=title_fuente, fontsize=title_size)  # Actualizar título
    ax.set_xlabel(ejex_titulo.get(), fontname=ejex_shape, fontsize=ejex_size)  # Actualizar título eje X    
    ax.set_ylabel(ejey_titulo.get(), fontname=ejey_shape, fontsize=ejey_size)  # Actualizar título eje Y
    ax.grid(show_grid)
    ax.set_facecolor(bg_color)

    # Se grafican las regresiones realizadas anteriormente
    if 'regresiones' in globals() and regresiones:
        for reg in regresiones:
            ax.plot(
                reg['x_vals'], reg['y_vals'],
                label=reg['label'],
                color=reg.get('color', 'blue'),
                linewidth=reg.get('line_width', 1.0),
                marker=reg.get('marker_type', 'o'),
                markersize=reg.get('point_size', 5),
                markerfacecolor=reg.get('marker_color', 'blue')
            )
    
    ax.legend()

    canvas.draw()  # Actualizar la gráfica

    # canvas.mpl_connect('button_press_event', on_double_click)
    
    # Crear botón "+" para edición de límites eje X
    x_plus_button = Button(raiz, text="+", command=lambda: update_x_limits(raiz))
    x_plus_button.place(x=canvas.get_tk_widget().winfo_width() - 60, y=canvas.get_tk_widget().winfo_height() / 2 + 185)

    # Crear botón "+" para edición de límites eje Y
    y_plus_button = Button(raiz, text="+", command=lambda: update_y_limits(raiz))
    y_plus_button.place(x=canvas.get_tk_widget().winfo_width() - 60, y=canvas.get_tk_widget().winfo_height() / 2 - 185)

def update_graph_property(property_type=None, new_value=None):
    """
    Actualiza las propiedades visuales de la gráfica según el tipo de propiedad y el nuevo valor proporcionado. 
    La función ajusta el estilo de la línea, el marcador, el color de fondo, el tamaño de los puntos, 
    y la visibilidad de la cuadrícula, y actualiza la gráfica para reflejar los cambios.

    Parámetros
    ----------
    property_type : str, opcional
        El tipo de propiedad que se desea actualizar. Puede ser uno de los siguientes:
        - 'line_width': El grosor de la línea de la gráfica.
        - 'marker_type': El tipo de marcador utilizado en los puntos de la gráfica (ej. 'o', 's', 'x').
        - 'line_color': El color de la línea de la gráfica.
        - 'marker_color': El color de los marcadores de la gráfica.
        - 'bg_color': El color de fondo del área de la gráfica.
        - 'point_size': El tamaño de los puntos o marcadores en la gráfica.
        - 'grid': Un valor booleano que indica si la cuadrícula debe ser visible o no.

    new_value : float, str o bool, opcional
        El nuevo valor que se asignará a la propiedad seleccionada. Dependiendo de la propiedad, puede ser:
        - Un valor de tipo float (para grosor de línea o tamaño de punto),
        - Un valor de tipo str (para el tipo de marcador o color),
        - Un valor booleano (para la visibilidad de la cuadrícula).

    Variables globales
    ------------------
    line_width : float
        Grosor de la línea de la gráfica.
    marker_type : str
        Tipo de marcador que se utiliza en la gráfica.
    line_color : str
        Color de la línea de la gráfica.
    marker_color : str
        Color del marcador de la gráfica.
    bg_color : str
        Color de fondo del área de la gráfica.
    point_size : float
        Tamaño de los puntos o marcadores en la gráfica.
    show_grid : bool
        Indica si la cuadrícula de la gráfica está visible o no.
    ax : matplotlib.axes._axes.Axes
        El objeto de ejes de matplotlib donde se configura el color de fondo y la cuadrícula.
    canvas : matplotlib.backends.backend_tkagg.FigureCanvasTkAgg
        Canvas que contiene la gráfica y permite la actualización de eventos.
    line : matplotlib.lines.Line2D
        Línea de la gráfica que permite asociar eventos de clic.
    """
    global line_width, marker_type, line_color, marker_color, bg_color, point_size, show_grid

    if property_type == 'line_width':
        line_width = float(new_value)
    elif property_type == 'marker_type':
        marker_type = new_value
    elif property_type == 'line_color':
        line_color = colorchooser.askcolor()[1]
    elif property_type == 'marker_color':
        marker_color = colorchooser.askcolor()[1]
    elif property_type == 'bg_color':
        bg_color = colorchooser.askcolor()[1]
        ax.set_facecolor(bg_color)
    elif property_type == 'point_size':
        point_size = float(new_value)
    elif property_type == 'grid':
        show_grid = bool(new_value)
        ax.grid(show_grid)

    graficar_datos()  

def grafica_ventana(master):
    """
    Crea una ventana emergente para la personalización visual de la gráfica, permitiendo 
    al usuario ajustar parámetros como el color de fondo, grosor de la línea, tipo de 
    marcador, color y tamaño de puntos, y mostrar o ocultar la cuadrícula.

    Parámetros
    ----------
    master : Tkinter.Tk
        Ventana principal de la aplicación.

    Variables globales
    ------------------
    personalizacion_ventana : Tkinter.Toplevel
        Referencia a la ventana emergente de personalización, para evitar crear 
        múltiples instancias y poder acceder a sus elementos.
    show_grid : bool
        Valor booleano que indica si la cuadrícula de la gráfica está visible.
    line_width : float
        Grosor actual de la línea de la gráfica.
    marker_type : str
        Tipo de marcador utilizado en la gráfica.
    point_size : float
        Tamaño actual de los puntos en la gráfica.
    """
    global personalizacion_ventana

    if personalizacion_ventana is not None and personalizacion_ventana.winfo_exists():
        personalizacion_ventana.lift()
        return  

    personalizacion_ventana = Toplevel(master)
    personalizacion_ventana.title("Personalización de Gráfica")
    personalizacion_ventana.geometry("400x400")

    Label(personalizacion_ventana, text="Fondo", font=("Arial", 12, "bold")).pack(pady=10)
    Button(personalizacion_ventana, text="Color de Fondo", command=lambda: update_graph_property('bg_color')).pack(pady=5)

    grid_var = IntVar(value=int(show_grid))  # Inicializar con el valor actual
    Checkbutton(personalizacion_ventana, text="Mostrar Grilla", variable=grid_var, command=lambda: update_graph_property('grid', grid_var.get())).pack(pady=5)

    frame = Frame(personalizacion_ventana)
    frame.pack(pady=10)

    linea_frame = Frame(frame)
    linea_frame.grid(row=0, column=0, padx=20)

    Label(linea_frame, text="Línea", font=("Arial", 12, "bold")).pack(pady=10)

    Button(linea_frame, text="Color de Línea", command=lambda: update_graph_property('line_color')).pack(pady=5)

    Label(linea_frame, text="Tamaño de Línea:").pack(pady=5)
    line_width_slider = Scale(linea_frame, from_=0.5, to=10, resolution=0.1, orient=HORIZONTAL, command=lambda value: update_graph_property('line_width', value))
    line_width_slider.set(line_width)
    line_width_slider.pack(pady=5)

    puntos_frame = Frame(frame)
    puntos_frame.grid(row=0, column=1, padx=20)

    Label(puntos_frame, text="Puntos", font=("Arial", 12, "bold")).pack(pady=10)

    Label(puntos_frame, text="Tipo de Marcador:").pack()
    marker_options = ['o', 'x', '^', 's', '*']  
    marker_var = StringVar(value=marker_type)
    marker_menu = ttk.Combobox(puntos_frame, textvariable=marker_var, values=marker_options)
    marker_menu.pack(pady=5)
    marker_menu.bind("<<ComboboxSelected>>", lambda event: update_graph_property('marker_type', marker_var.get()))

    Button(puntos_frame, text="Color de Puntos", command=lambda: update_graph_property('marker_color')).pack(pady=5)

    Label(puntos_frame, text="Tamaño de Puntos:").pack(pady=5)
    point_size_slider = Scale(puntos_frame, from_=1, to=20, resolution=1, orient=HORIZONTAL, command=lambda value: update_graph_property('point_size', value))
    point_size_slider.set(point_size)
    point_size_slider.pack(pady=5)
    
    # Actualizar para obtener las dimensiones de la ventana emergente
    personalizacion_ventana.update_idletasks()

    centrar_ventana(raiz, personalizacion_ventana)

    # Hacer que la ventana emergente sea modal
    personalizacion_ventana.transient(raiz)
    personalizacion_ventana.grab_release()

def graficar_regresion(tipo):
    """
    Grafica la regresión especificada según el tipo proporcionado para los datos cargados en la aplicación.

    Parámetros:
    ----------
    tipo : str
        El tipo de regresión a realizar. Puede ser 'lineal', 'polinomial' o 'interpolacion'.

    Funcionalidad:
    --------------
    Esta función toma los nombres de las columnas `x` e `y` seleccionadas para realizar la regresión.
    Si no se han cargado datos, muestra un mensaje de error utilizando `messagebox.showerror`.
    Luego, crea una instancia de la clase `RegressionAnalysis` usando el conjunto de datos cargados (`data`).
    
    Dependiendo del valor del argumento `tipo`, llama a la función correspondiente para calcular la regresión:
    - `linear_regression` para regresión lineal.
    - `polynomial_regression` para regresión polinómica.
    - `interpolation` para realizar una interpolación.

    Los métodos de regresión devuelven los valores `x_vals`, `y_vals` y la ecuación de la línea ajustada.
    Los resultados de la regresión se guardan en una lista global `regresiones` con las siguientes propiedades:
    - `x_vals` y `y_vals` son los puntos calculados para la gráfica.
    - `label` etiqueta la línea de regresión con el tipo correspondiente.
    - `color`, `line_width`, `marker_type`, `marker_color`, y `point_size` definen la apariencia de la línea y los puntos.

    La función no retorna ningún valor explícito.

    Notas:
    ------
    - La variable global `data` debe estar cargada antes de llamar a esta función.
    - La variable global `regresiones` es utilizada para almacenar múltiples regresiones.
    - Se espera que `RegressionAnalysis` sea una clase que implemente los métodos `linear_regression`, `polynomial_regression` e `interpolation`.
    
    Excepciones:
    ------------
    Muestra un mensaje de error si no hay datos cargados para las columnas `x` e `y`.

    Ejemplo de uso:
    ---------------
    graficar_regresion('lineal')  # Realiza y grafica una regresión lineal
    """
    global regresiones
    
    x_col = columna_x.get()
    y_col = columna_y.get()

    if x_col is None or y_col is None:
        messagebox.showerror("Error", "No hay datos cargados para realizar la regresión.")
        return

    # Crear la instancia de RegressionAnalysis pasando el DataFrame directamente
    reg_analysis = RegressionAnalysis(data)

    if tipo == 'lineal':
        # Llamar a la función linear_regression con return_metrics=False
        x_vals, y_vals, ecuacion = reg_analysis.linear_regression(x_col, y_col, ax1=ax, return_metrics=False)
    elif tipo == 'polinomial':
        x_vals, y_vals, ecuacion = reg_analysis.polynomial_regression(x_col, y_col, ax1=ax, return_metrics=False)
    elif tipo == 'interpolacion':
        x_vals, y_vals, ecuacion = reg_analysis.interpolation(x_col, y_col, ax1=ax, return_metrics=False)

    # Guardar los datos de la regresión
    regresiones.append({
    'x_vals': x_vals,
    'y_vals': y_vals,
    'label': f"Regresión {tipo.capitalize()}",  
    'color': 'red',  
    'line_width': 1.0,
    'marker_type': 'o',
    'marker_color': 'red',
    'point_size': 5
    })

def update_regresion_property(regresion, property_type, new_value=None):
    """
    Actualiza las propiedades visuales de una línea de regresión y actualiza la gráfica.

    Parametros
    ----------
    regresion : dict
        Diccionario que contiene los datos y propiedades visuales de la regresión.
    property_type : str
        Tipo de propiedad a modificar ('line_color', 'line_width', 'marker_type', 'marker_color', 'point_size').
    new_value : any, opcional
        Nuevo valor para la propiedad especificada. Si no se proporciona, se abre un cuadro de diálogo
        para seleccionar el color.
    """
    if property_type == 'line_color':
        regresion['color'] = colorchooser.askcolor()[1]
    elif property_type == 'line_width':
        regresion['line_width'] = new_value
    elif property_type == 'marker_type':
        regresion['marker_type'] = new_value
    elif property_type == 'marker_color':
        regresion['marker_color'] = colorchooser.askcolor()[1]
    elif property_type == 'point_size':
        regresion['point_size'] = new_value

    # Redibujar la gráfica
    graficar_datos()

def grafica_ventana_regresion(master, tipo):
    """
    Crea una ventana emergente para personalizar visualmente las líneas de regresión.
    Esta ventana permite cambiar propiedades como color, grosor de línea y tipo de marcador
    para la línea de regresión seleccionada.

    Parametros
    ----------
    master : tkinter.Tk
        Ventana principal de la aplicación.
    tipo_regresion : str
        Tipo de regresión que se está personalizando ('lineal', 'polinomial', 'interpolacion').

    Variables globales
    ------------------
    regresiones : list
        Lista que contiene las regresiones realizadas, con sus datos y propiedades visuales.
    """
    global personalizacion_ventana

    if personalizacion_ventana is not None and personalizacion_ventana.winfo_exists():
        personalizacion_ventana.lift()
        return  

    personalizacion_ventana = Toplevel(master)
    personalizacion_ventana.title(f"Personalización de Regresión {tipo.capitalize()}")
    personalizacion_ventana.geometry("400x400")


    regresion = next(
        (reg for reg in regresiones if tipo.strip().lower() in reg['label'].strip().lower()), 
    None
    )

    if regresion is None:
        messagebox.showerror("Error", f"No se encontró una regresión del tipo {tipo}.")
        personalizacion_ventana.destroy()
        return
        

    # Botón para cambiar el color de la línea
    Button(personalizacion_ventana, text="Color de Línea", 
           command=lambda: update_regresion_property(regresion, 'line_color')).pack(pady=10)

    # Slider para cambiar el grosor de la línea
    Label(personalizacion_ventana, text="Grosor de Línea:").pack(pady=5)
    line_width_slider = Scale(personalizacion_ventana, from_=0.5, to=10, resolution=0.1, orient=HORIZONTAL, 
                              command=lambda value: update_regresion_property(regresion, 'line_width', float(value)))
    line_width_slider.set(regresion.get('line_width', 1.0))
    line_width_slider.pack(pady=5)

    # Combobox para cambiar el tipo de marcador
    Label(personalizacion_ventana, text="Tipo de Marcador:").pack(pady=5)
    marker_options = ['o', 'x', '^', 's', '*']  
    marker_var = StringVar(value=regresion.get('marker_type', 'o'))
    marker_menu = ttk.Combobox(personalizacion_ventana, textvariable=marker_var, values=marker_options)
    marker_menu.pack(pady=5)
    marker_menu.bind("<<ComboboxSelected>>", 
                     lambda event: update_regresion_property(regresion, 'marker_type', marker_var.get()))

    # Botón para cambiar el color del marcador
    Button(personalizacion_ventana, text="Color del Marcador", 
           command=lambda: update_regresion_property(regresion, 'marker_color')).pack(pady=10)

    # Slider para cambiar el tamaño del marcador
    Label(personalizacion_ventana, text="Tamaño del Marcador:").pack(pady=5)
    point_size_slider = Scale(personalizacion_ventana, from_=1, to=20, resolution=1, orient=HORIZONTAL, 
                              command=lambda value: update_regresion_property(regresion, 'point_size', float(value)))
    point_size_slider.set(regresion.get('point_size', 5))
    point_size_slider.pack(pady=5)

    # Centrar la ventana
    personalizacion_ventana.update_idletasks()
    centrar_ventana(raiz, personalizacion_ventana)

    # Hacer que la ventana emergente sea modal
    personalizacion_ventana.transient(raiz)
    personalizacion_ventana.grab_release()


def apply_title_changes(title_size_var, title_fuente_var, titulo_grafica_entry):
    """
    Aplica los cambios en el título de la gráfica, incluyendo el texto, tamaño de fuente 
    y estilo de fuente, de acuerdo a los valores seleccionados por el usuario.

    Parámetros
    ----------
    title_size_var : tkinter.IntVar
        Variable del tamaño de la fuente del título de la gráfica.
    title_fuente_var : tkinter.StringVar
        Variable del estilo de fuente del título de la gráfica.
    titulo_grafica_entry : tkinter.Entry
        Campo de entrada del nuevo texto para el título de la gráfica.

    Variables globales
    ------------------
    title_size : int
        Tamaño de la fuente del título de la gráfica.
    title_fuente : str
        Estilo de la fuente utilizado para el título de la gráfica.
    titulo_grafica : tkinter.StringVar
        Variable de texto para el título de la gráfica, que almacena el valor actual y el nuevo título.
    """
    global title_size, title_fuente, titulo_grafica
    titulo_grafica.set(titulo_grafica_entry.get()) 
    
    # Obtener valores seleccionados
    title_size = int(title_size_var.get())
    title_fuente = title_fuente_var.get()
    
    # Actualizar el título de la gráfica
    ax.set_title(titulo_grafica.get(), fontsize=title_size, fontname=title_fuente)
    canvas.draw()

def grafica_ventana_title(master):
    """
    Abre una ventana emergente que permite al usuario personalizar el título de la gráfica, 
    incluyendo el texto, tamaño de la fuente y el estilo de la fuente.

    Parámetros
    ----------
    master : 
        Ventana principal de la aplicación.
    
    Variables globales
    ------------------
    personal_ventana_title : tkinter.Toplevel
        Ventana emergente de personalización del título de la gráfica.
    titulo_grafica : tkinter.StringVar
        Variable del título actual de la gráfica.
    """
    global personal_ventana_title
    
    # Verificar si la ventana ya está abierta
    if personal_ventana_title is not None and personal_ventana_title.winfo_exists():
        personal_ventana_title.lift()  # Lleva la ventana al frente
        return  # No abrir otra ventana

    # Crear nueva ventana
    personal_ventana_title = Toplevel(master)
    personal_ventana_title.title("Personalización de Título")
    personal_ventana_title.geometry("300x250")
    
    # Nombre del Título
    Label(personal_ventana_title, text="Ingrese el Título:").pack(pady=10)
    titulo_grafica_entry = Entry(personal_ventana_title)
    titulo_grafica_entry.insert(0, titulo_grafica.get())  # Mostrar el título actual
    titulo_grafica_entry.pack(pady=5)
    
    # Selección del tamaño de letra (8,10,12,...)
    Label(personal_ventana_title, text="Tamaño de la letra:").pack()
    title_size_options = [8, 10, 12, 14, 16, 18, 20]  # Tamaños de letra disponibles
    title_size_var = StringVar(value=str(title_size))  # Valor actual del tamaño
    
    # Crear un Combobox para seleccionar el tamaño de letra
    title_size_combobox = ttk.Combobox(personal_ventana_title, textvariable=title_size_var, values=title_size_options)
    title_size_combobox.pack(pady=5)
    
    # Selección de la fuente
    Label(personal_ventana_title, text="Fuente de la letra:").pack()
    title_fuente_options = ['Liberation Serif', 'DejaVu Serif']  # Fuentes disponibles (depende del usuario)
    title_fuente_var = StringVar(value=title_fuente)  # Valor actual de la fuente
    
    # Crear un Combobox para seleccionar la fuente
    title_fuente_combobox = ttk.Combobox(personal_ventana_title, textvariable=title_fuente_var, values=title_fuente_options)
    title_fuente_combobox.pack(pady=5)
    
    # Botón para aplicar los cambios
    Button(personal_ventana_title, text="Aplicar Cambios", 
           command=lambda: apply_title_changes(title_size_var, title_fuente_var, titulo_grafica_entry)).pack(pady=10)

    # Actualizar para obtener las dimensiones de la ventana emergente
    personal_ventana_title.update_idletasks()

    centrar_ventana(raiz, personal_ventana_title)

    # Hacer que la ventana emergente sea modal
    personal_ventana_title.transient(raiz)
    personal_ventana_title.grab_set()
    raiz.wait_window(personal_ventana_title)

def apply_xaxis_changes(ejex_size_var, ejex_fuente_var, ejex_titulo_entry):
    """
    Aplica los cambios en el título del eje X de la gráfica, incluyendo el texto, tamaño de fuente 
    y estilo de fuente, de acuerdo a los valores seleccionados por el usuario.

    Parámetros
    ----------
    ejex_size_var : tkinter.IntVar
        Variable vinculada al tamaño de la fuente del título del eje X.
    ejex_fuente_var : tkinter.StringVar
        Variable vinculada al estilo de fuente del título del eje X.
    ejex_titulo_entry : tkinter.Entry
        Campo de entrada que contiene el nuevo texto para el título del eje X.

    Variables globales
    ------------------
    ejex_size : int
        Tamaño de la fuente del título del eje X.
    ejex_shape : str
        Estilo de la fuente utilizado para el título del eje X.
    ejex_titulo : tkinter.StringVar
        Variable de texto para el título del eje X, que almacena el valor actual y el nuevo título.
    """
    global ejex_size, ejex_shape, ejex_titulo
    ejex_titulo.set(ejex_titulo_entry.get())  # Obtener el nuevo título del eje X    
    # Obtener valores seleccionados
    ejex_size = int(ejex_size_var.get())
    ejex_shape = ejex_fuente_var.get()
    
    # Actualizar el título del eje X de la gráfica
    ax.set_xlabel(ejex_titulo.get(), fontsize=ejex_size, fontname=ejex_shape)
    
    # Redibujar la gráfica
    canvas.draw()

def grafica_ventana_ejex(master):
    """
    Abre una ventana emergente que permite al usuario personalizar el título del eje X de la gráfica.
    El usuario puede modificar el texto, el tamaño de la fuente y el estilo de la fuente del eje X.

    Parámetros
    ----------
    master : 
        La ventana principal desde la que se abrirá la ventana emergente de personalización.

    Variables globales
    ------------------
    ventana_ejex : tkinter.Toplevel
        Ventana emergente de personalización del eje X.
    ejex_titulo : tkinter.StringVar
        Variable de texto del título actual del eje X.
    ejex_size : int
        Tamaño de la fuente del título del eje X.
    ejex_shape : str
        Estilo de la fuente utilizada para el título del eje X.
    """
    global ventana_ejex
    
    # Verificar si la ventana ya está abierta
    if ventana_ejex is not None and ventana_ejex.winfo_exists():
        ventana_ejex.lift()  # Lleva la ventana al frente
        return  # No abrir otra ventana

    # Crear nueva ventana
    ventana_ejex = Toplevel(master)
    ventana_ejex.title("Personalización Eje x")
    ventana_ejex.geometry("300x250")
    
    # Nombre del Título
    Label(ventana_ejex, text="Ingrese Eje x:").pack(pady=10)
    titulo_ejex_var = Entry(ventana_ejex)
    titulo_ejex_var.insert(0, ejex_titulo.get())  # Mostrar el título actual
    titulo_ejex_var.pack(pady=5)
    
    # Selección del tamaño de letra (8,10,12,...)
    Label(ventana_ejex, text="Tamaño de la letra:").pack()
    ejex_size_options = [8, 10, 12, 14, 16, 18, 20]  # Tamaños de letra disponibles
    ejex_size_var = StringVar(value=str(ejex_size))  # Valor actual del tamaño
    
    # Crear un Combobox para seleccionar el tamaño de letra
    ejex_size_combobox = ttk.Combobox(ventana_ejex, textvariable=ejex_size_var, values=ejex_size_options)
    ejex_size_combobox.pack(pady=5)
    
    # Selección de la fuente
    Label(ventana_ejex, text="Fuente de la letra:").pack()
    ejex_fuente_options = ['Liberation Serif', 'DejaVu Serif']  # Fuentes disponibles (depende del usuario)
    ejex_fuente_var = StringVar(value=ejex_shape)  # Valor actual de la fuente
    
    # Crear un Combobox para seleccionar la fuente
    ejex_fuente_combobox = ttk.Combobox(ventana_ejex, textvariable=ejex_fuente_var, values=ejex_fuente_options)
    ejex_fuente_combobox.pack(pady=5)
    
    # Botón para aplicar los cambios
    Button(ventana_ejex, text="Aplicar Cambios", 
           command=lambda: apply_xaxis_changes(ejex_size_var, ejex_fuente_var,titulo_ejex_var)).pack(pady=10)

    # Actualizar para obtener las dimensiones de la ventana emergente
    ventana_ejex.update_idletasks()

    centrar_ventana(raiz, ventana_ejex)

    # Hacer que la ventana emergente sea modal
    ventana_ejex.transient(raiz)
    ventana_ejex.grab_set()
    raiz.wait_window(ventana_ejex)

def apply_yaxis_changes(ejey_size_var, ejey_fuente_var, ejey_titulo_entry):
    """
    Aplica los cambios de personalización al título del eje Y de la gráfica, como el tamaño y el tipo de fuente.

    Parámetros
    ----------
    ejey_size_var : tkinter.StringVar
        Variable del tamaño de la fuente para el título del eje Y.
    ejey_fuente_var : tkinter.StringVar
        Variable de la fuente seleccionada para el título del eje Y.
    ejey_titulo_entry : tkinter.Entry
        Campo de texto donde se ingresa el nuevo título del eje Y.

    Variables globales
    ------------------
    ejey_size : int
        Tamaño de la fuente para el título del eje Y.
    ejey_shape : str
        Tipo de fuente para el título del eje Y.
    ejey_titulo : tkinter.StringVar
        Variable de texto que contiene el título del eje Y.
    """
    global ejey_size, ejey_shape, ejey_titulo
    ejey_titulo.set(ejey_titulo_entry.get())  # Obtener el nuevo título del eje X    
    # Obtener valores seleccionados
    ejey_size = int(ejey_size_var.get())
    ejey_shape = ejey_fuente_var.get()
    
    # Actualizar el título del eje X de la gráfica
    ax.set_ylabel(ejey_titulo.get(), fontsize=ejey_size, fontname=ejey_shape)
    
    # Redibujar la gráfica
    canvas.draw()

def grafica_ventana_ejey(master):
    """
    Abre una ventana emergente para personalizar el título del eje Y de la gráfica, 
    permitiendo modificar el texto, el tamaño de la fuente y la fuente de la letra.

    Parámetros
    ----------
    master : tkinter.Tk
        Ventana principal de la aplicación.

    Variables globales
    ------------------
    ventana_ejey : tkinter.Toplevel
        La ventana emergente de personalización del eje Y.
    ejey_titulo : tkinter.StringVar
        Variable del título del eje Y de la gráfica.
    ejey_size : int
        Tamaño de la fuente para el título del eje Y.
    ejey_shape : str
        Tipo de fuente para el título del eje Y.
    """
    global ventana_ejey
    
    # Verificar si la ventana ya está abierta
    if ventana_ejey is not None and ventana_ejey.winfo_exists():
        ventana_ejey.lift()  # Lleva la ventana al frente
        return  # No abrir otra ventana

    # Crear nueva ventana
    ventana_ejey = Toplevel(master)
    ventana_ejey.title("Personalización Eje y")
    ventana_ejey.geometry("300x250")
    
    # Nombre del Título
    Label(ventana_ejey, text="Ingrese Eje y:").pack(pady=10)
    titulo_ejey_var = Entry(ventana_ejey)
    titulo_ejey_var.insert(0, ejey_titulo.get())  # Mostrar el título actual
    titulo_ejey_var.pack(pady=5)
    
    # Selección del tamaño de letra (8,10,12,...)
    Label(ventana_ejey, text="Tamaño de la letra:").pack()
    ejey_size_options = [8, 10, 12, 14, 16, 18, 20]  # Tamaños de letra disponibles
    ejey_size_var = StringVar(value=str(ejey_size))  # Valor actual del tamaño
    
    # Crear un Combobox para seleccionar el tamaño de letra
    ejey_size_combobox = ttk.Combobox(ventana_ejey, textvariable=ejey_size_var, values=ejey_size_options)
    ejey_size_combobox.pack(pady=5)
    
    # Selección de la fuente
    Label(ventana_ejey, text="Fuente de la letra:").pack()
    ejey_fuente_options = ['Liberation Serif', 'DejaVu Serif']  # Fuentes disponibles (depende del usuario)
    ejey_fuente_var = StringVar(value=ejey_shape)  # Valor actual de la fuente
    
    # Crear un Combobox para seleccionar la fuente
    ejey_fuente_combobox = ttk.Combobox(ventana_ejey, textvariable=ejey_fuente_var, values=ejey_fuente_options)
    ejey_fuente_combobox.pack(pady=5)
    
    # Botón para aplicar los cambios
    Button(ventana_ejey, text="Aplicar Cambios", 
           command=lambda: apply_yaxis_changes(ejey_size_var, ejey_fuente_var,titulo_ejey_var)).pack(pady=10)

    # Actualizar para obtener las dimensiones de la ventana emergente
    ventana_ejey.update_idletasks()

    centrar_ventana(raiz, ventana_ejey)

    # Hacer que la ventana emergente sea modal
    ventana_ejey.transient(raiz)
    ventana_ejey.grab_set()
    raiz.wait_window(ventana_ejey)
    
def on_double_click(event):
    """
    Detecta un doble clic en los títulos de la gráfica (título principal, título del eje X o título del eje Y) 
    y abre la ventana de edición correspondiente para personalizar el título del eje o gráfico.

    Parámetros
    ----------
    event : matplotlib.backend_bases.MouseEvent
        El evento de clic que contiene la información sobre la posición del clic y si es un doble clic.
    
    Variables globales
    ------------------
    raiz : tkinter.Tk
        La ventana principal de la aplicación.
    """
    if event.dblclick:
        # Coordenadas del clic en la ventana gráfica
        x, y = event.x, event.y

        # Obtener la posición del título
        bbox_title = ax.title.get_window_extent(canvas.get_renderer())
        bbox_xlabel = ax.xaxis.label.get_window_extent(canvas.get_renderer())
        bbox_ylabel = ax.yaxis.label.get_window_extent(canvas.get_renderer())

        # Comprobar si el clic fue en el título de la gráfica
        if bbox_title.contains(x, y):
            grafica_ventana_title(raiz)  # Usar la ventana principal 'raiz' para abrir la personalización
        # Comprobar si el clic fue en el título de la gráfica
        elif bbox_xlabel.contains(x, y):
            grafica_ventana_ejex(raiz)
        # Comprobar si el clic fue hecho en Eje y
        elif bbox_ylabel.contains(x,y):
            grafica_ventana_ejey(raiz)

# Conectar evento de doble clic
canvas.mpl_connect('button_press_event', on_double_click)

def update_x_limits(master):
    """
    Muestra una ventana emergente para actualizar los límites del eje X de la gráfica.

    Parámetros
    ----------
    master : tkinter.Tk
        La ventana principal de la aplicación.

    Variables globales
    ------------------
    ventana_lim_x : tkinter.Toplevel
        La ventana emergente creada para la actualización de los límites del eje X.
    """
    global ventana_lim_x

    # Obtener las columnas seleccionadas
    columna_x_seleccionada = columna_x.get()
        
    # Obtener los datos de la columna seleccionada
    datos_x = data[columna_x_seleccionada]
    
    # Valores predeterminados 
    x_min_datos = datos_x.min()
    x_max_datos = datos_x.max()

    # Crear nueva ventana
    ventana_lim_x = Toplevel(master)
    ventana_lim_x.title("Límites Eje X")
    ventana_lim_x.geometry("300x250")

    # Etiquetas y campos de entrada para x_min y x_max
    Label(ventana_lim_x, text="Ingrese x_min:").pack(pady=5)
    x_min_entry = Entry(ventana_lim_x)
    x_min_entry.insert(0, str(x_min_datos))  # Valor de x_min
    x_min_entry.pack()

    Label(ventana_lim_x, text="Ingrese x_max:").pack(pady=5)
    x_max_entry = Entry(ventana_lim_x)
    x_max_entry.insert(0, str(x_max_datos))  # Valor de x_max
    x_max_entry.pack()

    # Botón para actualizar los límites de X
    Button(ventana_lim_x, text="Actualizar Límites", command=lambda: set_x_limits(x_min_entry, x_max_entry)).pack(pady=10)

    # Actualizar para obtener las dimensiones de la ventana emergente
    ventana_lim_x.update_idletasks()

    centrar_ventana(raiz, ventana_lim_x)

    # Hacer que la ventana emergente sea modal
    ventana_lim_x.transient(raiz)
    ventana_lim_x.grab_set()
    raiz.wait_window(ventana_lim_x)

def set_x_limits(x_min_entry, x_max_entry):
    """
    Actualiza los límites del eje X según los valores ingresados por el usuario en la ventana emergente.

    Parámetros
    ----------
    x_min_entry : tkinter.Entry
        Campo de entrada dl valor para el límite inferior del eje X (x_min).

    x_max_entry : tkinter.Entry
        Campo de entrada del valor para el límite superior del eje X (x_max).

    Variables globales
    ------------------
    x_limits : list
        Lista que almacena los límites actuales del eje X [x_min, x_max].
    origx_lim : list
        Copia de los límites originales del eje X, utilizada para restaurar los valores iniciales si es necesario.
    """
    global x_limits, origx_lim

    try:
        # Obtener las columnas seleccionadas
        columna_x_seleccionada = columna_x.get()
        
        # Obtener los datos de la columna seleccionada
        datos_x = data[columna_x_seleccionada]

        # Valores predeterminados 
        x_min_datos = datos_x.min()
        x_max_datos = datos_x.max()
        
        # Validar y asignar los límites ingresados por el usuario
        x_min = float(x_min_entry.get()) if x_min_entry.get() else x_min_datos
        x_max = float(x_max_entry.get()) if x_max_entry.get() else x_max_datos
        if x_min < x_max:
            x_limits = [x_min, x_max]  # Límite actual se actualiza
            if origx_lim is None:  # Solo actualiza los límites originales si no se han definido
                origx_lim = [x_min_datos, x_max_datos]
            else:
                origx_lim = [x_min, x_max]
            print(f"Límites del eje X actualizados: {origy_lim}")
            graficar_datos()  # Redibuja la gráfica con los nuevos límites
            ventana_lim_x.destroy() # Cerrar la ventana emergente
        else:
            messagebox.showerror("Error","El valor de x_min debe ser menor que x_max.")
    except ValueError:
        messagebox.showerror("Error","Por favor, ingrese valores numéricos válidos.")

def update_y_limits(master):
    """
    Muestra una ventana emergente para actualizar los límites del eje Y.

    Parámetros
    ----------
    master : tkinter.Tk
        La ventana principal de la aplicación. Es el contenedor sobre el que se crea la ventana emergente.

    Variables globales
    ------------------
    ventana_lim_y : tkinter.Toplevel
        Ventana emergente que permite al usuario ingresar los límites del eje Y.
    """
    global ventana_lim_y

    # Obtener las columnas seleccionadas
    columna_y_seleccionada = columna_y.get()
        
    # Obtener los datos de la columna seleccionada
    datos_y = data[columna_y_seleccionada]
    
    # Valores predeterminados 
    y_min_datos = datos_y.min()
    y_max_datos = datos_y.max()


    # Crear nueva ventana
    ventana_lim_y = Toplevel(master)
    ventana_lim_y.title("Límites Eje Y")
    ventana_lim_y.geometry("300x250")

    # Etiquetas y campos de entrada para x_min y x_max
    Label(ventana_lim_y, text="Ingrese y_min:").pack(pady=5)
    y_min_entry = Entry(ventana_lim_y)
    y_min_entry.insert(0, str(y_min_datos))  # Valor de y_min
    y_min_entry.pack()

    Label(ventana_lim_y, text="Ingrese y_max:").pack(pady=5)
    y_max_entry = Entry(ventana_lim_y)
    y_max_entry.insert(0, str(y_max_datos))  # Valor de y_max
    y_max_entry.pack()

    # Botón para actualizar los límites de X
    Button(ventana_lim_y, text="Actualizar Límites", command=lambda: set_y_limits(y_min_entry, y_max_entry)).pack(pady=10)

    # Actualizar para obtener las dimensiones de la ventana emergente
    ventana_lim_y.update_idletasks()

    centrar_ventana(raiz, ventana_lim_y)

    # Hacer que la ventana emergente sea modal
    ventana_lim_y.transient(raiz)
    ventana_lim_y.grab_set()
    raiz.wait_window(ventana_lim_y)

def set_y_limits(y_min_entry, y_max_entry):
    """
    Actualiza los límites del eje Y según los valores ingresados por el usuario en la ventana emergente.

    Parámetros
    ----------
    y_min_entry : tkinter.Entry
        Campo de entrada del valor mínimo para el eje Y.

    y_max_entry : tkinter.Entry
        Campo de entrada del valor máximo para el eje Y.

    Variables globales
    ------------------
    y_limits : list
        Lista que almacena los valores actuales de los límites del eje Y [y_min, y_max].

    origy_lim : list
        Copia de los límites originales del eje Y, utilizada para restaurar los valores si es necesario.
    """
    global y_limits, origy_lim

    try:
        # Obtener las columnas seleccionadas
        columna_y_seleccionada = columna_y.get()
        
        # Obtener los datos de la columna seleccionada
        datos_y = data[columna_y_seleccionada]

        # Valores predeterminados 
        y_min_datos = datos_y.min()
        y_max_datos = datos_y.max()
        
        # Validar y asignar los límites ingresados por el usuario
        y_min = float(y_min_entry.get()) if y_min_entry.get() else y_min_datos
        y_max = float(y_max_entry.get()) if y_max_entry.get() else y_max_datos
        
        if y_min < y_max:
            y_limits = [y_min, y_max]  # Límite actual se actualiza
            if origy_lim is None:  # Solo actualiza los límites originales si no se han definido
                origy_lim = [y_min_datos, y_max_datos]
            else:
                origy_lim = [y_min, y_max]
            print(f"Límites del eje Y actualizados: {origy_lim}")
            graficar_datos()  # Redibuja la gráfica con los nuevos límites
            ventana_lim_y.destroy() # Cerrar la ventana emergente
        else:
            messagebox.showerror("Error","El valor de y_min debe ser menor que y_max.")
    except ValueError:
        messagebox.showerror("Error","Por favor, ingrese valores numéricos válidos.")

def zoom(event=None,reset=False):
    """
    Ajuste del nivel de zoom en la gráfica redibujando los ejes a partir de nuevos límites que 
    se actualizarán dependiendo de la amplificación que de el usuario. El nivel de zoom es 
    controlado por el valor de una barra deslizante [scale] y la gráfica es redibujada en 
    función de los límites ajustados. También se actualiza el porcentaje de zoom mostrado en pantalla
    [zoom_label]. Si se desea volver al tamaño original de la gráfica este se reestablecera cuando 
    [reset] sea True.

    Parámetros
    ----------
    event : tkinter.Event, optional
        Evento que dispara la acción de zoom.

    reset : bool, optional
        Si True, restablece los límites originales de la gráfica.
    
    Variables globales
    ------------------
    x_limits : list
        Lista que contiene los límites actuales del eje 'x' en la forma [xmin, xmax].
    y_limits : list
        Lista que contiene los límites actuales del eje 'y' en la forma [ymin, ymax].

    Returns
    -------
    None
        La función no retorna ningún valor, simplemente actualiza la gráfica y la interfaz de usuario.
    """
    global x_limits, y_limits, origx_lim, origy_lim # Variables globales, límites de 'x' y 'y'
    if reset:
        # Restablecer límites originales
        x_limits = origx_lim.copy()
        y_limits = origy_lim.copy()
        zoom_label.config(text="Zoom: 100%")  # Restablecer la etiqueta de zoom
        x_scale.set(0)  # Resetear la barra de zoom de X
        y_scale.set(0)  # Resetear la barra de zoom de Y
    else:
        # Obtener los valores de las barras deslizantes para cada eje
        x_zoom_level = x_scale.get()
        y_zoom_level = y_scale.get()
        
        x_mid = (origx_lim[1] + origx_lim[0]) / 2  # Punto medio 'x'
        x_zoom_factor = 1 + x_zoom_level
        x_range = (origx_lim[1] - origx_lim[0]) / x_zoom_factor
        x_limits = [x_mid - x_range / 2, x_mid + x_range / 2]
        
        y_mid = (origy_lim[1] + origy_lim[0]) / 2  # Punto medio 'y'
        y_zoom_factor = 1 + y_zoom_level
        y_range = (origy_lim[1] - origy_lim[0]) / y_zoom_factor
        y_limits = [y_mid - y_range / 2, y_mid + y_range / 2]

        # Actualizar la etiqueta de porcentaje de zoom para cada eje
        x_zoom_percentage = int((x_zoom_level / 10) * 100)
        y_zoom_percentage = int((y_zoom_level / 10) * 100)
        zoom_label.config(text=f"Zoom X: {x_zoom_percentage}% | Zoom Y: {y_zoom_percentage}%")
    
    # Actualizar los límites de la gráfica
    ax.set_xlim(x_limits)
    ax.set_ylim(y_limits)
    canvas.draw()

# Funciones para manejar el desplazamiento con el mouse sobre la gráfica
def on_press(event):
    """
    Evento que permite inicializar un evento con un clic siempre y cuando este se haya 
    realizado dentro de la gráfica, es decir, definido dentro de los límites de la definición
    para matplotlib. 

    Parámetros
    ----------
    event : matplotlib.backend_bases.MouseEvent
        Evento que contiene la información del clic del mouse dentro de los límites de la 
        gráfica y almacenando las coordenadas [x,y] del clic realizado.

    Variables globales
    ------------------
    is_dragging : bool
        Indicador que se establece en True cuando el usuario está arrastrando el mouse.
    start_x : float
        Coordenada 'x' donde se inició el clic en la gráfica.
    start_y : float
        Coordenada 'y' donde se inició el clic en la gráfica.

    Returns
    -------
    None
        La función no retorna ningún valor, simplemente actualiza datos.
    """
    global is_dragging, start_x, start_y
    if event.inaxes:
        is_dragging = True   # Interacción con la gráfica
        start_x, start_y = event.xdata, event.ydata  # Almacenamiento de datos iniciales de clic

def on_release(event):
    """
    Evento que permite finalizar la función anterior de interacción del usuario y la 
    gráfica a través del mouse. A demás, permite que la acción solo se realice siempre y 
    cuando el usuario deslice mientras hace el clic, al soltar el clic se finaliza la acción.

    Parámetros
    ----------
    event : matplotlib.backend_bases.MouseEvent
        Evento que contiene la información del clic del mouse dentro de los límites de la 
        gráfica y almacenando las coordenadas [x,y] del clic realizado.

    Variables globales
    ------------------
    is_dragging : bool
        Indicador que se establece en False cuando el usuario suelta el botón del mouse,
        lo que indica que la interacción/arrastre ha finalizado.

    Returns
    -------
    None
        La función no retorna ningún valor, simplemente actualiza datos.
    """
    global is_dragging
    is_dragging = False # Finalizar el evento de interacción al soltar el clic.

def on_motion(event):
    """
    Evento que permite desplazar la gráfica mientras el usuario interactúa/arrastra el 
    mouse, ajustando los límites de los ejes de acuerdo al desplazamiento del cursor.

    Parámetros
    ----------
    event : matplotlib.backend_bases.MouseEvent
        Evento que contiene la información del clic del mouse dentro de los límites de la 
        gráfica y almacenando las coordenadas [x,y] del clic realizado.

    Variables globales
    ------------------
    x_limits : list
        Lista que contiene los límites actuales del eje 'x' en la forma [xmin, xmax].
    y_limits : list
        Lista que contiene los límites actuales del eje 'y' en la forma [ymin, ymax].
    start_x : float
        Coordenada 'x' donde se inició el clic en la gráfica.
    start_y : float
        Coordenada 'y' donde se inició el clic en la gráfica.



    Nota:
    -----
    Este evento solo se activa si la variable global `is_dragging` es `True`, lo que 
    indica que el usuario ya ha iniciado el proceso de arrastre al presionar el botón 
    del ratón en la gráfica (evento gestionado por la función `on_press`).
    
    Nota:
    -----
    Este evento solo se activa si la variable global `is_dragging` es `True`, lo que 
    indica que el usuario ya ha iniciado el proceso de arrastre al presionar el botón 
    del ratón en la gráfica (evento gestionado por la función `on_press`).
    """
    global x_limits, y_limits, start_x, start_y, origx_lim, origy_lim
    if is_dragging and event.inaxes: # Verificación de interacción True and True
        
        # Calculo de diferencia entre el clic inicial y la posición actual del cursor
        dx = start_x - event.xdata
        dy = start_y - event.ydata
        
        # Redefinir los límites de acuerdo al desplazamiento
        x_limits = [x + dx for x in x_limits]
        y_limits = [y + dy for y in y_limits]

        # Sincronizar con los límites originales
        origx_lim = x_limits.copy()
        origy_lim = y_limits.copy()

        # Actualizar la gráfica dinámicamente
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)
        canvas.draw()

# Conectar eventos del ratón
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

# Crear frame para los controles de zoom
frame_zoom = Frame(raiz, bg="gray22")
frame_zoom.grid(row=1, column=0, padx=10, pady=10)

# Barra de zoom
style = ttk.Style()
style.configure("Horizontal.TScale", background='gray22')  # Configurar estilo para la barra

# Barra zoom eje x
x_scale = ttk.Scale(frame_zoom, to=10, from_=0, orient='horizontal', length=200, style="Horizontal.TScale", command=zoom)
x_scale.grid(column=0, row=0, padx=5)

#Barra zoom eje y
y_scale = ttk.Scale(frame_zoom, to=10, from_=0, orient='horizontal', length=200, style="Horizontal.TScale", command=zoom)
y_scale.grid(column=1, row=0, pady=5)

# Etiqueta para mostrar el porcentaje de zoom de cada eje
zoom_label = ttk.Label(frame, text="Zoom X: 0% | Zoom Y: 0%")
zoom_label.grid(column=0, row=5)

def cerrar_ventana():
    """Función que se llama al cerrar la ventana para borrar el archivo tmp_graph.pkl"""
    archivo_tmp = "tmp_graph.pkl"
    if os.path.exists(archivo_tmp):
        os.remove(archivo_tmp)
    raiz.quit()  # Esto cierra el mainloop de Tkinter

# Añadir un manejador de evento para cerrar la ventana
raiz.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Ejecutar la aplicación
if __name__ == "__main__":
    cargar_datos()
    raiz.mainloop()
