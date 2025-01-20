import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from tkinter import filedialog, messagebox
from datetime import datetime

class DataOperations:
    """
    Clase para realizar operaciones de manipulación y procesamiento de datos con pandas.
    Esta clase proporciona funcionalidades para cargar, procesar y exportar datos, manteniendo
    un registro de las transformaciones aplicadas y los datos originales.
    
    Las operaciones a realizar en dichas transformaciones son:
    - Eliminar valores nulos: Elimina las filas con valores nulos del DataFrame.
    - Eliminar duplicados: Elimina las filas duplicadas del DataFrame.
    - Normalizar datos: Normaliza los datos numéricos del DataFrame.
    - Rellenar valores nulos con la media: Rellena los valores nulos con la media de cada columna.

    Como se mencionó, la clase también proporciona una función para obtener un resumen de las transformaciones
    realizadas, que devuelve un string con el formato:

    Resumen de transformaciones:

    1. Eliminar valores nulos
       Fecha: 2024-01-01 12:00:00
       Detalles: None
       Filas afectadas: 100

    2. Normalizar datos
       Fecha: 2024-01-01 12:00:00
       Detalles: None
       Filas afectadas: 100

    3. Rellenar valores nulos con la media
       Fecha: 2024-01-01 12:00:00
       Detalles: None
       Filas afectadas: 100
    
    Attributos:
        data (pd.DataFrame): DataFrame actual con los datos procesados.
        original_data (pd.DataFrame): Copia de los datos originales sin procesar.
        transformation_history (list): Lista de diccionarios con el historial de transformaciones.
                                     Cada entrada contiene:
                                     - operation: nombre de la operación
                                     - timestamp: momento de la ejecución
                                     - details: detalles específicos
                                     - rows_affected: número de filas afectadas
    """

    def __init__(self):
        """
        Inicializa la clase DataOperations con un DataFrame vacío y una lista para registrar transformaciones.
        Aquí no realiza ninguna operación en los datos iniciales, sino que almacena los datos originales
        para poder realizar transformaciones posteriores.
        
        Parameters
        ----------
        None
        """
        self.data = None
        self.original_data = None
        self.transformation_history = []

    def load_file(self):
        """
        Permite al usuario seleccionar y cargar un archivo de datos, desde un archivo CSV, TXT o Excel.

        Parameters
        ----------
        file_path : str
            La ruta al archivo que se desea cargar.

        Returns
        -------
        pd.DataFrame
            DataFrame que contiene los datos cargados.

        Raises
        ------
        ValueError
            Si el archivo no tiene extensión .csv  .xlsx o .txt.
        """
        file = filedialog.askopenfilename(filetypes=[
            ("Archivos CSV", "*.csv"),
            ("Archivos TXT", "*.txt"),
            ("Archivos Excel", "*.xlsx *.xls")
        ])
        
        if file:
            try:
                if file.endswith('.csv'):
                    self.data = pd.read_csv(file)
                elif file.endswith('.txt'):
                    self.data = pd.read_csv(file, delimiter='\t')
                else:
                    self.data = pd.read_excel(file)
                
                self.original_data = self.data.copy()
                self.transformation_history = []
                
                messagebox.showinfo("Éxito", "Archivo cargado correctamente")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo. Detalles: {e}")
                return False
        return False

    def _add_to_history(self, operation_name, details=None):
        """
        Registra una operación en el historial de transformaciones.
        Se utiliza para mantener un seguimiento de las modificaciones realizadas.

        Parameters
        ----------
        operation_name : str
            Nombre de la operación realizada.
        details : str, optional
            Detalles adicionales sobre la operación.

        Returns
        -------
        None
        """
        self.transformation_history.append({
            'operation': operation_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'details': details,
            'rows_affected': len(self.data)
        })

    def remove_null_values(self):
        """
        Elimina las filas que contienen valores nulos del DataFrame.
        
        La operación se realiza in-place y se registra en el historial de transformaciones.
        Muestra un mensaje con el número de filas eliminadas.
        
        Requires:
            Datos cargados previamente (self.data no None).
        """
        if self.data is not None:
            rows_before = len(self.data)
            self.data.dropna(inplace=True)
            rows_removed = rows_before - len(self.data)
            
            self._add_to_history('remove_null_values', 
                               f'Eliminadas {rows_removed} filas con valores nulos')
            
            messagebox.showinfo("Éxito", 
                              f"Se han eliminado {rows_removed} filas con valores nulos")
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")

    def remove_duplicates(self):
        """
        Elimina las filas duplicadas del DataFrame, manteniendo la primera ocurrencia.
        
        Este método:
        - Identifica y elimina filas completamente duplicadas
        - Mantiene la primera ocurrencia de cada fila duplicada
        - Registra la operación en el historial
        - Muestra un mensaje con el número de filas eliminadas
        
        Returns:
            None
        
        Raises:
            No lanza excepciones directamente, pero muestra un messagebox de advertencia
            si self.data es None
        
        Notas:
            - La comparación de duplicados considera todas las columnas
            - La operación es irreversible
        """
        if self.data is not None:
            rows_before = len(self.data)
            self.data.drop_duplicates(inplace=True)
            rows_removed = rows_before - len(self.data)
            
            self._add_to_history('remove_duplicates',
                               f'Eliminadas {rows_removed} filas duplicadas')
            
            messagebox.showinfo("Éxito", 
                              f"Se han eliminado {rows_removed} filas duplicadas")
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")

    def normalize_data(self, selected_columns, method="Min-Max Scaling"):
        """
        Normaliza las columnas seleccionadas en el conjunto de datos utilizando el método especificado.

        Args:
            selected_columns (list): Lista de nombres de columnas a normalizar.
            method (str): Método de normalización a utilizar. Opciones:
                - "Min-Max Scaling": Escala los valores al rango [0, 1].
                - "Z-Score Scaling": Centraliza los datos eliminando la media y escalando a varianza unitaria.
                - "Max Abs Scaling": Escala los valores al rango [-1, 1] dividiendo por el valor absoluto máximo.

        Raises:
            ValueError: Si no se seleccionan columnas o si no hay datos cargados.

        Returns:
            int: Número de filas afectadas por la normalización.

        Efectos secundarios:
            - Actualiza el atributo `data` con los valores normalizados.
            - Registra la transformación en el historial de operaciones.
        """
        if not selected_columns:
            raise ValueError("Debe seleccionar al menos una columna para normalizar.")

        if self.data is None:
            raise ValueError("No hay datos cargados para normalizar.")

        original_data = self.data[selected_columns].copy()

        for col in selected_columns:
            if self.data[col].notnull().any():  # Solo aplica si la columna no está completamente vacía
                if method == "Min-Max Scaling":
                    min_val = self.data[col].min()
                    max_val = self.data[col].max()
                    if max_val != min_val:
                        self.data[col] = (self.data[col] - min_val) / (max_val - min_val)
                    else:
                        self.data[col] = 0

                elif method == "Z-Score Scaling":
                    mean_val = self.data[col].mean()
                    std_val = self.data[col].std()
                    if std_val != 0:
                        self.data[col] = (self.data[col] - mean_val) / std_val
                    else:
                        self.data[col] = 0

                elif method == "Max Abs Scaling":
                    max_abs_val = self.data[col].abs().max()
                    if max_abs_val != 0:
                        self.data[col] = self.data[col] / max_abs_val
                    else:
                        self.data[col] = 0

        affected_rows = (self.data[selected_columns] != original_data).any(axis=1).sum()
        self._add_to_history('normalize_data', f'Normalizadas las columnas {", ".join(selected_columns)} usando {method}')

        return affected_rows


    def fill_null_values(self, method='mean', degree=None, columns=None, n_neighbors=5):
        """
        Llena valores nulos en columnas seleccionadas utilizando diferentes métodos de imputación.

        Este método permite rellenar valores faltantes en un DataFrame utilizando diversas técnicas, 
        como imputación por media, interpolación lineal, interpolación polinómica, interpolación basada 
        en tiempo o imputación mediante K-Nearest Neighbors (KNN).

        Args:
            method (str, opcional): El método de imputación a utilizar. Por defecto es 'mean'.
                Métodos compatibles:
                - 'mean': Reemplaza valores nulos con la media de la columna.
                - 'linear': Usa interpolación lineal para llenar valores faltantes.
                - 'polynomial': Usa interpolación polinómica para llenar valores faltantes.
                - 'time': Usa interpolación basada en tiempo (como indica el nombre).
                - 'knn': Usa imputación por K-Nearest Neighbors para columnas numéricas.

            degree (int, opcional): El grado de la interpolación polinómica.
                Requerido cuando el método es 'polynomial'. Por defecto es None.

            columns (list, opcional): Lista de nombres de columnas a procesar.
                Si es None, se procesarán todas las columnas del DataFrame. Por defecto es None.

            n_neighbors (int, opcional): Número de vecinos a usar para la imputación KNN.
                Relevante solo cuando el método es 'knn'. Por defecto es 5.

        Raises:
            tkinter.messagebox.showwarning: Si no se cargan datos.
            tkinter.messagebox.showerror: Si no se cumplen los requisitos para la imputación KNN.

        Efectos secundarios:
            - Modifica el DataFrame subyacente in-place.
            - Muestra cuadros de mensaje con detalles de la imputación y éxito/error.
            - Registra el historial de imputación utilizando el método self._add_to_history.

        Notas:
            - Para la imputación KNN, solo se consideran columnas numéricas.
            - El método KNN normaliza los datos antes de la imputación para manejar diferentes escalas.
            - El método proporciona interacción con el usuario para seleccionar la cantidad de vecinos en KNN.

        Ejemplos:
            # Llenar valores nulos con la media
            df.fill_null_values(method='mean')

            # Llenar valores nulos con interpolación polinómica de grado 2
            df.fill_null_values(method='polynomial', degree=2)

            # Llenar valores nulos en columnas específicas usando KNN
            df.fill_null_values(method='knn', columns=['column1', 'column2'])
        """
   
        if self.data is None:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")
            return

        if columns is None:
            columns = self.data.columns  # Si no se pasan columnas, usar todas las columnas

        affected_rows = 0  # Contador de filas afectadas

        for column in columns:
            if column not in self.data.columns:
                continue  # Si la columna no existe en los datos, continuar con la siguiente

            if self.data[column].isnull().any():
                initial_null_count = self.data[column].isnull().sum()  # Contar los valores nulos antes

                if method == 'mean':
                    self.data[column] = self.data[column].fillna(self.data[column].mean())
                    nulls_filled = initial_null_count - self.data[column].isnull().sum()  # Calcular los nulos rellenados
                    affected_rows += nulls_filled  # Sumar al total de filas afectadas
                    detail = f"rellenados con la media en {column}"

                elif method == 'linear':
                    # Realizar la interpolación lineal y asignar el resultado a la columna
                    self.data[column] = self.data[column].interpolate(method='linear')

                    nulls_filled = initial_null_count - self.data[column].isnull().sum()
                    affected_rows += nulls_filled
                    detail = f"rellenados con interpolación lineal en {column}"

                    # Registrar el detalle y mostrar mensaje
                    self._add_to_history('fill_null_values', detail)
                    messagebox.showinfo("Éxito", f"{detail}. Se imputaron {nulls_filled} valores nulos.")

                elif method == 'polynomial' and degree is not None:
                    # Realizar la interpolación polinomial y asignar el resultado a la columna
                    self.data[column] = self.data[column].interpolate(method='polynomial', order=degree)

                    nulls_filled = initial_null_count - self.data[column].isnull().sum()
                    affected_rows += nulls_filled
                    detail = f"rellenados con interpolación polinomial en {column} de grado {degree}"

                    # Registrar el detalle y mostrar mensaje
                    self._add_to_history('fill_null_values', detail)
                    messagebox.showinfo("Éxito", f"{detail}. Se imputaron {nulls_filled} valores nulos.")

                elif method == 'knn':
                    from sklearn.impute import KNNImputer
                    import pandas as pd
                    from tkinter.simpledialog import askstring

                    # Pedir al usuario el número de vecinos cercanos
                    neighbors_input = askstring("Número de Vecinos", "Ingrese el número de vecinos cercanos (default: 5):")

                    # Validar entrada del usuario
                    try:
                        n_neighbors = int(neighbors_input) if neighbors_input else 5
                        if n_neighbors <= 0:
                            raise ValueError("El número de vecinos debe ser mayor a 0.")
                    except ValueError:
                        messagebox.showerror("Error", "Entrada inválida. Usando el valor predeterminado de 5 vecinos.")
                        n_neighbors = 5

                    # Selección de columnas relevantes para KNN
                    numeric_cols = [col for col in columns if pd.api.types.is_numeric_dtype(self.data[col])]
                    if len(numeric_cols) < 2:
                        messagebox.showerror(
                            "Error", "KNN requiere al menos 2 columnas numéricas correlacionadas para funcionar."
                        )
                        return

                    # Normalizar datos para evitar problemas de escala
                    normalized_data = self.data[numeric_cols].copy()
                    min_vals = normalized_data.min()
                    max_vals = normalized_data.max()

                    normalized_data = (normalized_data - min_vals) / (max_vals - min_vals)

                    # Contar valores nulos antes
                    nulls_before = self.data[numeric_cols].isnull().sum().sum()

                    # Aplicar KNNImputer
                    imputer = KNNImputer(n_neighbors=n_neighbors)
                    imputed_normalized_data = imputer.fit_transform(normalized_data)

                    # Desnormalizar los datos imputados
                    imputed_data = pd.DataFrame(
                        imputed_normalized_data, columns=numeric_cols
                    )
                    imputed_data = imputed_data * (max_vals - min_vals) + min_vals

                    # Actualizar el DataFrame con los valores imputados
                    for col in numeric_cols:
                        self.data[col] = imputed_data[col]

                    # Contar valores nulos después
                    nulls_after = self.data[numeric_cols].isnull().sum().sum()
                    nulls_filled = nulls_before - nulls_after
                    affected_rows += nulls_filled  # Sumar al total de filas afectadas

                    # Registrar el detalle y mostrar mensaje
                    detail = f"KNN aplicado en columnas: {', '.join(numeric_cols)} con {n_neighbors} vecinos"
                    self._add_to_history('fill_null_with_knn', detail)

                    messagebox.showinfo("Éxito", f"{detail}. Se imputaron {nulls_filled} valores nulos.")

        # Mostrar el número total de filas afectadas
        messagebox.showinfo("Éxito", f"Se afectaron {affected_rows} valores nulos en total.")

    def export_results(self):
        """
        Exporta los datos procesados y el historial de transformaciones.
        
        Formatos soportados:
        - Excel (.xlsx): Crea múltiples hojas para datos transformados, originales e historial
        - CSV (.csv): Crea archivos separados para cada tipo de dato
        - TXT (.txt): Similar a CSV pero con delimitador de tabulación
        
        Returns:
            bool: True si la exportación fue exitosa, False en otro caso.
        
        Notes:
            Para CSV y TXT, se crean archivos adicionales con sufijos '_original' 
            y '_transformaciones' para los datos originales y el historial.
        """
        if self.data is None:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return False

        # Crear un DataFrame con el resumen de transformaciones
        transformation_summary = pd.DataFrame(self.transformation_history)
        
        file_path = filedialog.asksaveasfilename(
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return False

        try:
            # Exportar a Excel
            if file_path.endswith('.xlsx'):
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    self.data.to_excel(writer, sheet_name='Datos Transformados', index=False)
                    if self.original_data is not None:
                        self.original_data.to_excel(writer, sheet_name='Datos Originales', index=False)
                    if self.transformation_history:
                        transformation_summary.to_excel(writer, 
                                                     sheet_name='Historial de Transformaciones',
                                                     index=False)
            
            # Exportar a CSV
            elif file_path.endswith('.csv'):
                # Exportar datos transformados
                self.data.to_csv(file_path, index=False)
                
                # Exportar datos originales y transformaciones en archivos separados
                base_path = file_path[:-4]  # Remover la extensión .csv
                if self.original_data is not None:
                    self.original_data.to_csv(f"{base_path}_original.csv", index=False)
                if self.transformation_history:
                    transformation_summary.to_csv(f"{base_path}_transformaciones.csv", index=False)
            
            # Exportar a TXT
            elif file_path.endswith('.txt'):
                # Exportar datos transformados
                self.data.to_csv(file_path, sep='\t', index=False)
                
                # Exportar datos originales y transformaciones en archivos separados
                base_path = file_path[:-4]  # Remover la extensión .txt
                if self.original_data is not None:
                    self.original_data.to_csv(f"{base_path}_original.txt", sep='\t', index=False)
                if self.transformation_history:
                    transformation_summary.to_csv(f"{base_path}_transformaciones.txt", sep='\t', index=False)
            
            mensaje = "Los resultados se han exportado correctamente"
            if file_path.endswith(('.csv', '.txt')) and (self.original_data is not None or self.transformation_history):
                mensaje += "\nSe han creado archivos adicionales para los datos originales y el historial de transformaciones"
            
            messagebox.showinfo("Éxito", mensaje)
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar los resultados: {str(e)}")
            return False

    def get_transformation_summary(self):
        """
        Genera un resumen textual de todas las transformaciones aplicadas.
        
        Returns:
            str: Resumen formateado del historial de transformaciones, incluyendo:
                - Número de operación
                - Tipo de operación
                - Fecha y hora
                - Detalles específicos
                - Número de filas afectadas
            
            Si no hay transformaciones, retorna un mensaje indicándolo.
        """
        if not self.transformation_history:
            return "No se han realizado transformaciones"
        
        summary = "Resumen de transformaciones:\n\n"
        for i, trans in enumerate(self.transformation_history, 1):
            summary += f"{i}. {trans['operation']}\n"
            summary += f"   Fecha: {trans['timestamp']}\n"
            summary += f"   Detalles: {trans['details']}\n"
            summary += f"   Filas afectadas: {trans['rows_affected']}\n\n"
        
        return summary