import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# === Sökvägar (rotmapp = 'franvaro') ===
ROOT_DIR = "franvaro"
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Läs in filen som works.py producerar
INPUT_PATH = os.path.join(OUTPUT_DIR, "franvaro_rensad_kategoriserad.xlsx")
df = pd.read_excel(INPUT_PATH, sheet_name="Rensad data")

# Lägg till total frånvaro i procent
df["total_franvaro_pct"] = 100 - df["närvaro_pct"]

# Räkna antal elever med >11% total frånvaro
antal_over_11 = (df["total_franvaro_pct"] > 11).sum()
print(f"Antal elever med >11% total frånvaro: {antal_over_11}")

# Skapa enkel Excel med resultatet
wb = Workbook()
ws = wb.active
ws.title = "Sammanställning"
ws.append(["Mått", "Antal"])
ws.append([">11% total frånvaro", int(antal_over_11)])

# (Valfritt) per årskurs också – bra vid uppföljning
per_ak = (
    df.assign(over11=df["total_franvaro_pct"] > 11)
      .groupby("årskurs")["over11"]
      .sum()
      .reset_index()
      .rename(columns={"over11": "Antal >11%"})
)
ws2 = wb.create_sheet("Per årskurs")
for r in dataframe_to_rows(per_ak, index=False, header=True):
    ws2.append(r)

# Spara
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "franvaro_med_over11.xlsx")
wb.save(OUTPUT_PATH)
print(f"✔️ Klar! Filen sparades till {OUTPUT_PATH}")
