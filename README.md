# Proyecto NovaLabUD

NovaLa es un proyecto que ha sido desarrollado en Python utilizando el paradigma de Programación Orientada a Objetos (POO), lo que facilita la gestión, reutilización y mantenimiento del código. El objetivo del proyecto es realizar simulaciones de experimentos físicos, como la caída libre, con la capacidad de generar gráficos e informes detallados sobre el comportamiento de los objetos bajo diversas condiciones.

A lo largo de este proyecto, se utilizan librerías de Python como pandas, numpy y matplotlib para el manejo de datos y la visualización gráfica, y scipy para la interpolación y otros análisis matemáticos. El código está diseñado para ser fácilmente extensible y configurable, permitiendo a los usuarios modificar parámetros de los experimentos. Está diseñado para ser fácil de usar, ofreciendo una experiencia intuitiva para trabajar con datos científicos en diversas áreas.

## Authors

- [@Laura Viviana Oliveros](https://www.github.com/octokatherine)
- [@Julián Armando Áros](https://www.github.com/octokatherine)
- [@Andrés Fernando Gómez](https://www.github.com/octokatherine)
- [@Laura Carolina Triana](https://www.github.com/octokatherine)
- [@Juan Sebastian Manrique](https://www.github.com/octokatherine)
- [@georgfis](https://www.github.com/georgfis)

### Mención Especial, Maestro Andrés Vasco

## Funcionalidades de la aplicación:

### Procesamiento de Datos:
Nuestra aplicación está diseñada para simplificar y optimizar el manejo de datos. Ofrecemos herramientas integradas para:

- Carga de datos: Compatible con diversos formatos (CSV, JSON, Excel, entre otros).
- Preprocesamiento: Limpieza de datos, detección y tratamiento de valores nulos, normalización y escalado.
- Análisis exploratorio: Imputación y transformación básica de los datos.



### Ajuste de Modelos:
La app incluye funcionalidades avanzadas para entrenar y ajustar modelos de aprendizaje automático:

- Selección de modelos: Acceso a algoritmos predefinidos como regresión lineal, polinómicas del grado deseado e interpolación y sus respectivas métricas. 



### Graficadora:
La visualización de datos y resultados es fundamental, y nuestra app incluye una herramienta de graficado robusta:

- Gráficos predefinidos: Histogramas, gráficos de dispersión, diagramas de caja, entre otros.
- Personalización: Opciones para modificar colores, títulos, etiquetas y estilos.
- Interactividad: Permite explorar los gráficos con zoom, selección de regiones y exportación en formatos como PNG o SVG.

## Finalidad de la app:
Esta aplicación busca ofrecer una herramienta a los estudiantes de física de los primeros semestres, para importar los datos de laboratorio y obtener facilmente los ajustes y su vizualización. Tambien se incluye pestañas con la teoría correspondiente a los fenomenos físicos analizados.

### Metodología de programación: POO  (Programación Orientada a Objetos)

###  Lenguaje de programación  utilizado: Python

## Estructura del Proyecto

La estructura del repositorio es la siguiente:


## Librerías Utilizadas

### Librerías para Manejo de Datos
- **pandas**: Proporciona estructuras de datos y herramientas de análisis, esenciales para manejar la entrada de datos en experimentos y las simulaciones.
- **numpy**: Utilizado para realizar operaciones matemáticas y manejar arreglos numéricos de manera eficiente.
- **datetime**: Se usa para gestionar la temporalidad en las simulaciones y registrar las fechas de ejecución.
- **pickle**: Se emplea para guardar y cargar configuraciones de simulaciones o resultados previos.

### Librerías para Análisis y Visualización
- **matplotlib**: Se usa para generar gráficos interactivos de los resultados de las simulaciones, tales como la velocidad, la distancia y el tiempo en experimentos de caída libre.
- **scipy**: Utiliza herramientas como `interp1d` para realizar interpolación de los datos obtenidos en las simulaciones.

## Instalación

Clonación del repositorio

```bash
  git clone repositorio
```

Intrucción de crear el repositorio

```bash
  python -m venv env
```

Instalar dependenciaas

```bash
  pip install -r requiriments.txt
```

Correr la aplicación

```bash
  python app.py
```

Luego de abrir la aplicación se puede consultar el manual de usuario para navegar facilmente.

## Módulos del Código

### `data_operations.py`  
Este módulo contiene las funciones necesarias para el manejo y procesamiento de datos:  
- **Carga de datos**: Lectura de archivos en formatos como CSV, JSON, y Excel.  
- **Limpieza de datos**: Tratamiento de valores nulos, duplicados y datos inconsistentes.  
- **Transformaciones**: Normalización, escalado y codificación de datos categóricos.  

### `regression analysis.py`  
Incluye algoritmos para ajuste de modelos de regresión:  
- **Regresión Lineal**: Implementación y entrenamiento para análisis predictivo.  
- **Regresión Polinómica**: Modelado para datos no lineales.  
- **Evaluación de Modelos**: Cálculo de métricas como R², MAE, y RMSE.  

### `graficador.py`  
Proporciona herramientas para visualizar datos y resultados de modelos:  
- **Generación de gráficos**: Histogramas, gráficos de dispersión, y diagramas de caja.  
- **Personalización**: Opciones para títulos, colores y estilos de gráficos.  
- **Exportación**: Guarda gráficos en formatos como PNG y SVG.  

### `generador_dato.py`  
Diseñado para la creación y simulación de datos:  
- **Datos sintéticos**: Generación de conjuntos de datos personalizados para pruebas.  
- **Parámetros personalizables**: Control sobre distribución, tamaño y ruido.  
- **Utilidad en pruebas**: Ideal para validar modelos y algoritmos.  

### `app.py`  
Es el núcleo de la aplicación:  
- **Integración de módulos**: Conexión entre los diferentes componentes de la app.  
- **Interfaz de usuario**: Implementación de una UI interactiva para una experiencia amigable.  
- **Flujo principal**: Coordina la ejecución de procesamiento, modelado y visualización.  



### Contribuciones

  Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

 1. Haz un fork del repositorio.
 2. Crea una rama (git checkout -b nueva-funcionalidad).
 3. Realiza tus cambios y confirma las modificaciones (git commit -am 'Añadir nueva funcionalidad').
 4. Envía un pull request para que revisemos y fusionemos los cambios.
