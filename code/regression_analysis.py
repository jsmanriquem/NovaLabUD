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

    def __init__(self, data_ops):
        """Inicializa la clase con el objeto de operaciones de datos.

        Args:
            data_ops (DataOperations): Objeto que contiene los datos necesarios
                                        para el análisis.
        """
        self.data_ops = data_ops

    def calculate_metrics(self, y_true, y_pred):
        """Calcula las métricas de regresión.

        Args:
            y_true (array-like): Valores reales.
            y_pred (array-like): Valores predichos por el modelo.

        Returns:
            tuple: (R², MAE, MSE)

        Warnings:
            Asegúrate de que las dimensiones de `y_true` y `y_pred` coincidan.
        """
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        return r2, mae, mse

    def show_metrics(self, r2, mae, mse):
        """Muestra las métricas de regresión en una ventana de Tkinter.

        Args:
            r2 (float): Coeficiente de determinación R².
            mae (float): Error absoluto medio.
            mse (float): Error cuadrático medio.
        """
        metrics_window = tk.Toplevel()
        metrics_window.title("Métricas de Regresión")

        lbl_r2 = tk.Label(metrics_window, text=f"R²: {r2:.4f}", font=("Helvetica", 14))
        lbl_r2.pack(pady=5)

        lbl_mae = tk.Label(metrics_window, text=f"MAE: {mae:.4f}", font=("Helvetica", 14))
        lbl_mae.pack(pady=5)

        lbl_mse = tk.Label(metrics_window, text=f"MSE: {mse:.4f}", font=("Helvetica", 14))
        lbl_mse.pack(pady=5)

    def linear_regression(self, var_x, var_y):
        """Realiza una regresión lineal.

        Args:
            var_x (str): Nombre de la variable independiente.
            var_y (str): Nombre de la variable dependiente.

        Warnings:
            Si `data_ops.data` es None o las variables no están seleccionadas,
            se mostrará una advertencia.
        """
        if self.data_ops.data is not None and var_x and var_y:
            x = self.data_ops.data[var_x].values.reshape(-1, 1)
            y = self.data_ops.data[var_y].values
            model = LinearRegression()
            model.fit(x, y)
            y_pred = model.predict(x)
            plt.scatter(x, y, color='blue')
            plt.plot(x, y_pred, color='red')
            plt.xlabel(var_x)
            plt.ylabel(var_y)
            plt.title('Regresión Lineal')
            plt.show()

            r2, mae, mse = self.calculate_metrics(y, y_pred)
            self.show_metrics(r2, mae, mse)
        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables primero")

    def polynomial_regression(self, var_x, var_y):
        """Realiza una regresión polinómica.

        Args:
            var_x (str): Nombre de la variable independiente.
            var_y (str): Nombre de la variable dependiente.

        Warnings:
            Si `data_ops.data` es None o las variables no están seleccionadas,
            se mostrará una advertencia.
            Si el grado del polinomio es None, no se realizará la regresión.
        """
        if self.data_ops.data is not None and var_x and var_y:
            degree = simpledialog.askinteger("Grado del Polinomio", "Ingresa el grado del polinomio:", minvalue=1, maxvalue=10)

            if degree is not None:
                x = self.data_ops.data[var_x]
                y = self.data_ops.data[var_y]
                coef = np.polyfit(x, y, degree)
                poly_eq = np.poly1d(coef)

                x_fit = np.linspace(x.min(), x.max(), 100)
                y_fit = poly_eq(x_fit)

                plt.scatter(x, y, color='blue', label='Datos')
                plt.plot(x_fit, y_fit, color='red', label=f'Regresión Polinómica de grado {degree}')
                plt.xlabel(var_x)
                plt.ylabel(var_y)
                plt.title("Regresión Polinómica")
                plt.legend()
                plt.show()

                r2, mae, mse = self.calculate_metrics(y, poly_eq(x))
                self.show_metrics(r2, mae, mse)
        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables para la regresión")

    def interpolation(self, var_x, var_y):
        """Realiza la interpolación lineal de los datos.

        Args:
            var_x (str): Nombre de la variable independiente.
            var_y (str): Nombre de la variable dependiente.

        Warnings:
            Si `data_ops.data` es None o las variables no están seleccionadas,
            se mostrará una advertencia.
        """
        if self.data_ops.data is not None and var_x and var_y:
            x = self.data_ops.data[var_x]
            y = self.data_ops.data[var_y]
            interp_func = interp1d(x, y, kind='linear', fill_value="extrapolate")

            x_new = np.linspace(x.min(), x.max(), 100)
            y_new = interp_func(x_new)

            plt.scatter(x, y, color='blue', label='Datos')
            plt.plot(x_new, y_new, color='green', label='Interpolación Lineal')
            plt.xlabel(var_x)
            plt.ylabel(var_y)
            plt.title("Interpolación de Datos")
            plt.legend()
            plt.show()
        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables para la interpolación")
