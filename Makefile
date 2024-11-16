# Variables
SOURCEDIR     = source
BUILDDIR      = docs

# Definición del comando que construye la documentación
SPHINXBUILD   = python -m sphinx -b html

# Comando para generar la documentación y exportarla a GitHub Pages
build:
	# 1. Ejecutar el comando Sphinx para generar la documentación
	@$(SPHINXBUILD) $(SOURCEDIR) $(BUILDDIR)
	@echo "Sphinx documentation built."

	# 2. Renombrar la carpeta _static a assets dentro de docs
	@if [ -d "$(BUILDDIR)/_static" ]; then \
		mv "$(BUILDDIR)/_static" "$(BUILDDIR)/assets"; \
		echo "Renamed '_static' to 'assets'"; \
	else \
		echo "No '_static' folder found to rename"; \
	fi

	# 3. Reemplazar '_static' por 'assets' en todos los archivos .html generados dentro de docs
	@echo "Updating references in HTML files..."
	@find $(BUILDDIR) -type f -name "*.html" -exec sed -i 's/_static/assets/g' {} \;
	@echo "Replaced '_static' with 'assets' in HTML files."

	@echo "Build and modifications completed."

# Comando para eliminar la documentación generada y volver a crear una nueva
clean:
	rm -rf $(BUILDDIR)
	@echo "Cleaned build directory."