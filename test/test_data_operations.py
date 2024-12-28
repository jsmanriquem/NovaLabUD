import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import patch
from tkinter import messagebox
from data_operations import DataOperations

@pytest.fixture
def data_ops():
    """
    Fixture que crea una instancia de DataOperations con datos de prueba.
    Esta función se ejecutará antes de cada prueba que la utilice.
    """
    ops = DataOperations()
    # Creamos datos de prueba con valores nulos y duplicados
    data = {
        'A': [1, 2, np.nan, 4, 5, 5],
        'B': [10, 20, 30, np.nan, 50, 50],
        'C': ['x', 'y', 'z', 'x', 'y', 'y']
    }
    ops.data = pd.DataFrame(data)
    ops.original_data = ops.data.copy()
    return ops

def test_initialization():
    """
    Prueba la inicialización correcta de la clase DataOperations.
    Verifica que todos los atributos se inicialicen con los valores esperados.
    """
    ops = DataOperations()
    assert ops.data is None
    assert ops.original_data is None
    assert isinstance(ops.transformation_history, list)
    assert len(ops.transformation_history) == 0

@patch('tkinter.messagebox.showinfo')
def test_remove_null_values(mock_showinfo, data_ops):
    """
    Prueba la eliminación de valores nulos del DataFrame.
    Verifica tanto la eliminación de datos como el registro en el historial.
    """
    initial_rows = len(data_ops.data)
    data_ops.remove_null_values()
    
    assert len(data_ops.data) < initial_rows
    assert not data_ops.data.isnull().any().any()
    assert len(data_ops.transformation_history) == 1
    assert data_ops.transformation_history[0]['operation'] == 'remove_null_values'

@patch('tkinter.messagebox.showinfo')
def test_remove_duplicates(mock_showinfo, data_ops):
    """
    Prueba la eliminación de filas duplicadas del DataFrame.
    Verifica la eliminación de duplicados y el registro en el historial.
    """
    initial_rows = len(data_ops.data)
    data_ops.remove_duplicates()
    
    assert len(data_ops.data) < initial_rows
    assert not data_ops.data.duplicated().any()
    assert len(data_ops.transformation_history) == 1
    assert data_ops.transformation_history[0]['operation'] == 'remove_duplicates'

def test_normalize_data(data_ops):
    """
    Prueba la normalización de datos numéricos.
    Verifica que los valores estén en el rango correcto y el registro en el historial.
    """
    numeric_columns = ['A', 'B']
    data_ops.normalize_data(numeric_columns, method="Min-Max Scaling")
    
    for col in numeric_columns:
        non_null_values = data_ops.data[col].dropna()
        assert non_null_values.min() >= 0
        assert non_null_values.max() <= 1
    
    assert len(data_ops.transformation_history) == 1
    assert data_ops.transformation_history[0]['operation'] == 'normalize_data'

@patch('tkinter.messagebox.showinfo')
@patch('tkinter.messagebox.showwarning')
def test_fill_null_values_mean_no_history(mock_showwarning, mock_showinfo, data_ops):
    """
    Prueba el llenado de valores nulos usando la media, sin verificar el historial.
    """
    # Diagnóstico inicial
    initial_nulls = data_ops.data.isnull().sum().sum()
    assert initial_nulls > 0, "El DataFrame inicial no tiene valores nulos."

    # Llenamos los valores nulos
    with patch('builtins.print'):  # Suprimimos la salida de print si existe
        data_ops.fill_null_values(method='mean')

    # Verificamos que no queden valores nulos
    final_nulls = data_ops.data.isnull().sum().sum()
    assert final_nulls == 0, "El método fill_null_values no llenó todos los valores nulos."





# Separamos las pruebas de exportación por tipo de archivo
@patch('tkinter.filedialog.asksaveasfilename')
@patch('tkinter.messagebox.showinfo')
def test_export_results_xlsx(mock_showinfo, mock_asksaveasfilename, data_ops, tmp_path):
    """
    Prueba la exportación de resultados en formato Excel.
    """
    temp_file = str(tmp_path / "test_export.xlsx")
    mock_asksaveasfilename.return_value = temp_file
    
    with patch('tkinter.messagebox.showinfo'):
        data_ops.remove_null_values()
        result = data_ops.export_results()
    
    assert result is True

@patch('tkinter.filedialog.asksaveasfilename')
@patch('tkinter.messagebox.showinfo')
def test_export_results_csv(mock_showinfo, mock_asksaveasfilename, data_ops, tmp_path):
    """
    Prueba la exportación de resultados en formato CSV.
    """
    temp_file = str(tmp_path / "test_export.csv")
    mock_asksaveasfilename.return_value = temp_file
    
    with patch('tkinter.messagebox.showinfo'):
        data_ops.remove_null_values()
        result = data_ops.export_results()
    
    assert result is True

@patch('tkinter.filedialog.askopenfilename')
def test_load_file_invalid_extension(mock_askopenfilename, data_ops, tmp_path):
    """
    Prueba la carga de un archivo con extensión inválida.
    Verifica que se maneje correctamente el error.
    """
    invalid_file = tmp_path / "test.invalid"
    invalid_file.touch()
    mock_askopenfilename.return_value = str(invalid_file)
    
    result = data_ops.load_file()
    assert result is False

@patch('tkinter.messagebox.showwarning')
def test_error_handling_without_data(mock_showwarning):
    """
    Prueba el manejo de errores cuando no hay datos cargados.
    Verifica que se muestren las advertencias apropiadas.
    """
    ops = DataOperations()
    
    ops.remove_null_values()
    mock_showwarning.assert_called_with("Advertencia", "Primero debes cargar los datos")
    
    ops.remove_duplicates()
    mock_showwarning.assert_called_with("Advertencia", "Primero debes cargar los datos")

def test_transformation_history_format(data_ops):
    """
    Prueba el formato correcto del historial de transformaciones.
    Verifica que cada entrada del historial tenga la estructura correcta.
    """
    with patch('tkinter.messagebox.showinfo'):
        data_ops.remove_null_values()
    
    assert len(data_ops.transformation_history) == 1
    entry = data_ops.transformation_history[0]
    
    # Verificación de la estructura del historial
    required_fields = ['operation', 'timestamp', 'details', 'rows_affected']
    for field in required_fields:
        assert field in entry
    
    # Verificación de tipos de datos
    assert isinstance(entry['operation'], str)
    assert isinstance(entry['timestamp'], str)
    assert isinstance(entry['rows_affected'], int)
    
    # Verificación del formato de timestamp
    try:
        datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        pytest.fail("Formato de timestamp inválido en el historial")