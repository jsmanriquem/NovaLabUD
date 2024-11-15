# Minimal makefile for Sphinx documentation with custom post-processing

# Variables
SOURCEDIR     = source
BUILDDIR      = docs

# Define the command to run Sphinx build using Python
SPHINXBUILD   = python -m sphinx -b html

# Target to build the documentation
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

	# 4. Crear el archivo .nojekill en la carpeta docs si no existe
	@echo "Creating .nojekill file..."
	@touch "$(BUILDDIR)/.nojekill"
	@echo ".nojekill file created."

	@echo "Build and modifications completed."

# Optional target to clean up the build directory
clean:
	rm -rf $(BUILDDIR)/*
	@echo "Cleaned build directory."