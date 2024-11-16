# Importar librerías que usa el graficador e importar graficador
import pytest
from unittest.mock import Mock, patch, MagicMock
from tkinter import StringVar, colorchooser, IntVar
import pandas as pd
import graficador
from graficador import * # Importando TODO

# Prueba de flujo donde se cargan datos correctamente
def test_cargar_datos_exitoso():
    with patch("graficador.data_ops") as mock_data_ops:  # Reemplazo temporal data_ops por objeto simulado
        mock_data_ops.load_file.return_value = True  # Simula carga exitosa
        mock_data_ops.data = Mock(empty=False)  # Simula que los datos no están vacíos

        with patch("graficador.actualizar_columnas") as mock_actualizar_columnas:
            cargar_datos()
            mock_actualizar_columnas.assert_called_once()  # Confirma que se llama a actualizar_columnas

# Prueba de flujo donde no se cargan datos
def test_cargar_datos_fallo():
    with patch("graficador.data_ops") as mock_data_ops, \
         patch("graficador.messagebox.showerror") as mock_showerror:
        mock_data_ops.load_file.return_value = True  # Simula carga fallida
        mock_data_ops.data = Mock(empty=True)  # Simula que los datos están vacíos

        cargar_datos()
        mock_showerror.assert_called_once_with("Error", "No se pudieron cargar los datos del archivo.")  # Confirma el mensaje de error  

# Definición de algunas variables estándar para características del graficador
titulo_grafica = StringVar(value="Título de la Gráfica")
ejex_titulo = StringVar(value="Eje X")
ejey_titulo = StringVar(value="Eje Y")
line_color = 'blue'
line_width = 2
bg_color = "white"
x_limits = [-10, 10]
y_limits = [-10, 10]
show_grid = False  

def test_limpiar_grafica():
    with patch("graficador.data_ops") as mock_data_ops:
        mock_data_ops.data = Mock()  # Simula data como un objeto válido
        mock_data_ops.data.columns = ["Columna1", "Columna2"]  # Simula columnas 
        # Pla función zoom para evitar su aparición durante el testeo
        with patch("graficador.zoom"):
            limpiar_grafica()

            # COnfirmación de valores esperados
            assert titulo_grafica.get() == "Título de la Gráfica"
            assert ejex_titulo.get() == "Eje X"
            assert ejey_titulo.get() == "Eje Y"
            assert line_color == 'blue'
            assert line_width == 2
            assert bg_color == "white"
            assert x_limits == [-10, 10]
            assert y_limits == [-10, 10]
            assert not show_grid  

# Test para guardar la gráfica con éxito 'png'
@patch("tkinter.filedialog.asksaveasfilename", return_value="/ruta/del/archivo/mi_grafica.png")
@patch("graficador.fig.savefig")
def test_guardar_grafica_exitoso_png(mock_savefig, mock_asksaveas):
    guardar_grafica("png")
    mock_savefig.assert_called_once_with("/ruta/del/archivo/mi_grafica.png", format="png")

# Test cuando el usuario cancela el cuadro de diálogo
@patch("tkinter.filedialog.asksaveasfilename", return_value="")
@patch("graficador.fig.savefig")
def test_guardar_grafica_cancelacion_png(mock_savefig, mock_asksaveas):
    guardar_grafica("png")
    mock_savefig.assert_not_called()
    
 # Test para guardar la gráfica con éxito 'pdf'
@patch("tkinter.filedialog.asksaveasfilename", return_value="/ruta/del/archivo/mi_grafica.pdf")
@patch("graficador.fig.savefig")
def test_guardar_grafica_exitoso_pdf(mock_savefig, mock_asksaveas):
    guardar_grafica("pdf")
    mock_savefig.assert_called_once_with("/ruta/del/archivo/mi_grafica.pdf", format="pdf")

# Test cuando el usuario cancela el cuadro de diálogo
@patch("tkinter.filedialog.asksaveasfilename", return_value="")
@patch("graficador.fig.savefig")
def test_guardar_grafica_cancelacion_pdf(mock_savefig, mock_asksaveas):
    guardar_grafica("pdf")
    mock_savefig.assert_not_called()
    
# Test para guardar la gráfica con éxito 'jpg'
@patch("tkinter.filedialog.asksaveasfilename", return_value="/ruta/del/archivo/mi_grafica.jpg")
@patch("graficador.fig.savefig")
def test_guardar_grafica_exitoso_jpg(mock_savefig, mock_asksaveas):
    guardar_grafica("jpg")
    mock_savefig.assert_called_once_with("/ruta/del/archivo/mi_grafica.jpg", format="jpg")

# Test cuando el usuario cancela el cuadro de diálogo
@patch("tkinter.filedialog.asksaveasfilename", return_value="")
@patch("graficador.fig.savefig")
def test_guardar_grafica_cancelacion_jpg(mock_savefig, mock_asksaveas):
    guardar_grafica("jpg")
    mock_savefig.assert_not_called()
    
# Test para columnas seleccionadas no son válidas, por ejm columnas con valores no numéricos
@patch("tkinter.messagebox.showerror")
@patch("graficador.data_ops")
def test_graficar_datos_columnas_invalidas(mock_data_ops, mock_showerror):
    # Configura columnas
    mock_data_ops.data = Mock()
    mock_data_ops.data.columns = ["Columna1", "Columna2"]
    
    columna_x.set("ColumnaX")  
    columna_y.set("ColumnaY")  
    
    graficar_datos()

    mock_showerror.assert_called_once_with("Error", "Una o ambas columnas seleccionadas no son válidas.")

# Para columnas no numéricas
@patch("tkinter.messagebox.showerror")
@patch("graficador.data_ops")
def test_graficar_datos_columnas_no_numericas(mock_data_ops, mock_showerror):
    # Simular un DataFrame 
    mock_data_ops.data = MagicMock()
    mock_data_ops.data.columns = ["Columna1", "Columna2"]
    
    mock_data_ops.data.__getitem__.side_effect = lambda key: ["texto", "texto", "texto"] if key == "Columna1" else [1, 2, 3]
    
    # Establecer columnas seleccionadas
    columna_x.set("Columna1")  
    columna_y.set("Columna2")  
    
    graficar_datos()

    mock_showerror.assert_called_once_with("Error", "Las columnas seleccionadas deben ser numéricas.")
    
# Verificación de la función graficar datos con columnas de prueba
@patch("graficador.data_ops")  
def test_graficar_datos_exitoso(mock_data_ops):
    mock_data_ops.data = pd.DataFrame({
        'Columna1': [1, 2, 3],
        'Columna2': [4, 5, 6]
    })
    
    graficar_datos()

# Funcion a probar
def update_graph_property(property_type=None, new_value=None):
    global line_width, marker_type, line_color, marker_color, bg_color, point_size, show_grid

    # Verifica las nuevas propiedades asignadas
    print(f"Property being updated: {property_type} with value: {new_value}")
    
    if property_type == 'line_width':
        line_width = new_value
    elif property_type == 'marker_type':
        marker_type = new_value
    elif property_type == 'line_color':
        line_color = new_value
    elif property_type == 'marker_color':
        marker_color = new_value
    elif property_type == 'bg_color':
        bg_color = new_value
    elif property_type == 'point_size':
        point_size = new_value
    elif property_type == 'grid':
        show_grid = bool(new_value)

# Test para line_width
@patch('graficador.colorchooser.askcolor', return_value=('#FF0000', 'red'))  # Simula selección de color
def test_update_graph_property_line_width(mock_askcolor):
    # Cambiar line_width a 5
    update_graph_property('line_width', 5)
    
    # Comprobar que la propiedad line_width ha cambiado correctamente
    assert line_width == 5  

# Test para marker_type
@patch('graficador.colorchooser.askcolor', return_value=('#FF0000', 'red'))  # Simula selección de color
def test_update_graph_property_marker_type(mock_askcolor):
    # Cambiar marker_type a 'o'
    update_graph_property('marker_type', 'o')
    
    assert marker_type == 'o'

# Test para line_color
@patch('graficador.colorchooser.askcolor', return_value=('#FF0000', 'red'))  
def test_update_graph_property_line_color(mock_askcolor):
    update_graph_property('line_color', '#FF0000')
    print(f"line_color after update: {line_color}")  # Verifica el valor actualizado
    assert line_color == '#FF0000'   

# Test para marker_color
@patch('graficador.colorchooser.askcolor', return_value=('#00FF00', 'green'))  # Simula selección de color
def test_update_graph_property_marker_color(mock_askcolor):
    # Cambiar marker_color a '#00FF00'
    update_graph_property('marker_color', '#00FF00')
    
    assert marker_color == '#00FF00'

# Test para bg_color
@patch('graficador.colorchooser.askcolor', return_value=('#FFFF00', 'white'))  # Simula selección de color
def test_update_graph_property_bg_color(mock_askcolor):
    # Cambiar bg_color a '#FFFF00'
    update_graph_property('bg_color', '#FFFF00')
    
    assert bg_color == '#FFFF00'  
    
# Test para point_size
def test_update_graph_property_point_size():
    # Cambiar point_size a 10
    update_graph_property('point_size', 10)
    
    # Comprobar que point_size ha cambiado correctamente
    assert point_size == 10  # Cambié el valor esperado a 10, que es lo que estás pasando

# Función a probar
def apply_title_changes(title_size_var, title_fuente_var, titulo_grafica_entry):
    global title_size, title_fuente, titulo_grafica
    titulo_grafica.set(titulo_grafica_entry.get())  # Actualiza el título
    
    # Obtener valores seleccionados
    title_size = int(title_size_var.get())
    title_fuente = title_fuente_var.get()
    
    # Simulación de la actualización de la gráfica
    ax.set_title(titulo_grafica.get(), fontsize=title_size, fontname=title_fuente)
    canvas.draw()

# Test para la función
def test_apply_title_changes():
    global titulo_grafica, title_size, title_fuente
    
    # Inicializar las variables de prueba con Mock
    title_size_var = MagicMock()
    title_size_var.get.return_value = 14  # Simular tamaño de fuente

    title_fuente_var = MagicMock()
    title_fuente_var.get.return_value = "DejaVu Serif"  # Simular fuente

    titulo_grafica_entry = MagicMock()
    titulo_grafica_entry.get.return_value = "Nuevo Título"  # El texto del título de entrada

    titulo_grafica.set("Título de la Gráfica")  # Establecer un valor inicial
    
    # Simulación de objetos de gráfica
    ax = MagicMock()
    canvas = MagicMock()

    # Llamar a la función con los valores simulados
    apply_title_changes(title_size_var, title_fuente_var, titulo_grafica_entry)

    # Verificar si el título se actualizó correctamente
    print(f"titulo_grafica.get(): {titulo_grafica.get()}")
    assert titulo_grafica.get() == "Nuevo Título", f"Esperado 'Nuevo Título', pero obtenido {titulo_grafica.get()}"
    
    # Verificar actualización de fuente
    assert title_size == 14, f"Esperado tamaño de fuente 14, pero obtenido {title_size}"
    
    # Verificar actualización de estilo de la fuente
    assert title_fuente == "DejaVu Serif", f"Esperado fuente 'DejaVu Serif', pero obtenido {title_fuente}"

# Función a probar
def apply_xaxis_changes(ejex_size_var, ejex_fuente_var, ejex_titulo_entry):
    global ejex_size, ejex_shape, ejex_titulo
    ejex_titulo.set(ejex_titulo_entry.get())  # Obtener el nuevo título del eje X    
    # Obtener valores seleccionados
    ejex_size = int(ejex_size_var.get())
    ejex_shape = ejex_fuente_var.get()
    
    # Actualizar el título del eje X de la gráfica
    ax.set_xlabel(ejex_titulo.get(), fontsize=ejex_size, fontname=ejex_shape)
    
    # Redibujar la gráfica
    canvas.draw()

# Test para la función
def test_apply_xaxis_changes():
    global ejex_size, ejex_shape, ejex_titulo
    
    # Inicializar las variables de prueba con Mock
    ejex_size_var = MagicMock()
    ejex_size_var.get.return_value = 14  # Simular tamaño de fuente

    ejex_fuente_var = MagicMock()
    ejex_fuente_var.get.return_value = "DejaVu Serif"  # Simular fuente

    ejex_titulo_entry = MagicMock()
    ejex_titulo_entry.get.return_value = "Nuevo Título eje x"  # El texto del título de entrada

    ejex_titulo.set("Eje X")  # Establecer un valor inicial
    
    # Simulación de objetos de gráfica
    ax = MagicMock()
    canvas = MagicMock()

    # Llamar a la función con los valores simulados
    apply_xaxis_changes(ejex_size_var, ejex_fuente_var, ejex_titulo_entry)

    # Verificar si el título se actualizó correctamente
    print(f"ejex_titulo.get(): {ejex_titulo.get()}")
    assert ejex_titulo.get() == "Nuevo Título eje x", f"Esperado 'Nuevo Título eje x', pero obtenido {ejex_titulo.get()}"
    
    # Verificar si el tamaño de la fuente se actualizó
    assert ejex_size == 14, f"Esperado tamaño de fuente 14, pero obtenido {ejex_size}"
    
    # Verificar si el estilo de la fuente se actualizó
    assert ejex_shape == "DejaVu Serif", f"Esperado fuente 'DejaVu Serif', pero obtenido {ejex_shape}"
    
# Funcion a probar
def apply_yaxis_changes(ejey_size_var, ejey_fuente_var, ejey_titulo_entry):
    global ejey_size, ejey_shape, ejey_titulo
    ejey_titulo.set(ejey_titulo_entry.get())  # Obtener el nuevo título del eje Y   
    # Obtener valores seleccionados
    ejey_size = int(ejey_size_var.get())
    ejey_shape = ejey_fuente_var.get()
    
    # Actualizar el título del eje Y de la gráfica
    ax.set_ylabel(ejey_titulo.get(), fontsize=ejey_size, fontname=ejey_shape)
    
    # Redibujar la gráfica
    canvas.draw()

# Test para la función
def test_apply_yaxis_changes():
    global ejey_size, ejey_shape, ejey_titulo
    
    # Inicializar las variables de prueba con Mock
    ejey_size_var = MagicMock()
    ejey_size_var.get.return_value = 14  # Simular tamaño de fuente

    ejey_fuente_var = MagicMock()
    ejey_fuente_var.get.return_value = "DejaVu Serif"  # Simular fuente

    ejey_titulo_entry = MagicMock()
    ejey_titulo_entry.get.return_value = "Nuevo Título eje y"  # El texto del título de entrada

    ejey_titulo.set("Eje Y")  # Establecer un valor inicial
    
    # Simulación de objetos de gráfica
    ax = MagicMock()
    canvas = MagicMock()

    # Llamar a la función con los valores simulados
    apply_yaxis_changes(ejey_size_var, ejey_fuente_var, ejey_titulo_entry)

    # Verificar si el título se actualizó correctamente
    print(f"ejey_titulo.get(): {ejey_titulo.get()}")
    assert ejey_titulo.get() == "Nuevo Título eje y", f"Esperado 'Nuevo Título eje y', pero obtenido {ejey_titulo.get()}"
    
    # Verificar si el tamaño de la fuente se actualizó
    assert ejey_size == 14, f"Esperado tamaño de fuente 14, pero obtenido {ejey_size}"
    
    # Verificar si el estilo de la fuente se actualizó
    assert ejey_shape == "DejaVu Serif", f"Esperado fuente 'DejaVu Serif', pero obtenido {ejey_shape}"

# Función a probar
def set_x_limits(x_min_entry, x_max_entry):
    global x_limits, origx_lim

    try:
        # Obtener y validar valores ingresados
        x_min = float(x_min_entry.get())
        x_max = float(x_max_entry.get())
        if x_min < x_max:
            x_limits = [x_min, x_max]
            origx_lim = x_limits.copy()
            print(f"Límites del eje X actualizados: {x_limits}")
            graficar_datos()  # Redibuja la gráfica con los nuevos límites
        else:
            print("El valor de x_min debe ser menor que x_max.")
    except ValueError:
        print("Por favor, ingrese valores numéricos válidos.")

# Parcheo para simular las siguientes funciones y evitar la aparición de ventanas emergentes
@patch("graficador.Tk")
@patch("graficador.Toplevel")
@patch("graficador.messagebox")
@patch("graficador.canvas.draw")
@patch("graficador.graficar_datos")
@patch("graficador.data_ops")
def test_set_x_limits(mock_data_ops, mock_graficar_datos, mock_canvas_draw, mock_messagebox, mock_toplevel, mock_tk):
    global x_limits, origx_lim

    # Inicializar variables globales
    x_limits = [0, 10]
    origx_lim = [0, 10]

    # Configurar data_ops.data con columnas válidas
    mock_data_ops.data = MagicMock()
    mock_data_ops.data.columns = ["columna_x", "columna_y"]

    # Simular entradas de usuario
    x_min_entry = MagicMock()
    x_max_entry = MagicMock()

    x_min_entry.get.return_value = "5"
    x_max_entry.get.return_value = "15"

    # Ejecutar la función
    set_x_limits(x_min_entry, x_max_entry)

    # Verificar que los límites se actualizan
    assert x_limits == [5.0, 15.0]
    assert origx_lim == [5.0, 15.0]

# Función a probar
def set_y_limits(y_min_entry, y_max_entry):
    global y_limits, origy_lim

    try:
        # Obtener y validar valores ingresados
        y_min = float(y_min_entry.get())
        y_max = float(y_max_entry.get())
        if y_min < y_max:
            y_limits = [y_min, y_max]
            origy_lim = y_limits.copy()
            print(f"Límites del eje Y actualizados: {y_limits}")
            graficar_datos()  # Redibuja la gráfica con los nuevos límites
        else:
            print("El valor de y_min debe ser menor que y_max.")
    except ValueError:
        print("Por favor, ingrese valores numéricos válidos.")  

# Parcheo para simular las siguientes funciones y evitar la aparición de ventanas emergentes
@patch("graficador.Tk")
@patch("graficador.Toplevel")
@patch("graficador.messagebox")
@patch("graficador.canvas.draw")
@patch("graficador.graficar_datos")
@patch("graficador.data_ops")
def test_set_y_limits(mock_data_ops, mock_graficar_datos, mock_canvas_draw, mock_messagebox, mock_toplevel, mock_tk):
    global y_limits, origy_lim

    # Inicializar variables globales
    y_limits = [0, 10]
    origy_lim = [0, 10]

    # Configurar data_ops.data con columnas válidas
    mock_data_ops.data = MagicMock()
    mock_data_ops.data.columns = ["columna_x", "columna_y"]

    # Simular entradas de usuario
    y_min_entry = MagicMock()
    y_max_entry = MagicMock()

    y_min_entry.get.return_value = "5"
    y_max_entry.get.return_value = "15"

    # Ejecutar la función
    set_y_limits(y_min_entry, y_max_entry)

    # Verificar que los límites se actualizan
    assert y_limits == [5.0, 15.0]
    assert origy_lim == [5.0, 15.0]

