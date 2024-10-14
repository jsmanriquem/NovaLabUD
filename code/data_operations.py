import pandas as pd
from tkinter import filedialog, messagebox

class DataOperations:
    """Clase para realizar operaciones de manipulación de datos con pandas.

    Esta clase permite cargar archivos de datos, procesar los datos cargados, 
    y realizar operaciones como eliminación de valores nulos, eliminación de duplicados,
    normalización de datos y relleno de valores nulos con la media.

    Attributes:
        data (DataFrame): El DataFrame que contiene los datos cargados.
    """

    def __init__(self):
        """Inicializa la clase DataOperations y establece el DataFrame de datos como None."""
        self.data = None

    def load_file(self, ui_callback):
        """Carga un archivo de datos desde el sistema de archivos.

        Permite seleccionar archivos CSV, TXT o Excel, y los carga en un DataFrame de pandas.
        Al finalizar la carga, llama a un callback de la interfaz de usuario para mostrar los datos.

        Args:
            ui_callback (callable): Función que se ejecuta para mostrar los datos cargados.
        
        Returns:
            bool: True si el archivo se carga correctamente, False en caso contrario.
        """
        file = filedialog.askopenfilename(filetypes=[("Archivos CSV", ".csv"), ("Archivos TXT", ".txt"), ("Archivos Excel", "*.xlsx *.xls")])
        
        if file:
            try:
                if file.endswith('.csv'):
                    self.data = pd.read_csv(file)
                elif file.endswith('.txt'):
                    self.data = pd.read_csv(file, delimiter='\t')
                else:
                    self.data = pd.read_excel(file)
                ui_callback(self.data)  # Llamar al callback de UI para mostrar los datos
                return True
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo. Detalles: {e}")
                return False
        return False

    def remove_null_values(self):
        """Elimina las filas con valores nulos del DataFrame.

        Muestra un mensaje de éxito si se eliminan las filas, o un mensaje de advertencia
        si no se han cargado datos previamente.
        """
        if self.data is not None:
            self.data.dropna(inplace=True)
            messagebox.showinfo("Éxito", "Se han eliminado las filas con valores nulos")
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")

    def remove_duplicates(self):
        """Elimina las filas duplicadas del DataFrame.

        Muestra un mensaje de éxito si se eliminan las filas duplicadas, o un mensaje de advertencia
        si no se han cargado datos previamente.
        """
        if self.data is not None:
            self.data.drop_duplicates(inplace=True)
            messagebox.showinfo("Éxito", "Se han eliminado las filas duplicadas")
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")

    def normalize_data(self):
        """Normaliza los datos numéricos del DataFrame."""
        if self.data is not None:
            for col in self.data.select_dtypes(include='number').columns:
                # Maneja los valores NaN
                if self.data[col].notnull().any():  # Asegúrate de que hay datos no nulos
                    min_val = self.data[col].min()
                    max_val = self.data[col].max()

                    # Evita la división por cero
                    if max_val != min_val:
                        self.data[col] = (self.data[col] - min_val) / (max_val - min_val)
                    else:
                        self.data[col] = 0  # Si todos los valores son iguales, asigna 0

        #Opcional: Rellenar NaN resultantes con 0 o mantener NaN dado que por el momento manejamos solo dos montajes de laboratorio.
            self.data.fillna(0, inplace=True)  # Descomentar si quieres reemplazar NaN con 0

            messagebox.showinfo("Éxito", "Datos normalizados correctamente")
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")

    def fill_null_with_mean(self):
        """Rellena los valores nulos del DataFrame con la media de cada columna.

        Muestra un mensaje de éxito si se rellenan los valores, o un mensaje de advertencia
        si no se han cargado datos previamente.
        """
        if self.data is not None:
            self.data.fillna(self.data.mean(), inplace=True)
            messagebox.showinfo("Éxito", "Valores nulos rellenados con la media")
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")
