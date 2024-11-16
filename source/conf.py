# Paquetería importante
import os
import sys

# Instalación del tema principal
import sphinx_book_theme

# Ruta a la carpeta con el código a documentar
sys.path.insert(0, os.path.abspath('../code'))  # Agrega el directorio 'code' al path

# Nombre del proyecto
project = 'Proyecto final'

# Copyright
copyright = '2024, Andrés Gómez, Jorge Garzón, Julián Aros, Laura Oliveros, Laura Triana, Sebastian Manrique'

# Autor del proyecto
author = 'Andrés Gómez, Jorge Garzón, Julián Aros, Laura Oliveros, Laura Triana, Sebastian Manrique'

# Versión del proyecto
release = '1.0'

# Extensiones de la documentación
extensions = [
    'sphinx.ext.autodoc',   # Genera documentación automáticamente desde docstrings
    'sphinx.ext.napoleon',  # Soporte para docstrings estilo Google o NumPy
    'sphinx.ext.viewcode',  # Agrega enlaces al código fuente en la documentación
    'sphinx.ext.githubpages'  # Genera un archivo .nojekyll para GitHub Pages
]

# Ruta para carpeta de plantillas
templates_path = ['_templates']

# Excluir patrones no deseados
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Lenguaje de la documentación
language = 'es'

# Tema de la documentación
html_theme = 'sphinx_book_theme'

# Ruta para carpeta de archivos estáticos
html_static_path = ['assets']

# Configuración del tema
html_theme_options = {
    'repository_url': 'https://github.com/jsmanriquem/proyecto_final',
    'use_repository_button': True,
    'use_issues_button': True,
    'use_download_button': True,
}

# Soluciona posibles errores en docstrings
autodoc_default_options = {
    'members': True,  # Incluye todos los miembros públicos
    'undoc-members': True,  # Incluye miembros no documentados
    'private-members': False,  # Excluye miembros privados
    'show-inheritance': True  # Muestra herencia en clases
}

# Estilo de código fuente
pygments_style = 'sphinx'