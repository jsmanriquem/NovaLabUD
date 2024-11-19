import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from tkinter import simpledialog, messagebox
import tkinter as tk

class RegressionAnalysis:
    def __init__(self, data_ops):
        self.data_ops = data_ops

    def calculate_metrics(self, y_true, y_pred):
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        return r2, mae, mse

    def format_equation(self, coefficients):
        """Formatea los coeficientes en una ecuación legible."""
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

    def linear_regression(self, var_x, var_y):
        if self.data_ops.data is not None and var_x and var_y:
            x = self.data_ops.data[var_x].values.reshape(-1, 1)
            y = self.data_ops.data[var_y].values
            model = LinearRegression()
            model.fit(x, y)
            y_pred = model.predict(x)

            # Crear figura con dos subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, height_ratios=[3, 1], figsize=(10, 8))
            fig.suptitle('Análisis de Regresión Lineal', fontsize=14)

            # Graficar regresión
            ax1.scatter(x, y, color='blue', label='Datos')
            ax1.plot(x, y_pred, color='red', label='Regresión')
            ax1.set_xlabel(var_x)
            ax1.set_ylabel(var_y)
            ax1.legend()

            # Calcular y mostrar métricas
            r2, mae, mse = self.calculate_metrics(y, y_pred)
            metrics_text = f'R² = {r2:.4f}\nMAE = {mae:.4f}\nMSE = {mse:.4f}'
            equation = self.format_equation([model.coef_[0], model.intercept_])
            
            # Mostrar métricas y ecuación
            ax2.text(0.5, 0.5, f'{equation}\n\n{metrics_text}',
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ax2.transAxes,
                    bbox=dict(facecolor='white', alpha=0.8))
            ax2.axis('off')

            plt.tight_layout()
            plt.show()
        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables primero")

    def polynomial_regression(self, var_x, var_y):
        if self.data_ops.data is not None and var_x and var_y:
            degree = simpledialog.askinteger("Grado del Polinomio", 
                                           "Ingresa el grado del polinomio:", 
                                           minvalue=1, maxvalue=10)

            if degree is not None:
                x = self.data_ops.data[var_x]
                y = self.data_ops.data[var_y]
                coef = np.polyfit(x, y, degree)
                poly_eq = np.poly1d(coef)

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
                plt.show()
        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables para la regresión")

    def interpolation(self, var_x, var_y):
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

                # Crear la función de interpolación de Lagrange
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

                # Generar los datos interpolados para todo el conjunto de datos
                y_interpolated = np.array([lagrange_interpolation(x_val, x_points, y_points) for x_val in x])

                # Generar expresión algebraica
                expression = lagrange_interpolation_expression(x_points, y_points)

                # Crear figura con dos subplots
                fig, (ax1, ax2) = plt.subplots(2, 1, height_ratios=[3, 1], figsize=(10, 8))
                fig.suptitle(f'Interpolación de Lagrange (Grado {degree})', fontsize=14)

                # Graficar interpolación
                ax1.scatter(x, y, color='blue', label='Datos originales')
                ax1.plot(x, y_interpolated, color='red', label='Interpolación')
                ax1.set_xlabel(var_x)
                ax1.set_ylabel(var_y)
                ax1.legend()

                # Calcular y mostrar métricas
                r2, mae, mse = self.calculate_metrics(y, y_interpolated)
                metrics_text = f'R² = {r2:.4f}\nMAE = {mae:.4f}\nMSE = {mse:.4f}'

                # Mostrar métricas y ecuación
                ax2.text(0.5, 0.5, f'{expression}\n\n{metrics_text}',
                         horizontalalignment='center',
                         verticalalignment='center',
                         transform=ax2.transAxes,
                         bbox=dict(facecolor='white', alpha=0.8), fontsize=8, wrap=True)
                ax2.axis('off')

                plt.tight_layout()
                plt.show()
        else:
            messagebox.showwarning("Advertencia", "Selecciona las variables primero")
