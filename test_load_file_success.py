import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from modules.data_operations import DataOperations  

@pytest.fixture
def data_ops():
    """Fixture para crear una instancia de DataOperations."""
    return DataOperations()

def test_load_file_success(data_ops):
    """Prueba la carga exitosa de un archivo CSV."""
    sample_data = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    })

    # Simula la función de callback de la UI
    ui_callback = MagicMock()

    # Usa patch para simular filedialog.askopenfilename y pd.read_csv
    with patch('builtins.open', new_callable=MagicMock), \
         patch('pandas.read_csv', return_value=sample_data), \
         patch('modules.data_operations.filedialog.askopenfilename', return_value='fake_path.csv'):
        result = data_ops.load_file(ui_callback)

    assert result is True
    assert data_ops.data.equals(sample_data)  # Verifica que los datos cargados sean correctos
    ui_callback.assert_called_once_with(sample_data)  # Verifica que el callback se haya llamado correctamente

def test_load_file_failure(data_ops):
    """Prueba la carga de un archivo que no existe."""
    ui_callback = MagicMock()

    with patch('modules.data_operations.filedialog.askopenfilename', return_value='fake_path.csv'):
        with patch('pandas.read_csv', side_effect=FileNotFoundError):
            result = data_ops.load_file(ui_callback)

    assert result is False
    assert data_ops.data is None  # Asegúrate de que los datos no se cargaron
    ui_callback.assert_not_called()  # Verifica que el callback no se haya llamado

def test_load_file_cancel(data_ops):
    """Prueba la carga cuando el usuario cancela la selección del archivo."""
    ui_callback = MagicMock()

    with patch('modules.data_operations.filedialog.askopenfilename', return_value=None):
        result = data_ops.load_file(ui_callback)

    assert result is False
    assert data_ops.data is None  # Asegúrate de que no se cargaron datos
    ui_callback.assert_called_once_with(None)  # Verifica que el callback se haya llamado con None

