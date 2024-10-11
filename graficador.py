# Librerías necesarias para realizar un graficador
from tkinter import Tk, Frame, Button, Label, Menu, ttk
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

edicionEspMenu = Menu(barraMenu, tearoff=0)
edicionEspMenu.add_command(label="Cambiar Título")
edicionEspMenu.add_command(label="Cambiar límites")
edicionEspMenu.add_command(label="Cambiar título ejes")
edicionEspMenu.add_separator()
edicionEspMenu.add_command(label="Tamaño punto")
edicionEspMenu.add_command(label="Color punto")

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Revisar documentación")

barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
barraMenu.add_cascade(label="Edición", menu=edicionMenu)
barraMenu.add_cascade(label="Edición Especial", menu=edicionEspMenu)
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

# Función para graficar los puntos. Función ejemplo -> vincular funciones d elos otros módulos
def graficar_datos():
    ax.clear()  # Limpiar la gráfica anterior
    ax.plot(x, y, 'bo-', label="Seno")  # Graficar los puntos
    ax.set_xlim(x_limits)  # Límites del eje X
    ax.set_ylim(y_limits)  # Límites del eje Y
    ax.set_title("Gráfica del Seno")
    ax.set_xlabel("Eje Horizontal")
    ax.set_ylabel("Eje Vertical")
    ax.grid(True)  # Activar la grilla
    canvas.draw()  # Actualizar la gráfica

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
