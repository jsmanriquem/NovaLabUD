import pandas as pd
from tkinter import filedialog, messagebox
from datetime import datetime

class DataOperations:
    """Clase para realizar operaciones de manipulación de datos con pandas.

    Esta clase permite cargar archivos de datos, procesar los datos cargados, 
    y realizar operaciones como eliminación de valores nulos, eliminación de duplicados,
    normalización de datos y relleno de valores nulos con la media.

    Attributes:
        data (DataFrame): El DataFrame que contiene los datos cargados.
        original_data (DataFrame): Copia de los datos originales sin procesar.
        transformation_history (list): Historial de transformaciones aplicadas.
    """

    def __init__(self):
        """Inicializa la clase DataOperations."""
        self.data = None
        self.original_data = None
        self.transformation_history = []

    def load_file(self):
        """Carga un archivo de datos desde el sistema de archivos."""
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
                
                # ui_callback(self.data)
                messagebox.showinfo("Éxito", "Archivo cargado correctamente")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo. Detalles: {e}")
                return False
        return False

    def _add_to_history(self, operation_name, details=None):
        """Agrega una operación al historial de transformaciones."""
        self.transformation_history.append({
            'operation': operation_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'details': details,
            'rows_affected': len(self.data)
        })

    def remove_null_values(self):
        """Elimina las filas con valores nulos del DataFrame."""
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
        """Elimina las filas duplicadas del DataFrame."""
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
        """Normaliza los datos numéricos del DataFrame."""
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
        """Rellena los valores nulos con la media de cada columna."""
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
        """Exporta los datos transformados a un archivo en formato XLSX, CSV o TXT.
    
            Returns:
            bool: True si la exportación fue exitosa, False en caso contrario.
        """
        if self.data is None:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return False

    # Crear un DataFrame con el resumen de transformaciones
        transformation_summary = pd.DataFrame(self.transformation_history)
    
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
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
        """Retorna un resumen de las transformaciones realizadas."""
        if not self.transformation_history:
            return "No se han realizado transformaciones"
        
        summary = "Resumen de transformaciones:\n\n"
        for i, trans in enumerate(self.transformation_history, 1):
            summary += f"{i}. {trans['operation']}\n"
            summary += f"   Fecha: {trans['timestamp']}\n"
            summary += f"   Detalles: {trans['details']}\n"
            summary += f"   Filas afectadas: {trans['rows_affected']}\n\n"
        
        return summary
