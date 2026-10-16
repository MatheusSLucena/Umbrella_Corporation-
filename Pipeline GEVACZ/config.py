"""Configurações da ETL GEVACZ."""
import os
from pathlib import Path
from dotenv import dotenv_values

# Ajuste para a pasta onde estão os arquivos de ovitrampas e o .env.
BASE = Path(os.getenv("GEVACZ_BASE", r"C:\Users\joaoc\Downloads\PROJETO5"))
ENV_PATH = BASE / ".env"
_ENV = dotenv_values(ENV_PATH)

PATH_2026 = BASE / "INFORMAÇÕES - GEVACZ" / "OVITRAMPAS 2026" / (
    "PLANILHA GERAL OVT 2026 ATÃ_ O CICLO  - ESSA É A NOVA PLNILHA DE DIGITAÇÃO DAS OVITRAMPAS.xlsx"
)
PATH_ANTIGOS = {
    2025: str(BASE / "INFORMAÇÕES - GEVACZ" / "OVITRAMPAS 2025" / "Planilha OVT DS-{ds}.xls"),
    2024: str(BASE / "INFORMAÇÕES - GEVACZ" / "OVITRAMPAS 2024" / "Planilha OVT DS-{ds}.xls"),
}
DSS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

def cfg(chave, padrao=None, obrigatorio=False):
    """Obtém uma configuração do .env ou das variáveis de ambiente."""
    valor = _ENV.get(chave) or os.environ.get(chave) or padrao
    if obrigatorio and not valor:
        raise KeyError(f"Variável {chave} não encontrada em {ENV_PATH}")
    return valor.strip() if isinstance(valor, str) else valor
