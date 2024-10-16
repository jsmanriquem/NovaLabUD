import numpy as np
import pandas as pd
import pytest
from .regression_analysis import RegressionAnalysis

# Clase simulada para DataOperations
class DataOperations:
    def __init__(self, data):
        self.data = data

def test_regression_analysis_initialization():
    # Preparar datos de prueba
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 5, 4, 5]
    })
    data_ops = DataOperations(data)

    # Inicializar la clase RegressionAnalysis
    regression_analysis = RegressionAnalysis(data_ops)

    # Verificar que la instancia se inicializa correctamente
    assert regression_analysis.data_ops is not None
    assert regression_analysis.data_ops.data.equals(data)

def test_calculate_metrics():
    # Datos de prueba
    y_true = np.array([2, 4, 5, 4, 5])
    y_pred = np.array([2.2, 3.8, 4.9, 4.1, 5.1])  # Predicciones de ejemplo

    # Inicializar la clase RegressionAnalysis sin datos
    regression_analysis = RegressionAnalysis(None)

    # Calcular métricas
    r2, mae, mse = regression_analysis.calculate_metrics(y_true, y_pred)

    # Verificar resultados
    assert isinstance(r2, float)
    assert isinstance(mae, float)
    assert isinstance(mse, float)

    # Verificar valores esperados (puedes ajustar estos valores)
    assert r2 >= 0  # Coeficiente de determinación R² debe ser >= 0
    assert mae >= 0  # MAE debe ser >= 0
    assert mse >= 0  # MSE debe ser >= 0
