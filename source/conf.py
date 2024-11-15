# Paquetería importante
import os
import sys

# Instalación del tema principal
import sphinx_book_theme

# Ruta a la carpeta con el código a documentar
sys.path.insert(0, os.path.abspath('../code'))

# Nombre del proyecto
project = 'Proyecto final'
# Copyright
copyright = '2024, Andrés Gómez, Jorge Garzón, Julián Aros, Laura Oliveros, Laura Triana, Sebastian Manrique'
# Autor del proyecto
author = 'Andrés Gómez, Jorge Garzón, Julián Aros, Laura Oliveros, Laura Triana, Sebastian Manrique'
# Versión del proyecto
release = '1.0'

# Extensiones de la documentación
extensions = ['sphinx.ext.autodoc','sphinx.ext.napoleon']

# Ruta para carpeta de plantillas
templates_path = ['_templates']
exclude_patterns = []

# Lenguaje de la documentación
language = 'es'

# Tema de la documentación
html_theme = 'sphinx_book_theme'
# Ruta para carpeta de archivos estáticos
html_static_path = ['assets']