# Proyecto de Software en Python

## Descripción del Proyecto

Este proyecto ha sido desarrollado en Python utilizando el paradigma de **Programación Orientada a Objetos (POO)**, lo que facilita la gestión, reutilización y mantenimiento del código. El objetivo del proyecto es realizar simulaciones de experimentos físicos, como la caída libre, con la capacidad de generar gráficos e informes detallados sobre el comportamiento de los objetos bajo diversas condiciones.

A lo largo de este proyecto, se utilizan librerías de Python como **pandas**, **numpy** y **matplotlib** para el manejo de datos y la visualización gráfica, y **scipy** para la interpolación y otros análisis matemáticos. El código está diseñado para ser fácilmente extensible y configurable, permitiendo a los usuarios modificar parámetros de los experimentos.

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

Para instalar y ejecutar el proyecto, sigue estos pasos:

1. Clona el repositorio
2. Crea un entorno virtual (opcional, pero recomendado)
3. Instala las dependencias necesarias
4. Ejecuta el programa principal

# Detalles del Código

## `simulation.py`

Contiene la clase `CaidaLibre`, que simula el comportamiento de un objeto en caída libre. La clase se encarga de calcular el tiempo, la distancia recorrida y la velocidad del objeto en función del tiempo.

### Ejemplo de código dentro de `simulation.py`:

```python
import numpy as np

class CaidaLibre:
    def __init__(self, altura_inicial, gravedad, tiempo_total):
        self.altura_inicial = altura_inicial
        self.gravedad = gravedad
        self.tiempo_total = tiempo_total

    def realizar_simulacion(self):
        tiempo = np.linspace(0, self.tiempo_total, num=100)
        distancia = self.altura_inicial - (0.5 * self.gravedad * tiempo**2)
        velocidad = -self.gravedad * tiempo
        return {"tiempo": tiempo, "distancia": distancia, "velocidad": velocidad}

### Contribuciones

  Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

 1. Haz un fork del repositorio.
 2. Crea una rama (git checkout -b nueva-funcionalidad).
 3. Realiza tus cambios y confirma las modificaciones (git commit -am 'Añadir nueva funcionalidad').
 4. Envía un pull request para que revisemos y fusionemos los cambios.
