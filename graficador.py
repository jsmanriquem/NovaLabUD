# Librerías necesarias para realizar un graficador
from tkinter import Tk, Frame, Button, Label, Menu, Toplevel, StringVar, ttk, Entry, filedialog, colorchooser, Scale, HORIZONTAL , IntVar, Checkbutton
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt

# Ventana principal
raiz = Tk()
raiz.geometry("1024x780")  # Tamaño de la pantalla
raiz.config(bg="gray")  # Color de fondo
raiz.wm_title('Gráfica de datos')  # Título de la gráfica

# Menú de opciones para el usuario
barraMenu = Menu(raiz)
raiz.config(menu=barraMenu)

archivoMenu = Menu(barraMenu, tearoff=0)
archivoMenu.add_command(label="Nuevo")
archivoMenu.add_command(label="Guardar")

guardarComoMenu = Menu(archivoMenu, tearoff=0)
guardarComoMenu.add_command(label="PDF", command=lambda: guardar_grafica('pdf'))
guardarComoMenu.add_command(label="JPG", command=lambda: guardar_grafica('jpg'))
guardarComoMenu.add_command(label="PNG", command=lambda: guardar_grafica('png'))
archivoMenu.add_cascade(label="Guardar como ...", menu=guardarComoMenu)
archivoMenu.add_separator()
archivoMenu.add_command(label="Cerrar")
archivoMenu.add_command(label="Salir")

edicionMenu = Menu(barraMenu, tearoff=0)
edicionMenu.add_command(label="Cortar")
edicionMenu.add_command(label="Copiar")
edicionMenu.add_command(label="Pegar")
edicionMenu.add_separator()
edicionMenu.add_command(label="Rehacer")
edicionMenu.add_command(label="Deshacer")

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Revisar documentación")

barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
barraMenu.add_cascade(label="Edición", menu=edicionMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

# Frame para la gráfica a la derecha
frame = Frame(raiz, bg='gray22', bd=3)
frame.grid(column=1, row=0, sticky='nsew')

# Crear la figura y el canvas
fig, ax = plt.subplots(dpi=90, figsize=(8, 6), facecolor='#D3D3D3')
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(column=0, row=0, padx=5, pady=5)

# Variables predeterminadas para los títulos
titulo_grafica = StringVar(value="Título de la Gráfica")
title_fuente = "DejaVu Sans"
title_size = 12
personal_ventana_title = None  # Inicializamos la ventana emergente como None

titulo_eje_x = StringVar(value="Eje Horizontal")
ejex_fuente = "DejaVu Sans"
ejex_size = 8

titulo_eje_y = StringVar(value="Eje Vertical")
ejey_fuente = "DejaVu Sans"
ejey_size = 8

# Variables de personalización
line_color = 'blue' 
line_width = 2       
bg_color = '#D3D3D3' 
marker_type = "o"
marker_color = "blue"
show_grid = False  # Variable para controlar si la grilla está activa o no
point_size = 5  # Tamaño de los puntos
line = None
personalizacion_ventana= None

# Inicializar variables para manejo del zoom y desplazamiento
x_limits = [-1, 12]
y_limits = [-1, 1]
x = np.arange(0, 10, 0.1)
y = np.sin(x)
is_dragging = False
start_x, start_y = 0, 0
points = None  # Objeto necesario para almacenamiento de puntos y posterior edición

def guardar_grafica(formato):
    """
    Función para guardar la gráfica actual en el formato especificado por el usuario.
    
    Parámetros
    -----------
    formato : str
        El formato en el que se desea guardar la gráfica ('pdf', 'png', 'jpg').
    
    Returns
    -----------
    None
        La función abre un cuadro de diálogo para guardar el archivo y luego lo guarda en el formato seleccionado.
    """
    archivo = filedialog.asksaveasfilename(defaultextension=f".{formato}",
                                           filetypes=[(f"{formato.upper()} files", f"*.{formato}"),
                                                      ("All files", "*.*")])

    if archivo:
        fig.savefig(archivo, format=formato)
        print(f"Gráfica guardada como {archivo}")

def graficar_datos():
    """
    Esta función se encarga de dibujar o actualizar la gráfica de datos en el canvas de Matplotlib 
    dentro de la interfaz gráfica. Limpia la gráfica anterior, dibuja una nueva basada en los datos actuales 
    y actualiza los títulos y límites de los ejes.

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

    Returns
    ------------
    None
        No retorna ningún valor, sino que actualiza la gráfica con los nuevos datos y títulos.
    """
    ax.clear()  # Limpiar la gráfica anterior
    line, = ax.plot(x, y, color=line_color, marker=marker_type, markersize=point_size, markerfacecolor=marker_color, linewidth=line_width, label="Seno")
    ax.set_xlim(x_limits)  # Límites del eje X
    ax.set_ylim(y_limits)  # Límites del eje Y
    ax.set_title(titulo_grafica.get())  # Actualizar título
    ax.set_xlabel(titulo_eje_x.get())  # Actualizar título eje X    
    ax.set_ylabel(titulo_eje_y.get())  # Actualizar título eje Y
    ax.grid(show_grid)
    ax.set_facecolor(bg_color)
    canvas.draw()  # Actualizar la gráfica

    canvas.mpl_connect('button_press_event', lambda event: on_line_click(event, line))
    canvas.mpl_connect('button_press_event', on_double_click)

# Funciones para abrir ventana emergente y editar los puntos
def update_graph_property(property_type=None, new_value=None):
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
    canvas.mpl_connect('button_press_event', lambda event: on_line_click(event, line))


def grafica_ventana(master):
    global personalizacion_ventana

    if personalizacion_ventana is not None and personalizacion_ventana.winfo_exists():
        personalizacion_ventana.lift()
        return  

    personalizacion_ventana = Toplevel(master)
    personalizacion_ventana.title("Personalización de Gráfica")
    personalizacion_ventana.geometry("400x400")

    # Sección del Fondo
    Label(personalizacion_ventana, text="Fondo", font=("Arial", 12, "bold")).pack(pady=10)
    Button(personalizacion_ventana, text="Color de Fondo", command=lambda: update_graph_property('bg_color')).pack(pady=5)

    # Checkbutton para activar/desactivar la grilla
    grid_var = IntVar(value=int(show_grid))  # Inicializar con el valor actual
    Checkbutton(personalizacion_ventana, text="Mostrar Grilla", variable=grid_var, command=lambda: update_graph_property('grid', grid_var.get())).pack(pady=5)

    # Crear un frame para la disposición en dos columnas
    frame = Frame(personalizacion_ventana)
    frame.pack(pady=10)

    linea_frame = Frame(frame)
    linea_frame.grid(row=0, column=0, padx=20)

    Label(linea_frame, text="Línea", font=("Arial", 12, "bold")).pack(pady=10)

    # Botón para seleccionar el color de la línea
    Button(linea_frame, text="Color de Línea", command=lambda: update_graph_property('line_color')).pack(pady=5)

    # Slider para ajustar el grosor de la línea
    Label(linea_frame, text="Tamaño de Línea:").pack(pady=5)
    line_width_slider = Scale(linea_frame, from_=0.5, to=10, resolution=0.1, orient=HORIZONTAL, command=lambda value: update_graph_property('line_width', value))
    line_width_slider.set(line_width)
    line_width_slider.pack(pady=5)

    puntos_frame = Frame(frame)
    puntos_frame.grid(row=0, column=1, padx=20)

    Label(puntos_frame, text="Puntos", font=("Arial", 12, "bold")).pack(pady=10)

    # Menú para seleccionar el tipo de marcador
    Label(puntos_frame, text="Tipo de Marcador:").pack()
    marker_options = ['o', 'x', '^', 's', '*']  
    marker_var = StringVar(value=marker_type)
    marker_menu = ttk.Combobox(puntos_frame, textvariable=marker_var, values=marker_options)
    marker_menu.pack(pady=5)
    marker_menu.bind("<<ComboboxSelected>>", lambda event: update_graph_property('marker_type', marker_var.get()))

    # Botón para seleccionar el color de los puntos
    Button(puntos_frame, text="Color de Puntos", command=lambda: update_graph_property('marker_color')).pack(pady=5)

    # Slider para ajustar el tamaño de los puntos
    Label(puntos_frame, text="Tamaño de Puntos:").pack(pady=5)
    point_size_slider = Scale(puntos_frame, from_=1, to=20, resolution=1, orient=HORIZONTAL, command=lambda value: update_graph_property('point_size', value))
    point_size_slider.set(point_size)
    point_size_slider.pack(pady=5)

def on_line_click(event, line):
    if event.inaxes and event.button == 1:  # Botón izquierdo del mouse
        # Se obtienen las coordenadas de los puntos de la línea
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        
        # Comprobar si el click fue cerca de la línea
        for i in range(len(xdata)):
            if abs(event.xdata - xdata[i]) < 0.1 and abs(event.ydata - ydata[i]) < 0.1:
                grafica_ventana(raiz) 
                break

# Función para aplicar los cambios del título
def apply_title_changes(title_size_var, title_fuente_var, titulo_grafica_entry):
    global title_size, title_fuente, titulo_grafica
    titulo_grafica.set(titulo_grafica_entry.get())  # Obtener el nuevo título
    
    # Obtener valores seleccionados
    title_size = int(title_size_var.get())
    title_fuente = title_fuente_var.get()
    
    # Actualizar el título de la gráfica
    ax.set_title(titulo_grafica.get(), fontsize=title_size, fontname=title_fuente)
    
    # Redibujar la gráfica
    canvas.draw()

# Función para abrir la ventana emergente de edición del título
def grafica_ventana_title(master):
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

# Función para detectar doble clic en el título y abrir la ventana de edición
def on_double_click(event):
    if event.dblclick:
        # Coordenadas del clic en la ventana gráfica
        x, y = event.x, event.y

        # Obtener la posición del título
        bbox_title = ax.title.get_window_extent(canvas.get_renderer())

        # Comprobar si el clic fue en el título de la gráfica
        if bbox_title.contains(x, y):
            grafica_ventana_title(raiz)  # Usar la ventana principal 'raiz' para abrir la personalización

# Conectar evento de doble clic
canvas.mpl_connect('button_press_event', on_double_click)

# Guardar límites originales para reestablecer al tamaño original
origx_lim = x_limits.copy()
origy_lim = y_limits.copy()

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
    global x_limits, y_limits # Variables globales, límites de 'x' y 'y'
    if reset:
        # Restablecer límites originales
        x_limits = origx_lim.copy()
        y_limits = origy_lim.copy()
        zoom_label.config(text="Zoom: 100%")  # Restablecer la etiqueta de zoom
        scale.set(0)  # Resetear la barra de zoom a su posición inicial
    else:
        zoom_level = scale.get()  # Obtener el valor de la barra
        if zoom_level == 0:
            # Si la barra está en el nivel inicial, restablecer los límites originales
            x_limits = origx_lim.copy()
            y_limits = origy_lim.copy()
        else:   
            x_mid = (x_limits[1] + x_limits[0]) / 2 # Punto medio 'x'
            y_mid = (y_limits[1] + y_limits[0]) / 2 # Punto medio 'y'
            zoom_factor = 1 + zoom_level
            # Rango de los ejes de acuerdo a la escala de zoom
            x_range = (x_limits[1] - x_limits[0]) / zoom_factor
            y_range = (y_limits[1] - y_limits[0]) / zoom_factor
            # Actualización de los límites acorde al zoom
            x_limits = [x_mid - x_range / 2, x_mid + x_range / 2]
            y_limits = [y_mid - y_range / 2, y_mid + y_range / 2]

        # Actualizar la etiqueta de porcentaje de zoom
        zoom_percentage = int((zoom_level / 6) * 100)
        zoom_label.config(text=f"Zoom: {zoom_percentage}%")


    # Redibujar la gráfica con los nuevos límites
    graficar_datos() # Modificar respecto a los módulos por agregar

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

    
    """
    global x_limits, y_limits, start_x, start_y
    if is_dragging and event.inaxes: # Verificación de interacción True and True
        
        # Calculo de diferencia entre el clic inicial y la posición actual del cursor
        dx = start_x - event.xdata
        dy = start_y - event.ydata
        
        # Redefinir los límites de acuerdo al desplazamiento
        x_limits = [x + dx for x in x_limits]
        y_limits = [y + dy for y in y_limits]

        # Redibujar la gráfica con los nuevos límites
        graficar_datos()

# Conectar eventos del ratón
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

# Barra de zoom
style = ttk.Style()
style.configure("Horizontal.TScale", background='gray22')  # Configurar estilo para la barra

scale = ttk.Scale(frame, to=6, from_=0, orient='horizontal', length=200, style="Horizontal.TScale", command=zoom)
scale.grid(column=0, row=3)

# Etiqueta para mostrar el porcentaje de zoom
zoom_label = ttk.Label(frame, text="Zoom: 0%")
zoom_label.grid(column=0, row=4)

# Botón para graficar
Button(frame, text='Graficar', width=15, bg='green', fg='white', command=graficar_datos).grid(column=0, row=1, pady=5)

# Ejecutar la aplicación
raiz.mainloop()
