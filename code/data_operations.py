import pandas as pd
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

    def normalize_data(self):
        """
        Normaliza todas las columnas numéricas del DataFrame al rango [0,1].
        
        Para cada columna numérica, aplica la fórmula:
        normalized = (x - min) / (max - min)
        
        Si max = min, todos los valores se establecen en 0.
        Solo se normalizan columnas que contienen al menos un valor no nulo.
        
        Requires:
            Datos cargados previamente (self.data no None).
        """
        if self.data is not None:
            columns_normalized = []
            for col in self.data.select_dtypes(include='number').columns:
                if self.data[col].notnull().any():
                    min_val = self.data[col].min()
                    max_val = self.data[col].max()
                    
                    if max_val != min_val:
                        self.data[col] = (self.data[col] - min_val) / (max_val - min_val)
                        columns_normalized.append(col)
                    else:
                        self.data[col] = 0
            
            self._add_to_history('normalize_data',
                               f'Normalizadas las columnas: {", ".join(columns_normalized)}')
            
            messagebox.showinfo("Éxito", "Datos normalizados correctamente")
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")

    def fill_null_with_mean(self):
        """
        Rellena los valores nulos (NaN) en el DataFrame con la media de cada columna.
    
        Este método:
        - Calcula la media de cada columna numérica del DataFrame
        - Reemplaza todos los valores nulos con la media correspondiente
        - Registra la operación en el historial
        - Muestra un mensaje con el número de valores rellenados
        
        Returns:
            None
        
        Raises:
            No lanza excepciones directamente, pero muestra un messagebox de advertencia
            si self.data es None
        """
        if self.data is not None:
            nulls_before = self.data.isnull().sum().sum()
            self.data.fillna(self.data.mean(), inplace=True)
            nulls_filled = nulls_before - self.data.isnull().sum().sum()
            
            self._add_to_history('fill_null_with_mean',
                               f'Rellenados {nulls_filled} valores nulos con la media')
            
            messagebox.showinfo("Éxito", 
                              f"Se han rellenado {nulls_filled} valores nulos con la media")
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar los datos")

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