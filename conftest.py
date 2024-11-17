import sys
from pathlib import Path

# Path maneja automáticamente los separadores según el SO
PROJECT_ROOT = Path(__file__).resolve().parent
CODE_PATH = PROJECT_ROOT / 'code'

# Verificación y agregado al path
if not CODE_PATH.exists():
    raise ImportError(f"No se encuentra el directorio de código en: {CODE_PATH}")

sys.path.append(str(CODE_PATH))