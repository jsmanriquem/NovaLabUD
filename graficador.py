# Librerías necesarias para realizar un graficador
from tkinter import Tk, Frame, Button, Label, Menu, Toplevel, StringVar, ttk, Entry, filedialog, colorchooser
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
titulo_grafica = StringVar(value="Título")
titulo_eje_x = StringVar(value="Eje Horizontal")
titulo_eje_y = StringVar(value="Eje Vertical")

# Variables de personalización
line_color = 'blue' 
line_width = 2       
bg_color = '#D3D3D3' 
marker_type = "o"
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
    line, = ax.plot(x, y, 'bo-', color=line_color, marker = marker_type, linewidth=line_width, label="Seno")   # Graficar los puntos
    ax.set_xlim(x_limits)  # Límites del eje X
    ax.set_ylim(y_limits)  # Límites del eje Y
    ax.set_title(titulo_grafica.get())  # Actualizar título
    ax.set_xlabel(titulo_eje_x.get())  # Actualizar título eje X    
    ax.set_ylabel(titulo_eje_y.get())  # Actualizar título eje Y
    ax.grid(True)  # Activar la grilla
    ax.set_facecolor(bg_color)
    canvas.draw()  # Actualizar la gráfica

    canvas.mpl_connect('button_press_event', lambda event: on_line_click(event, line))

# Funciones para abrir ventana emergente y editar los puntos
def apply_graph_changes(line_width_entry, marker_var):
    global line_width, marker_type
    try:
        line_width = float(line_width_entry.get())
        
        marker_type = marker_var.get()
        
        graficar_datos()
    except ValueError:
        print("Error: El grosor de línea debe ser un número.")

def select_line_color():
    global line_color
    line_color = colorchooser.askcolor()[1]
    graficar_datos()

def select_bg_color():
    global bg_color
    bg_color = colorchooser.askcolor()[1]
    ax.set_facecolor(bg_color) 
    graficar_datos()  

def grafica_ventana(master):
    global personalizacion_ventana

    # Verificar si la ventana ya está abierta
    if personalizacion_ventana is not None and personalizacion_ventana.winfo_exists():
        personalizacion_ventana.lift()  # Lleva la ventana al frente
        return  # No abrir otra ventana

    # Crear nueva ventana
    personalizacion_ventana = Toplevel(master)
    personalizacion_ventana.title("Personalización de Gráfica")
    personalizacion_ventana.geometry("300x250")

    # Color de la línea
    Button(personalizacion_ventana, text="Seleccionar Color de Línea", command=select_line_color).pack(pady=10)

    # Grosor de la línea
    Label(personalizacion_ventana, text="Grosor de Línea:").pack(pady=5)
    line_width_entry = Entry(personalizacion_ventana)
    line_width_entry.insert(0, str(line_width))
    line_width_entry.pack(pady=5)

    # Selección del tipo de marcador (círculo, cruz, triángulo, etc.)
    marker_label = Label(personalizacion_ventana, text="Tipo de marcador:")
    marker_label.pack()
    marker_options = ['o', 'x', '^', 's', '*']  # Opciones de marcadores
    marker_var = StringVar(value=marker_type)  # Valor actual del marcador
    
    marker_menu = ttk.Combobox(personalizacion_ventana, textvariable=marker_var, values=marker_options)
    marker_menu.pack()

    Button(personalizacion_ventana, text="Seleccionar Color de Fondo", command=select_bg_color).pack(pady=10)

    Button(personalizacion_ventana, text="Aplicar Cambios", command=lambda: apply_graph_changes(line_width_entry, marker_var)).pack(pady=20)

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

canvas.mpl_connect('button_press_event', lambda event: on_line_click(event, line))

def on_double_click(event):
    """
    Captura el evento de doble click en la gráfica y permite editar los títulos de la gráfica y 
    los ejes. Dependiendo de la posición del click, se abre un campo de entrada para modificar 
    el título correspondiente.

    Parámetros
    --------------------
    event : matplotlib.backend_bases.MouseEvent
        Evento que contiene la información del doble click en la gráfica.

    Variables globales
    --------------------
    ax : matplotlib.axes.Axes
        Objeto de ejes donde se encuentra el título de la gráfica y los ejes.
    canvas : matplotlib.backends.backend_tkagg.FigureCanvasTkAgg
        Canvas donde se renderiza la gráfica dentro de Tkinter.
    titulo_grafica : StringVar
        Variable que contiene el título de la gráfica.
    titulo_eje_x : StringVar
        Variable que contiene el título del eje X.
    titulo_eje_y : StringVar
        Variable que contiene el título del eje Y.

    Returns
    --------------------
    None
        La función no retorna ningún valor, abre un campo de entrada si se hace doble click
        en un título.
    """
    if event.dblclick:
        # Coordenadas del clic en la ventana gráfica
        x, y = event.x, event.y

        # Obtener posiciones de los títulos actuales
        bbox_title = ax.title.get_window_extent(canvas.get_renderer())
        bbox_xlabel = ax.xaxis.label.get_window_extent(canvas.get_renderer())
        bbox_ylabel = ax.yaxis.label.get_window_extent(canvas.get_renderer())

        # Comprobar si el clic fue en el título de la gráfica
        if bbox_title.contains(x, y):
            crear_entry(titulo_grafica, 300, 50)
        # Comprobar si el clic fue en el título del eje X
        elif bbox_xlabel.contains(x, y):
            crear_entry(titulo_eje_x, 300, 500)
        # Comprobar si el clic fue en el título del eje Y
        elif bbox_ylabel.contains(x, y):
            crear_entry(titulo_eje_y, 100, 300)

def crear_entry(variable_titulo, x_pos, y_pos):
    """
    Crea un campo de entrada en una posición específica para que el usuario pueda
    modificar el título de la gráfica o de los ejes. Se destruye al presionar enter,
    actualizando así el nuevo título.

    Parámetros
    --------------------
    variable_titulo : tkinter.StringVar
        Variable que contiene el valor actual del título a modificar.
    x_pos : int
        Coordenada X para posicionar el campo de entrada.
    y_pos : int
        Coordenada Y para posicionar el campo de entrada.

    Returns
    --------------------
    None
    """
    # Crear el campo de entrada y asociarlo con la variable correspondiente al título
    entry = Entry(raiz, textvariable = variable_titulo)
    entry.place(x=x_pos, y=y_pos)  # Posicionar el campo de entrada en la interfaz

    # Vincular la acción de presionar "Enter" para actualizar el título y redibujar la gráfica
    entry.bind("<Return>", lambda event: (variable_titulo.set(entry.get()), entry.destroy(), graficar_datos()))

# Conectar eventos del ratón en Matplotlib (doble clic)
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
