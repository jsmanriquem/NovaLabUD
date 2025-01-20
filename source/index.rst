Documentación de ``NovaLab``
============================

Hola, esta es la documentación de la aplicación: ``NovaLab``. Esta es una aplicación diseñada para procesar, analizar y visualizar datos de los experimentos de *'Caída libre'* y *'Ley de Hooke'*, que junto a ello, se muestra de forma amigable la teoría de los experimentos.

Nace como un software diseñado de forma amigable para su público dirigido, el cual son estudiantes de primeros semestres del Programa Académico de Física de la Facultad de Ciencias Matemáticas y Naturales de la Universidad Distrital Francisco José de Caldas.

Instalación
------------

Configuración del Entorno
~~~~~~~~~~~~~~~~~~~~~~~~~

La configuración del entorno de desarrollo es un paso fundamental en cualquier proyecto de software, ya que garantiza que los desarrolladores cuenten con las herramientas, bibliotecas y configuraciones necesarias para trabajar de manera eficiente y organizada. Este proceso incluye la instalación de lenguajes de programación, la gestión de dependencias, la integración de bases de datos, el uso de herramientas de control de versiones como Git, y la configuración de entornos virtuales para aislar proyectos. Un entorno de desarrollo bien configurado no solo reduce errores y problemas técnicos, sino que también facilita la colaboración en equipo y asegura la reproducibilidad del proyecto en diferentes sistemas.

Requisitos del Sistema
~~~~~~~~~~~~~~~~~~~~~~

- **Sistema Operativo**: Windows o Linux.
- **Python**: Versión 3.8 o superior.
- **Espacio en Disco**: Mínimo 500 MB disponibles.
- **Memoria RAM**: Recomendado 4 GB o más.

Dependencias Necesarias
~~~~~~~~~~~~~~~~~~~~~~~

El software utiliza varias librerías de Python que deben ser instaladas antes de ejecutar la aplicación. A continuación, se detallan las principales:

- ``contourpy==1.3.1``: Para la creación de contornos en gráficas.
- ``cycler==0.12.1``: Para la gestión de estilos y colores en gráficas.
- ``fonttools==4.55.3``: Para manipulación de fuentes.
- ``joblib==1.4.2``: Para la serialización eficiente de objetos.
- ``kiwisolver==1.4.8``: Para la resolución de sistemas de ecuaciones en gráficos.
- ``matplotlib==3.10.0``: Para la generación de gráficas.
- ``numpy==2.2.2``: Para cálculos matemáticos y operaciones con matrices.
- ``packaging==24.2``: Para la gestión de versiones.
- ``pandas==2.2.3``: Para manipulación y análisis de datos.
- ``pillow==11.1.0``: Para la manipulación de imágenes.
- ``PyMuPDF==1.25.2``: Para la visualización de documentos PDF.
- ``pyparsing==3.2.1``: Para análisis de texto y sintaxis.
- ``python-dateutil==2.9.0.post0``: Para trabajar con fechas y horas.
- ``pytz==2024.2``: Para manejo de zonas horarias.
- ``scikit-learn==1.6.1``: Para regresión y análisis estadístico.
- ``scipy==1.15.1``: Para interpolaciones y funciones matemáticas avanzadas.
- ``six==1.17.0``: Para compatibilidad entre Python 2 y 3.
- ``threadpoolctl==3.5.0``: Para la gestión de hilos en operaciones paralelas.
- ``tk==0.1.0``: Para la interfaz gráfica de usuario.
- ``tzdata==2024.2``: Para gestión de zonas horarias.

Instrucciones de Instalación
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Instalación de Python**:
   - Descargue e instale Python desde su sitio oficial.
   - Durante la instalación, asegúrese de seleccionar la opción ``Add Python to PATH``.

2. **Clonación del Repositorio y Creación de un Entorno Virtual (Opcional pero Recomendado)**:
   - Clone el repositorio ejecutando el siguiente comando:
     ```
     git clone https://github.com/jsmanriquem/NovaLabUD.git
     python -m venv NovaLabUD
     ```
   - Active el entorno virtual:
     - En Windows: ``NovaLabUD\Scripts\activate``
     - En macOS/Linux: ``source NovaLabUD/bin/activate``

3. **Instalación de Dependencias**:
   - Instale las dependencias necesarias ejecutando:
     ```
     pip install -r requirements.txt
     ```
   - Si el archivo ``requirements.txt`` no está disponible, instale manualmente las librerías listadas en la sección de dependencias:
     ```
     pip install contourpy==1.3.1 cycler==0.12.1 fonttools==4.55.3 joblib==1.4.2 kiwisolver==1.4.8 matplotlib==3.10.0 numpy==2.2.2 packaging==24.2 pandas==2.2.3 pillow==11.1.0 PyMuPDF==1.25.2 pyparsing==3.2.1 python-dateutil==2.9.0.post0 pytz==2024.2 scikit-learn==1.6.1 scipy==1.15.1 six==1.17.0 threadpoolctl==3.5.0 tk==0.1.0 tzdata==2024.2
     ```

4. **Ejecución del Software**:
   - Navegue al directorio donde se encuentra el archivo ``app.py``.
   - Ejecute el archivo principal con:
     ```
     python app.py
     ```

5. **Pruebas de Funcionamiento**:
   - Verifique que la aplicación se abra correctamente y que pueda cargar un archivo de datos.

Solución de Problemas Comunes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Error ``ModuleNotFoundError``**:
  - Asegúrese de que las dependencias estén instaladas correctamente.
  - Ejecute nuevamente:
    ```
    pip install -r requirements.txt
    ```

- **Problemas de Visualización de PDF**:
  - Verifique que ``PyMuPDF`` esté instalado y actualizado:
    ```
    pip install --upgrade pymupdf
    ```

- **No se Abre la Aplicación**:
  - Asegúrese de estar ejecutando el archivo correcto (``app.py``).
  - Verifique que Python esté correctamente instalado y configurado en el PATH del sistema.

.. toctree::
   :maxdepth: 1
   :caption: Manual de usuario
   :class: left-column

   interfaz_novalab
   procesamiento_datos
   analisis_datos
   graficador_manual
   miscelaneos

.. toctree::
   :maxdepth: 1
   :caption: Módulos (código)
   :class: right-column

   app
   data_operations
   regression_analysis
   graficador