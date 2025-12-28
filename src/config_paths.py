"""
Konfigurationsfil för sökvägar i frånvaro-projektet
"""
from pathlib import Path

# Projektets rotmapp
ROOT_DIR = Path(__file__).parent.parent

# Läsår (kan ändras varje år)
LASAR = "2025-2026"

# Datamappar
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"

# Frånvarospecifika mappar
RAW_FRANVARO_DIR = RAW_DATA_DIR / "franvaro" / LASAR
OUTPUT_FRANVARO_DIR = OUTPUT_DIR / LASAR

# Skapa mappar om de inte finns
for directory in [RAW_FRANVARO_DIR, OUTPUT_FRANVARO_DIR, PROCESSED_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
