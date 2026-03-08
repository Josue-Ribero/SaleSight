#################################################################################
# GLOBALES                                                                       #
#################################################################################

PROJECT_NAME = SaleSight
# UV se encarga de la versión de python automáticamente
PYTHON_INTERPRETER = uv run salesight

#################################################################################
# COMANDOS                                                                      #
#################################################################################

## Instalar dependencias y sincronizar proyecto con UV
.PHONY: requirements
requirements:
	uv sync

## Limpiar archivos compilados y cachés
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .venv

## Revisar estilo con ruff a través de UV
.PHONY: lint
lint:
	uv run ruff format --check
	uv run ruff check

## Aplicar formato automático con ruff
.PHONY: format
format:
	uv run ruff check --fix
	uv run ruff format

## Ejecutar tests unitarios con UV
.PHONY: test
test:
	uv run pytest tests

## Crear/Sincronizar entorno virtual con UV
.PHONY: create_environment
create_environment:
	uv sync
	@echo ">>> Proyecto sincronizado con UV. El entorno virtual está en .venv"

#################################################################################
# REGLAS DEL PROYECTO                                                           #
#################################################################################

## Ejecutar Pipeline ETL completo (Extraer, Transformar/EDA, Cargar)
.PHONY: data
data:
	$(PYTHON_INTERPRETER) --modo completo

## Generar Reporte Visual (EDA) desde la base de datos
.PHONY: eda
eda:
	$(PYTHON_INTERPRETER) --modo reporte

#################################################################################
# Ayuda                                                                         #
#################################################################################

.DEFAULT_GOAL := help

help:
	@uv run python -c "import re, sys; lines = '\n'.join([line for line in sys.stdin]); matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); print('Reglas disponibles:\n'); print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))" < $(MAKEFILE_LIST)
