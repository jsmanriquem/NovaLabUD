import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from tkinter import simpledialog, messagebox
import tkinter as tk

class RegressionAnalysis:
    """Clase para realizar análisis de regresión.

    Esta clase proporciona métodos para realizar análisis de regresión lineal
    y polinómica, así como interpolación de datos. Las métricas de desempeño
    se pueden calcular y mostrar en una interfaz gráfica.

    Attributes:
        data_ops (DataOperations): Objeto que contiene los datos necesarios
                                    para el análisis de regresión.
    """
  
