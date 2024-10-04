# Librerías
from tkinter import Tk, Frame, Button, Label, Menu, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Posicionamiento de la gráfica
import numpy as np
import matplotlib.pyplot as plt

# Definir estilo de la gráfica
plt.rcParams['font.family'] = 'Times New Roman'
fig, ax = plt.subplots(dpi=90, figsize=(8, 6), facecolor='#D3D3D3')
plt.title("Título de la gráfica", color='blue', size=16, family="Times New Roman")

plt.xlim(-1, 12)  # Límites eje x
plt.ylim(-1, 8)  # Límites eje y
ax.set_facecolor('white')  # Color de fondo

# Grosor y color de los ejes
ax.axhline(linewidth=1.5, color='black')
ax.axvline(linewidth=1.5, color='black')

# Etiquetas
ax.set_xlabel("Eje  Horizontal", color='black')
ax.set_ylabel("Eje  Vertical", color='black')
ax.tick_params(direction='out', length=6, width=2,  # Líneas para los números
               colors='black', grid_color='r', grid_alpha=0.5)

# Función ejemplo
def graficar_datos():
    nivel = scale.get()
    x = np.arange(-np.pi, 4*np.pi, 0.01)
    line, = ax.plot(x, nivel*np.sin(x),
                    color='b', linestyle='solid')
    canvas.draw()
    label.config(text=nivel)
    line.set_ydata(np.sin(x)+10)
    raiz.after(100, graficar_datos)

# Ventana principal
raiz = Tk()
raiz.geometry("1024x780")  # Tamaño de la pantalla
raiz.config(bg="gray")  # Color de fondo
raiz.wm_title('Gráfica Matplotlib con Scale')  # Título de la gráfica

# Menú 
barraMenu = Menu(raiz) 
raiz.config(menu=barraMenu)

archivoMenu = Menu(barraMenu, tearoff=0)
archivoMenu.add_command(label="Nuevo")
archivoMenu.add_command(label="Guardar")

# Crear un submenú para la opción "Guardar como ..."
guardarComoMenu = Menu(archivoMenu, tearoff=0)
guardarComoMenu.add_command(label="PDF")
guardarComoMenu.add_command(label="JPG")
guardarComoMenu.add_command(label="PNG")

# Añadir el submenú a la opción "Guardar como ..."
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

# Añadir los menús a la barra de menú
barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
barraMenu.add_cascade(label="Edición", menu=edicionMenu)
barraMenu.add_cascade(label="Edición Especial", menu=edicionEspMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

# Frame para la gráfica a la derecha
graph_frame = Frame(raiz, bg='gray22', bd=3)
graph_frame.grid(column=1, row=0, sticky='nsew')

canvas = FigureCanvasTkAgg(fig, master=graph_frame)  # Crea el área de dibujo en Tkinter
canvas.get_tk_widget().grid(column=0, row=0, padx=5, pady=5)

# Creación del botón graficar y su funcionamiento
Button(graph_frame, text='Graficar', width=15, bg='green', fg='white', command=graficar_datos).grid(
    column=0, row=1, pady=5, sticky='ew')  # Centrado horizontal

# Barra de escala
scale = ttk.Scale(graph_frame, to=6, from_=0, orient='horizontal', length=300)
scale.grid(column=0, row=2)

style = ttk.Style()
style.configure("Horizontal.TScale", background='gray22')

raiz.mainloop()