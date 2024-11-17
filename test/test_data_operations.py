import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
from data_operations import DataOperations

@pytest.fixture
def data_ops():
    """Fixture que proporciona una instancia de DataOperations."""
    return DataOperations()

# Pruebas parametrizadas para fill_null_with_mean
@pytest.mark.parametrize(
    "input_data, expected_filled", [
        (
            pd.DataFrame({"A": [1, np.nan, 3]}),
            pd.DataFrame({"A": [1.0, 2.0, 3.0]})
        ),
        (
            pd.DataFrame({"A": [np.nan, np.nan, 3]}),
            pd.DataFrame({"A": [3.0, 3.0, 3.0]})
        ),
        (
            pd.DataFrame({"A": [np.nan, np.nan, np.nan]}),
            pd.DataFrame({"A": [np.nan, np.nan, np.nan]})
        )
    ]
)
def test_fill_null_with_mean(data_ops, input_data, expected_filled):
    """Prueba parametrizada para rellenar nulos con la media."""
    data_ops.data = input_data
    data_ops.original_data = input_data.copy()
    
    data_ops.fill_null_with_mean()
    
    pd.testing.assert_frame_equal(data_ops.data, expected_filled)

# Pruebas parametrizadas para normalize_data
@pytest.mark.parametrize(
    "input_data, expected_min, expected_max", [
        (
            pd.DataFrame({"A": [1, 2, 3, 4]}),
            0,
            1
        ),
        (
            pd.DataFrame({"A": [10, 20, 30, 40]}),
            0,
            1
        ),
        (
            pd.DataFrame({"A": [5, 5, 5, 5]}),
            0,
            0
        ),
        (
            pd.DataFrame({"A": [1, np.nan, 3, 4]}),
            0,
            1
        )
    ]
)
def test_normalize_data(data_ops, input_data, expected_min, expected_max):
    """Prueba parametrizada para la normalización de datos numéricos."""
    data_ops.data = input_data
    data_ops.original_data = input_data.copy()
    
    data_ops.normalize_data()
    
    # Verificar valores mínimos y máximos después de la normalización
    if not input_data['A'].dropna().empty:  # Solo validar si hay valores numéricos
        assert data_ops.data['A'].min() == expected_min
        assert data_ops.data['A'].max() == expected_max
    else:
        assert data_ops.data['A'].isnull().all()

# Pruebas parametrizadas para remove_null_values
@pytest.mark.parametrize(
    "input_data, expected_output", [
        (
            pd.DataFrame({"A": [1, None, 3], "B": [4, 5, None]}),
            pd.DataFrame({"A": [1], "B": [4]})
        ),
        (
            pd.DataFrame({"A": [None, None, None], "B": [None, None, None]}),
            pd.DataFrame(columns=["A", "B"])
        ),
        (
            pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}),
            pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        )
    ]
)
def test_remove_null_values(data_ops, input_data, expected_output):
    """Prueba parametrizada para eliminar valores nulos."""
    data_ops.data = input_data
    data_ops.original_data = input_data.copy()
    
    data_ops.remove_null_values()
    
    # Ignorar diferencias en tipos de datos
    pd.testing.assert_frame_equal(data_ops.data, expected_output, check_dtype=False)

# Pruebas parametrizadas para remove_duplicates
@pytest.mark.parametrize(
    "input_data, expected_output", [
        (
            pd.DataFrame({"A": [1, 2, 2, 4], "B": [5, 6, 6, 8]}),
            pd.DataFrame({"A": [1, 2, 4], "B": [5, 6, 8]})
        ),
        (
            pd.DataFrame({"A": [1, 1, 1], "B": [2, 2, 2]}),
            pd.DataFrame({"A": [1], "B": [2]})
        ),
        (
            pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}),
            pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        )
    ]
)
def test_remove_duplicates(data_ops, input_data, expected_output):
    """Prueba parametrizada para eliminar duplicados."""
    data_ops.data = input_data
    data_ops.original_data = input_data.copy()
    
    data_ops.remove_duplicates()
    
    # Comparar los valores sin tener en cuenta los índices
    pd.testing.assert_frame_equal(data_ops.data.reset_index(drop=True), expected_output, check_dtype=False)