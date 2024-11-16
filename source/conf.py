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
    'sphinx.ext.autodoc',          # Para documentar automáticamente el código
    'sphinx.ext.napoleon',         # Soporte para docstrings de estilo Google/Numpy
    'sphinx_copybutton',           # Agrega un botón para copiar bloques de código
    'sphinx.ext.githubpages',      # Soporte para GitHub Pages
]

# Ruta para carpeta de plantillas
templates_path = ['_templates']

# Excluir patrones no deseados de la documentación
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Lenguaje de la documentación
language = 'es'

# Tema de la documentación
html_theme = 'sphinx_book_theme'  # Usamos el tema 'sphinx_book_theme'

# Ruta para carpeta de archivos estáticos
html_static_path = ['assets']

# Configuración adicional para el tema 'sphinx_book_theme'
html_theme_options = {
    'repository_url': 'https://github.com/usuario/repositorio',
    'use_repository_button': True,
    'home_page_in_toc': True,
    'use_download_button': False,
}

# Configuración para mostrar código fuente automáticamente
autodoc_typehints = 'description'
autodoc_class_signature = 'separated'
autodoc_preserve_defaults = True

def setup(app):
    app.add_css_file('custom.css')
    app.connect('autodoc-process-docstring', add_source_code)

def add_source_code(app, what, name, obj, options, lines):
    import inspect
    # Solo mostrar código para funciones (no para clases)
    if inspect.isfunction(obj):
        try:
            source = inspect.getsource(obj)
            lines.extend(['', '.. code-block:: python', ''])
            lines.extend(['    ' + line for line in source.splitlines()])
        except Exception:
            pass

# Configuración para manejar la documentación automática
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'private-members': False,
    'show-inheritance': True,
    'member-order': 'bysource',  # Mantiene el orden del código fuente
}

# Estilo de código fuente
pygments_style = 'sphinx'

# Configuración para el logo y favicon
html_logo = 'assets/logo_provisional1.svg'
html_favicon = 'assets/logo_provisional1.ico'

# Configuración del archivo .nojekyll para GitHub Pages
html_extra_path = ['.nojekyll']