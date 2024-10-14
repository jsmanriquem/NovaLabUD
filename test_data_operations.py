import pytest
import pandas as pd
from modules.data_operations import DataOperations

@pytest.fixture
def data_ops():
    """Fixture para DataOperations."""
    # Crea un DataFrame de ejemplo con duplicados
    sample_data = pd.DataFrame({
        'A': [1, 2, 2, None, 5],  # Duplicado en la segunda fila
        'B': [1, 2, 2, 2, None],
        'C': [10, 20, 20, 40, 50]  # Duplicado en la tercera fila
    })
    ops = DataOperations()
    ops.data = sample_data
    return ops

def test_remove_duplicates(data_ops):
    """Prueba para eliminar las filas duplicadas."""
    data_ops.remove_duplicates()
    assert len(data_ops.data) == 4  # Verifica que se haya eliminado una fila duplicada.

def test_normalize_data(data_ops):
    """Prueba para la normalización de los datos."""
    data_ops.normalize_data()
    # Verifica que los valores estén en el rango [0, 1]
    assert (data_ops.data >= 0).all().all() and (data_ops.data <= 1).all().all(), "Algunos valores no están en el rango [0, 1]."


def test_fill_null_with_mean(data_ops):
    """Prueba para rellenar valores nulos con la media."""
    data_ops.fill_null_with_mean()
    # Verifica que los valores nulos se hayan rellenado correctamente.
    assert data_ops.data['A'].isnull().sum() == 0
