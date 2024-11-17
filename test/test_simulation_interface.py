import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
from data_operations import DataOperations

@pytest.fixture
def data_ops():
    """Fixture que proporciona una instancia de DataOperations"""
    return DataOperations()

@pytest.fixture
def sample_dataframe():
    """Fixture que proporciona un DataFrame de prueba con datos"""
    return pd.DataFrame({
        'A': [1, 2, np.nan, 4, 1],
        'B': [10, 20, 30, np.nan, 10],
        'C': ['x', 'y', 'z', 'x', 'x']
    })

class TestDataOperations:
    
    def test_initialization(self, data_ops):
        """Prueba la inicialización correcta de la clase"""
        assert data_ops.data is None
        assert data_ops.original_data is None
        assert data_ops.transformation_history == []

    @patch('tkinter.filedialog.askopenfilename')
    def test_load_file_csv(self, mock_filedialog, data_ops, sample_dataframe):
        """Prueba la carga de un archivo CSV"""
        # Simulamos la selección de un archivo CSV
        mock_filedialog.return_value = "test_load.csv"
        
        # Simulamos la lectura del DataFrame
        with patch('pandas.read_csv', return_value=sample_dataframe):
            result = data_ops.load_file()
            
        assert result is True
        pd.testing.assert_frame_equal(data_ops.data, sample_dataframe)
        pd.testing.assert_frame_equal(data_ops.original_data, sample_dataframe)
        assert len(data_ops.transformation_history) == 0

    def test_remove_null_values_no_data(self, data_ops):
        """Prueba remove_null_values cuando no hay datos cargados"""
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            data_ops.remove_null_values()
            mock_warning.assert_called_once_with("Advertencia", "Primero debes cargar los datos")

    def test_remove_duplicates(self, data_ops, sample_dataframe):
        """Prueba la eliminación de duplicados"""
        data_ops.data = sample_dataframe.copy()
        data_ops.original_data = sample_dataframe.copy()
        
        with patch('tkinter.messagebox.showinfo') as mock_info:
            data_ops.remove_duplicates()
        
        # Verificar que las filas duplicadas fueron eliminadas
        expected_data = pd.DataFrame({
            'A': [1, 2, np.nan, 4],
            'B': [10, 20, 30, np.nan],
            'C': ['x', 'y', 'z', 'x']
        })
        pd.testing.assert_frame_equal(data_ops.data.reset_index(drop=True), expected_data.reset_index(drop=True))
        
        # Verificar mensajes
        mock_info.assert_called_once()
        assert len(data_ops.transformation_history) == 1
        assert data_ops.transformation_history[0]['operation'] == 'remove_duplicates'
        assert 'Eliminadas 1 filas duplicadas' in data_ops.transformation_history[0]['details']


    #PROBAR EL TEST DE EXPORTAR RESULTADOS

    def test_get_transformation_summary(self, data_ops):
        """Prueba la generación del resumen de transformaciones"""
        data_ops.transformation_history = [
            {
                'operation': 'test_operation',
                'timestamp': '2024-01-01 12:00:00',
                'details': 'Test details',
                'rows_affected': 100
            }
        ]
        
        summary = data_ops.get_transformation_summary()
        assert 'test_operation' in summary
        assert '2024-01-01 12:00:00' in summary
        assert 'Test details' in summary
        assert '100' in summary

    def test_get_transformation_summary_empty(self, data_ops):
        """Prueba el resumen de transformaciones cuando no hay transformaciones"""
        summary = data_ops.get_transformation_summary()
        assert summary == "No se han realizado transformaciones"
