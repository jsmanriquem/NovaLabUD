# Librerías necesarias para realizar un graficador
from tkinter import Tk, Frame, Button, Label, Menu, Toplevel, StringVar, ttk, Entry
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
guardarComoMenu.add_command(label="PDF")
guardarComoMenu.add_command(label="JPG")
guardarComoMenu.add_command(label="PNG")
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

# Inicializar variables para manejo del zoom y desplazamiento
x_limits = [-1, 12]
y_limits = [-1, 1]
x = np.arange(0, 10, 0.1)
y = np.sin(x)
is_dragging = False
start_x, start_y = 0, 0

# Variables predeterminadas para los títulos
titulo_grafica = StringVar(value="Título")
titulo_eje_x = StringVar(value="Eje Horizontal")
titulo_eje_y = StringVar(value="Eje Vertical")


# Función para graficar los puntos. Función ejemplo -> vincular funciones d elos otros módulos
def graficar_datos():
    ax.clear()  # Limpiar la gráfica anterior
    ax.plot(x, y, 'bo-', label="Seno")  # Graficar los puntos
    ax.set_xlim(x_limits)  # Límites del eje X
    ax.set_ylim(y_limits)  # Límites del eje Y
    ax.set_title(titulo_grafica.get())  # Actualizar título
    ax.set_xlabel(titulo_eje_x.get())  # Actualizar título eje X    
    ax.set_ylabel(titulo_eje_y.get())  # Actualizar título eje Y
    ax.grid(True)  # Activar la grilla
    canvas.draw()  # Actualizar la gráfica

# Función para capturar el doble clic y editar los títulos
def on_double_click(event):
    # Obtener coordenadas del clic
    if event.dblclick:
        # Coordenadas del clic en la ventana gráfica
        x, y = event.x, event.y

        # Obtener posiciones de los títulos actuales
        bbox_title = ax.title.get_window_extent(canvas.get_renderer())
        bbox_xlabel = ax.xaxis.label.get_window_extent(canvas.get_renderer())
        bbox_ylabel = ax.yaxis.label.get_window_extent(canvas.get_renderer())

        # Comprobar si el clic fue en el título de la gráfica
        if bbox_title.contains(x, y):
            crear_entry(titulo_grafica, 'gráfica', 300, 50)
        # Comprobar si el clic fue en el título del eje X
        elif bbox_xlabel.contains(x, y):
            crear_entry(titulo_eje_x, 'eje X', 300, 500)
        # Comprobar si el clic fue en el título del eje Y
        elif bbox_ylabel.contains(x, y):
            crear_entry(titulo_eje_y, 'eje Y', 100, 300)

# Función para crear el campo de entrada en la posición del texto
def crear_entry(variable_titulo, tipo_titulo, x_pos, y_pos):
    entry = Entry(raiz, textvariable=variable_titulo)
    entry.insert(0, variable_titulo.get())
    
    # Se posiciona el campo de entrada cerca del área correspondiente
    entry.place(x=x_pos, y=y_pos)
    
    # Vinculamos el evento de presionar Enter para actualizar el título
    entry.bind("<Return>", lambda event: actualizar_titulo(entry, variable_titulo))

# Función para actualizar el título de la gráfica
def actualizar_titulo(entry, variable_titulo):
    nuevo_texto = entry.get().strip()
    entry.destroy()  # Eliminamos el campo de entrada

    # Si el campo está vacío, el título también queda vacío
    variable_titulo.set(nuevo_texto if nuevo_texto else "")
    
    # Redibujar la gráfica con los nuevos títulos
    graficar_datos()

# Conectar eventos del ratón en Matplotlib (doble clic)
canvas.mpl_connect('button_press_event', on_double_click)

# Función para ajustar el zoom (falta documentar)
def zoom(event=None):
    global x_limits, y_limits
    zoom_level = scale.get()  # Obtener el valor de la barra
    x_mid = (x_limits[1] + x_limits[0]) / 2
    y_mid = (y_limits[1] + y_limits[0]) / 2
    zoom_factor = 1 + zoom_level

    x_range = (x_limits[1] - x_limits[0]) / zoom_factor
    y_range = (y_limits[1] - y_limits[0]) / zoom_factor

    x_limits = [x_mid - x_range / 2, x_mid + x_range / 2]
    y_limits = [y_mid - y_range / 2, y_mid + y_range / 2]

    # Redibujar la gráfica con los nuevos límites
    graficar_datos()

    # Actualizar la etiqueta de porcentaje de zoom
    zoom_percentage = int((zoom_level / 6) * 100)
    zoom_label.config(text=f"Zoom: {zoom_percentage}%")

# Funciones para manejar el desplazamiento (Falta documentar)
def on_press(event):
    global is_dragging, start_x, start_y
    if event.inaxes:
        is_dragging = True
        start_x, start_y = event.xdata, event.ydata

def on_release(event):
    global is_dragging
    is_dragging = False

def on_motion(event):
    global x_limits, y_limits, start_x, start_y
    if is_dragging and event.inaxes:
        dx = start_x - event.xdata
        dy = start_y - event.ydata
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
