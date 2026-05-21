import sys
from pathlib import Path

# O Streamlit Cloud executa a partir da raiz do repositório.
# Este app isolado fica em subpasta para usar requirements.txt próprio e mínimo.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importa e executa o app independente criado na raiz.
# O arquivo importado não depende do dashboard de trading nem das bibliotecas pesadas.
import figurinhas_copa_2026_app  # noqa: F401
