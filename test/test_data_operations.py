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
        mock_filedialog.return_value = "test.csv"
        
        # Simulamos la lectura del DataFrame
        with patch('pandas.read_csv', return_value=sample_dataframe):
            result = data_ops.load_file()
            
        assert result is True
        pd.testing.assert_frame_equal(data_ops.data, sample_dataframe)
        pd.testing.assert_frame_equal(data_ops.original_data, sample_dataframe)
        assert len(data_ops.transformation_history) == 0

    def test_remove_null_values(self, data_ops, sample_dataframe):
        """Prueba la eliminación de valores nulos"""
        data_ops.data = sample_dataframe.copy()
        data_ops.original_data = sample_dataframe.copy()
        
        with patch('tkinter.messagebox.showinfo'):
            data_ops.remove_null_values()
        
        # Verificar que las filas con NaN fueron eliminadas
        assert len(data_ops.data) == 3
        assert not data_ops.data.isnull().any().any()
        assert len(data_ops.transformation_history) == 1
        assert data_ops.transformation_history[0]['operation'] == 'remove_null_values'

    def test_remove_duplicates(self, data_ops, sample_dataframe):
        """Prueba la eliminación de duplicados"""
        data_ops.data = sample_dataframe.copy()
        data_ops.original_data = sample_dataframe.copy()
        
        with patch('tkinter.messagebox.showinfo'):
            data_ops.remove_duplicates()
        
        # Verificar que las filas duplicadas fueron eliminadas
        assert len(data_ops.data) == 4  # Una fila duplicada debe ser eliminada
        assert len(data_ops.transformation_history) == 1
        assert data_ops.transformation_history[0]['operation'] == 'remove_duplicates'

    def test_normalize_data(self, data_ops):
        """Prueba la normalización de datos numéricos"""
        # Crear DataFrame con datos numéricos
        test_df = pd.DataFrame({
            'num': [1, 2, 3, 4, 5],
            'text': ['a', 'b', 'c', 'd', 'e']
        })
        
        data_ops.data = test_df.copy()
        data_ops.original_data = test_df.copy()
        
        with patch('tkinter.messagebox.showinfo'):
            data_ops.normalize_data()
        
        # Verificar que los datos numéricos están normalizados (0-1)
        assert data_ops.data['num'].min() == 0
        assert data_ops.data['num'].max() == 1
        assert len(data_ops.transformation_history) == 1
        assert data_ops.transformation_history[0]['operation'] == 'normalize_data'

    def test_fill_null_with_mean(self, data_ops, sample_dataframe):
        """Prueba el relleno de valores nulos con la media"""
        data_ops.data = sample_dataframe.copy()
        data_ops.original_data = sample_dataframe.copy()
        
        with patch('tkinter.messagebox.showinfo'):
            data_ops.fill_null_with_mean()
        
        # Verificar que no hay valores nulos y los valores se rellenaron correctamente
        assert not data_ops.data.isnull().any().any()
        assert len(data_ops.transformation_history) == 1
        assert data_ops.transformation_history[0]['operation'] == 'fill_null_with_mean'

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_export_results(self, mock_savedialog, data_ops, sample_dataframe):
        """Prueba la exportación de resultados"""
        mock_savedialog.return_value = "test_export.xlsx"
        data_ops.data = sample_dataframe
        data_ops.original_data = sample_dataframe
        
        with patch('pandas.ExcelWriter'):
            with patch('tkinter.messagebox.showinfo'):
                result = data_ops.export_results()
        
        assert result is True

    def test_get_transformation_summary(self, data_ops):
        """Prueba la generación del resumen de transformaciones"""
        # Simular algunas transformaciones
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