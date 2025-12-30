import xlrd
import xlwt
from pathlib import Path
from config_paths import RAW_FRANVARO_DIR, OUTPUT_FRANVARO_DIR


def busavsjo_samla_franvarorapporter():
    """
    Slår ihop alla .xls-filer i ``data/raw/franvaro/<läsår>`` till en fil
    (``data/output/<läsår>/franvaro.xls``),
    behåller bara rubriken från första filen och hoppar över de fyra första raderna i resten.
    """
    indata_mapp = RAW_FRANVARO_DIR
    output_fil = OUTPUT_FRANVARO_DIR / "franvaro.xls"

    wb_out = xlwt.Workbook()
    ws_out = wb_out.add_sheet("Data")

    rad_index = 0
    antal_filer = 0

    for filvag in sorted(indata_mapp.iterdir()):
        if filvag.suffix.lower() != ".xls" or filvag.name == "franvaro.xls":
            continue

        skola = Path(filvag).stem

        try:
            wb_in = xlrd.open_workbook(filvag)
            sheet = wb_in.sheet_by_index(0)

            start_row = 0 if antal_filer == 0 else 4  # behåll rubrik bara från första filen

            for row_idx in range(start_row, sheet.nrows):
                row_vals = sheet.row_values(row_idx)

                # Rubrikrad från första filen: lägg till "skola" först
                if antal_filer == 0 and row_idx == 0:
                    ws_out.write(rad_index, 0, "skola")
                    for col_idx, cell in enumerate(row_vals):
                        ws_out.write(rad_index, col_idx + 1, str(cell))
                    rad_index += 1
                    continue

                # Data: skola i kol 0 + resten skiftat
                ws_out.write(rad_index, 0, skola)
                for col_idx, cell in enumerate(row_vals):
                    ws_out.write(rad_index, col_idx + 1, str(cell))
                rad_index += 1

            antal_filer += 1

        except Exception as e:
            print(f"⚠️ Kunde inte läsa {filvag.name}: {e}")

    wb_out.save(str(output_fil))
    print(f"✔️ Skapade '{output_fil}' med {antal_filer} rapporter")


if __name__ == "__main__":
    busavsjo_samla_franvarorapporter()
