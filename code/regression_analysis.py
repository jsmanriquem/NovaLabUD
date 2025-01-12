import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from tkinter import simpledialog, messagebox
import tkinter as tk

class DataOps:
    """Clase auxiliar que contiene el atributo 'data'."""
    def __init__(self, data):
        self.data = data

class RegressionAnalysis:
    """Clase para realizar diferentes tipos de análisis de regresión e interpolación.

    Esta clase proporciona métodos para regresión lineal, regresión polinómica e interpolación
    de Lagrange, junto con visualización de resultados y cálculo de métricas.

    Args:
        data_ops: Objeto de operaciones de datos que contiene el conjunto de datos a analizar

    Atributos:
        data_ops: Objeto de operaciones de datos que contiene el conjunto de datos
    """
    
    def __init__(self, data_ops):
        """Inicializa la clase con operaciones de datos.
        
        Si el argumento es un DataFrame, crea un objeto `data_ops` y asigna el DataFrame a su atributo `data`.
        Si no, no hace nada.

        Args:
            data_ops: Un objeto que puede ser un DataFrame o una clase con atributo `data`.
        """
        if isinstance(data_ops, pd.DataFrame):
            # Si el argumento es un DataFrame, crea un objeto 'data_ops' con el DataFrame
            self.data_ops = DataOps(data_ops)  # Crea el objeto 'data_ops' y asigna el DataFrame a su atributo 'data'
        elif hasattr(data_ops, 'data'):
            # Si el argumento ya es un objeto con el atributo 'data', simplemente lo asigna
            self.data_ops = data_ops
        else:
            self.data_ops = None  # No hace nada si no es un DataFrame ni un objeto con el atributo 'data'

    def calculate_metrics(self, y_true, y_pred):
        """Calcula métricas de regresión entre valores reales y predichos.
        
        Args:
            y_true (array-like): Valores reales
            y_pred (array-like): Valores predichos
            
        Returns:
            tuple: Métricas R-cuadrado, Error Absoluto Medio y Error Cuadrático Medio
        """
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        return r2, mae, mse

    def format_equation(self, coefficients):
        """Formatea los coeficientes de regresión en una ecuación legible.
        
        Args:
            coefficients (array-like): Coeficientes de regresión
            
        Returns:
            str: Cadena de texto con la ecuación formateada
        """
        if len(coefficients) == 2:  # Regresión lineal
            return f'y = {coefficients[0]:.4f}x + {coefficients[1]:.4f}'
        else:  # Regresión polinómica
            eq = 'y = '
            for i, coef in enumerate(coefficients):
                power = len(coefficients) - i - 1
                if power > 1:
                    eq += f'{coef:.4f}x^{power} + '
                elif power == 1:
                    eq += f'{coef:.4f}x + '
                else:
                    eq += f'{coef:.4f}'
            return eq

    def linear_regression(self, var_x, var_y, ax1=None, return_metrics=False):
        """Realiza análisis de regresión lineal y visualización.
        
        Args:
            var_x (str): Nombre de la columna de variable independiente
            var_y (str): Nombre de la columna de variable dependiente
            ax1 (matplotlib.axes.Axes, optional): Eje de la gráfica donde se va a dibujar la regresión
            return_metrics (bool, optional): Si es True, devuelve solo la ecuación y métricas, 
                                              si es False, dibuja la regresión sobre el gráfico.
            
        Advertencias:
            Muestra diálogo de advertencia si no se seleccionan variables o no hay datos cargados.
        """
        if self.data_ops.data is not None and var_x in self.data_ops.data.columns and var_y in self.data_ops.data.columns:
            x = self.data_ops.data[var_x].values.reshape(-1, 1)
            y = self.data_ops.data[var_y].values
            model = LinearRegression()
            model.fit(x, y)
            y_pred = model.predict(x)

            # Si se indica que no se devuelvan solo métricas, graficar la regresión
            if not return_metrics:
                if ax1 is not None:
                    # Graficar los puntos y la línea de regresión en el gráfico existente
                    ax1.plot(x, y_pred, color='red', label='Regresión', linewidth=2)
                    ax1.legend()

            # Calcular métricas y formatear la ecuación
            r2, mae, mse = self.calculate_metrics(y, y_pred)
            metrics_text = f'R² = {r2:.4f}\nMAE = {mae:.4f}\nMSE = {mse:.4f}'
            equation = self.format_equation([model.coef_[0], model.intercept_])

            # Si se indican métricas, devolver la ecuación y las métricas
            if return_metrics:
                # Crear figura con dos subplots
                fig, (ax1, ax2) = plt.subplots(2, 1, height_ratios=[3, 1], figsize=(10, 8))
                fig.suptitle('Análisis de Regresión Lineal', fontsize=14)

                # Graficar regresión
                ax1.scatter(x, y, color='blue', label='Datos')
                ax1.plot(x, y_pred, color='red', label='Regresión')
                ax1.set_xlabel(var_x)
                ax1.set_ylabel(var_y)
                ax1.legend()

                # Mostrar métricas y ecuación
                ax2.text(0.5, 0.5, f'{equation}\n\n{metrics_text}',
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform=ax2.transAxes,
                        bbox=dict(facecolor='white', alpha=0.8))
                ax2.axis('off')

                plt.tight_layout()
                return fig
            else:
                # Devolver los datos de la regresión para ser graficados
                return x, y_pred, equation

        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables primero")

    def polynomial_regression(self, var_x, var_y, ax1=None, return_metrics=False):
        """Realiza análisis de regresión polinómica y visualización.
        
        Args:
            var_x (str): Nombre de la columna de variable independiente 
            var_y (str): Nombre de la columna de variable dependiente
            ax1 (matplotlib.axes.Axes, optional): Eje de la gráfica donde se va a dibujar la regresión
            return_metrics (bool, optional): Si es True, devuelve solo la ecuación y métricas, 
                                            si es False, dibuja la regresión sobre el gráfico.
        
        Advertencias:
            - Muestra diálogo de advertencia si no se seleccionan variables o no hay datos cargados
            - Diálogo para ingresar el grado del polinomio (1-10)
        
        Salida:
            - Gráfico de dispersión con curva de regresión polinómica
            - Cuadro de texto con ecuación polinómica y métricas
        """
        if self.data_ops.data is not None and var_x and var_y:
            degree = simpledialog.askinteger("Grado del Polinomio", 
                                        "Ingresa el grado del polinomio:", 
                                        minvalue=1, maxvalue=10)

            if degree is not None:
                x = self.data_ops.data[var_x]
                y = self.data_ops.data[var_y]
                coef = np.polyfit(x, y, degree)
                poly_eq = np.poly1d(coef)

                # Solo generar los puntos ajustados para el rango de datos original
                y_fit = poly_eq(x)

                # Si se indica que no se devuelvan solo métricas, graficar la regresión
                if not return_metrics:
                    if ax1 is not None:
                        # Graficar los puntos y la línea de regresión en el gráfico existente
                        ax1.scatter(x, y, color='blue', label='Datos')
                        ax1.plot(x, y_fit, color='red', label=f'Regresión Polinómica (Grado {degree})')
                        ax1.legend()

                # Calcular y devolver las métricas si se solicitan
                r2, mae, mse = self.calculate_metrics(y, y_fit)
                equation = self.format_equation(coef)

                if return_metrics:
                    x_fit = np.linspace(x.min(), x.max(), 100)
                    y_fit = poly_eq(x_fit)

                    # Crear figura con dos subplots
                    fig, (ax1, ax2) = plt.subplots(2, 1, height_ratios=[3, 1], figsize=(10, 8))
                    fig.suptitle(f'Análisis de Regresión Polinómica (Grado {degree})', fontsize=14)

                    # Graficar regresión
                    ax1.scatter(x, y, color='blue', label='Datos')
                    ax1.plot(x_fit, y_fit, color='red', 
                            label=f'Regresión Polinómica')
                    ax1.set_xlabel(var_x)
                    ax1.set_ylabel(var_y)
                    ax1.legend()

                    # Calcular y mostrar métricas
                    r2, mae, mse = self.calculate_metrics(y, poly_eq(x))
                    metrics_text = f'R² = {r2:.4f}\nMAE = {mae:.4f}\nMSE = {mse:.4f}'
                    equation = self.format_equation(coef)

                    # Mostrar métricas y ecuación
                    ax2.text(0.5, 0.5, f'{equation}\n\n{metrics_text}',
                            horizontalalignment='center',
                            verticalalignment='center',
                            transform=ax2.transAxes,
                            bbox=dict(facecolor='white', alpha=0.8))
                    ax2.axis('off')

                    plt.tight_layout()
                    return fig
                else:
                    return x, y_fit, equation

        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables para la regresión")

    def interpolation(self, var_x, var_y, ax1=None, return_metrics=False):
        """Realiza interpolación de Lagrange y visualización.

        Args:
            var_x (str): Nombre de la columna de variable independiente
            var_y (str): Nombre de la columna de variable dependiente
            ax1 (matplotlib.axes.Axes, optional): Eje de la gráfica donde se va a dibujar la interpolación
            return_metrics (bool, optional): Si es True, devuelve solo el polinomio de interpolación y métricas,
                                            si es False, dibuja la interpolación sobre el gráfico.

        Advertencias:
            Muestra diálogo de advertencia si no se seleccionan variables o no hay datos cargados.
            Diálogo para ingresar el grado de interpolación (1-10).
            Advertencia si no hay suficientes puntos para el grado seleccionado.

        Salida:
            - Gráfico de dispersión con curva de interpolación (si return_metrics es False)
            - Cuadro de texto con polinomio de Lagrange y métricas
        """
        if self.data_ops.data is not None and var_x and var_y:
            degree = simpledialog.askinteger("Grado del Polinomio", 
                                            "Ingresa el grado del polinomio:", 
                                            minvalue=1, maxvalue=10)

            if degree is not None:
                x = self.data_ops.data[var_x].values
                y = self.data_ops.data[var_y].values

                if len(x) < degree + 1:
                    messagebox.showwarning("Advertencia", 
                                        "No hay suficientes puntos para el grado seleccionado")
                    return

                # Selección de puntos: primer, intermedio(s) y último
                indices = np.linspace(0, len(x) - 1, degree + 1, dtype=int)
                x_points = x[indices]
                y_points = y[indices]

                # Generación de la función de interpolación de Lagrange
                def lagrange_interpolation_expression(x_points, y_points):
                    n = len(x_points)
                    terms = []
                    for i in range(n):
                        numerator = []
                        denominator = 1
                        for j in range(n):
                            if i != j:
                                numerator.append(f"(x - {x_points[j]:.4f})")
                                denominator *= (x_points[i] - x_points[j])
                        term = f"({y_points[i]:.4f} / {denominator:.4f}) * " + " * ".join(numerator)
                        terms.append(term)
                    return "P(x) = " + " + ".join(terms)

                def lagrange_interpolation(x_eval, x_points, y_points):
                    n = len(x_points)
                    result = 0
                    for i in range(n):
                        term = y_points[i]
                        for j in range(n):
                            if i != j:
                                term *= (x_eval - x_points[j]) / (x_points[i] - x_points[j])
                        result += term
                    return result

                # Generar los datos interpolados
                y_interpolated = np.array([lagrange_interpolation(x_val, x_points, y_points) for x_val in x])

                # Generar expresión algebraica
                expression = lagrange_interpolation_expression(x_points, y_points)

                # Si no se requieren solo métricas, graficar la interpolación
                if not return_metrics:
                    if ax1 is not None:
                        ax1.scatter(x, y, color='blue', label='Datos originales')
                        ax1.plot(x, y_interpolated, color='red', label='Interpolación')
                        ax1.set_xlabel(var_x)
                        ax1.set_ylabel(var_y)
                        ax1.legend()

                # Calcular métricas
                r2, mae, mse = self.calculate_metrics(y, y_interpolated)
                metrics_text = f'R² = {r2:.4f}\nMAE = {mae:.4f}\nMSE = {mse:.4f}'

                # Si se indican métricas, devolver la ecuación y las métricas
                if return_metrics:
                    # Crear figura con dos subplots
                    fig, (ax1, ax2) = plt.subplots(2, 1, height_ratios=[3, 1], figsize=(10, 8))
                    fig.suptitle(f'Interpolación de Lagrange (Grado {degree})', fontsize=14)

                    # Graficar interpolación
                    ax1.scatter(x, y, color='blue', label='Datos originales')
                    ax1.plot(x, y_interpolated, color='red', label='Interpolación')
                    ax1.set_xlabel(var_x)
                    ax1.set_ylabel(var_y)
                    ax1.legend()

                    # Mostrar métricas y ecuación
                    ax2.text(0.5, 0.5, f'{expression}\n\n{metrics_text}',
                            horizontalalignment='center',
                            verticalalignment='center',
                            transform=ax2.transAxes,
                            bbox=dict(facecolor='white', alpha=0.8), fontsize=8, wrap=True)
                    ax2.axis('off')

                    plt.tight_layout()
                    return fig
                else:
                    return x, y_interpolated, expression

        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables primero")
