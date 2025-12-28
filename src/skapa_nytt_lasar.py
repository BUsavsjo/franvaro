"""
Skript för att skapa mappstruktur för ett nytt läsår
Användning: python skapa_nytt_lasar.py 2025-2026
"""
import sys
from pathlib import Path

# Projektets rotmapp
ROOT_DIR = Path(__file__).parent.parent


def skapa_lasar_struktur(lasar: str):
    """
    Skapar mappar och .gitkeep-filer för ett nytt läsår
    
    Args:
        lasar: Läsår i format "YYYY-YYYY" (t.ex. "2025-2026")
    """
    # Validera format
    if not lasar or len(lasar) != 9 or lasar[4] != '-':
        print("❌ Felaktigt format! Använd format YYYY-YYYY (t.ex. 2025-2026)")
        return False
    
    try:
        start_ar = int(lasar[:4])
        slut_ar = int(lasar[5:])
        if slut_ar != start_ar + 1:
            print("❌ Slutåret måste vara startår + 1")
            return False
    except ValueError:
        print("❌ Ogiltiga årtal")
        return False
    
    # Skapa mappar
    data_dir = ROOT_DIR / "data"
    raw_franvaro = data_dir / "raw" / "franvaro" / lasar
    output_lasar = data_dir / "output" / lasar
    
    # Skapa mapparna
    raw_franvaro.mkdir(parents=True, exist_ok=True)
    output_lasar.mkdir(parents=True, exist_ok=True)
    
    # Skapa .gitkeep-filer med beskrivningar
    (raw_franvaro / ".gitkeep").write_text(
        f"# Lägg råa .xls frånvarorapporter här för läsåret {lasar}\n",
        encoding="utf-8"
    )
    (output_lasar / ".gitkeep").write_text(
        f"# Processerade rapporter för läsåret {lasar} sparas här\n",
        encoding="utf-8"
    )
    
    print(f"✅ Skapade mappstruktur för läsår {lasar}:")
    print(f"   📁 {raw_franvaro}")
    print(f"   📁 {output_lasar}")
    print(f"\n💡 Nästa steg:")
    print(f"   1. Uppdatera LASAR = '{lasar}' i src/config_paths.py")
    print(f"   2. Lägg rådata i data/raw/franvaro/{lasar}/")
    print(f"   3. Kör src/busavsjo_samla_franvaro.py")
    
    return True


def main():
    if len(sys.argv) != 2:
        print("Användning: python skapa_nytt_lasar.py 2025-2026")
        print("\nExempel:")
        print("  python skapa_nytt_lasar.py 2025-2026")
        print("  python skapa_nytt_lasar.py 2026-2027")
        sys.exit(1)
    
    lasar = sys.argv[1]
    if skapa_lasar_struktur(lasar):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
