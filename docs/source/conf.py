# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

import sphinx_book_theme

# Configurar el tema
html_theme = 'sphinx_book_theme'

# Opciones del tema (puedes personalizarlo según tus necesidades)
# html_theme_options = {
#     # "repository_url": "https://github.com/tu-repositorio",  # Enlace a tu repositorio
#     "use_repository_button": True,
#     "use_edit_page_button": True,  # Mostrar botón para editar en GitHub
#     "use_issues_button": True,     # Mostrar botón para reportar problemas
# }

sys.path.insert(0, os.path.abspath('../../code'))

project = 'toma_datos'
copyright = '2024, Julián Aros, Sebastian Manrique'
author = 'Julián Aros, Sebastian Manrique'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_static_path = ['_static']
