import tkinter as tk
from tkinter import ttk
from data_operations import DataOperations
from modules.ui_components import UIComponents
# from modules.regression_analysis import RegressionAnalysis

class LaboratorySoftware:
    """Clase principal del Software de Laboratorio.

    Esta clase se encarga de crear la interfaz gráfica para leer y procesar datos.
    """
    
    def __init__(self) -> None:
        """Inicializa la clase y configura la ventana principal del software.

        Crea instancias de las clases DataOperations, UIComponents y RegressionAnalysis.
        """
        self.root = tk.Tk()
        self.root.title("Software de Laboratorio - Leer y Procesar Datos")
        self.root.geometry("1000x600")
        self.root.config(bg="white")

        self.data_ops = DataOperations()
        self.ui = UIComponents(self.root, self.data_ops)
        # self.regression = RegressionAnalysis(self.data_ops)

        self.setup_ui()

    def setup_ui(self) -> None:
        """Configura la interfaz de usuario creando componentes visuales.

        Este método inicializa la barra de progreso y la barra de navegación.
        
        Warnings:
            Asegúrate de que los componentes de la interfaz de usuario se inicialicen correctamente.
        
        Output:
            None
        """
        self.ui.create_progress_bar()
        self.ui.create_navbar(self.show_read_data, self.show_process_data, self.show_regressions)

    def show_read_data(self) -> None:
        """Muestra la ventana para leer datos.

        Este método se llama cuando se selecciona la opción para leer datos en la barra de navegación.
        
        Output:
            None
        """
        self.ui.show_read_data_window()

    def show_process_data(self) -> None:
        """Muestra la ventana para procesar datos.

        Este método se llama cuando se selecciona la opción para procesar datos en la barra de navegación.
        
        Output:
            None
        """
        self.ui.show_process_data_window()

    def show_regressions(self) -> None:
        """Muestra la ventana para realizar regresiones.

        Este método se llama cuando se selecciona la opción para realizar regresiones en la barra de navegación.
        
        Output:
            None
        """
        self.ui.show_regressions_window(self.regression)

    def run(self) -> None:
        """Ejecuta el bucle principal de la interfaz gráfica.

        Este método mantiene la ventana del software en funcionamiento hasta que se cierra.
        
        Output:
            None
        """
        self.root.mainloop()

if __name__ == "__main__":
    app = LaboratorySoftware()
    app.run()
