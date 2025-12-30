# 🐍 Frånvaroanalys - Sävsjö kommun

Automatiserad bearbetning och analys av elevfrånvaro från flera rapporter.

## 📋 Översikt

Detta projekt samlar, bearbetar och analyserar frånvarodata från flera Excel-rapporter. Systemet skapar kategoriserade översikter per årskurs med fokus på närvaro och ogiltig frånvaro, och lägger nu till skolnamn (från filnamnet) som första kolumn vid sammanslagningen.

## 📁 Projektstruktur

```
franvaro/
├── src/                              # Källkod
│   ├── config_paths.py              # Centraliserad sökvägskonfiguration
│   ├── busavsjo_samla_franvaro.py  # Steg 1: Samla rådata (skola-kolumn läggs till)
│   └── skript works.py              # Steg 2: Analysera och kategorisera (även per skola)
├── data/
│   ├── raw/franvaro/2025-2026/     # Råa .xls-rapporter (lägg filer här)
│   ├── processed/                   # Mellanresultat
│   └── output/2025-2026/           # Färdiga rapporter
├── tests/                           # Testmoduler
├── notebooks/                       # Jupyter-notebooks för analys
└── dokumentation/                   # Teknisk dokumentation
```

## 🚀 Användning

### Förberedelser

1. **Installera beroenden:**
   ```bash
   pip install pandas openpyxl xlrd xlwt
   ```

2. **Lägg rådata i rätt mapp:**
   - Kopiera alla frånvarorapporter (.xls) till `data/raw/franvaro/2025-2026/`

### Arbetsflöde

#### Steg 1: Samla rapporter
Slår ihop alla individuella rapporter till en fil:
```bash
python src/busavsjo_samla_franvaro.py
```
**Output:** `data/output/2024-2025/franvaro.xls`

#### Steg 2: Analysera och kategorisera
Bearbetar data och skapar strukturerad rapport:
```bash
python src/skript works.py
```
**Output:** `data/output/2025-2026/franvaro_rensad_kategoriserad.xlsx`
   - Flikar: Kommun (rensad data), Kommun-översikt, samt en rensad/översikt-flik per skola

## 📊 Vad systemet gör

### Datainsamling
- Läser alla `.xls`-filer från rådata-mappen
- Behåller rubriker endast från första filen
- Sammanfogar till en konsoliderad fil

### Databearbetning
- **Rensning:** Tar bort tomma rader och dubblerade rubriker
- **Strukturering:** Extraherar årskurs från klassnamn
- **Konvertering:** Omvandlar procenttal till numeriska värden

### Kategorisering

**Total frånvaro:**
- 0,0-5,0%
- 5,1-15,0%
- 15,1-30,0%
- 30,1-50,0%
- 50,1--%

**Ogiltig frånvaro:**
- 1,0-5,0%
- 5,1-15,0%
- 15,1--%

### Rapport
Skapar Excel-fil med två flikar:
1. **Rensad data** - All elevdata med färgkodning
2. **Översikt per årskurs** - Summering och fördelning per kategori

## ⚙️ Konfiguration

### Ändra aktivt läsår

Uppdatera i `src/config_paths.py`:
```python
LASAR = "2025-2026"  # Uppdatera för nytt läsår
```

### Skapa nytt läsår (automatiskt)

Använd hjälpskriptet för att skapa mappstruktur för ett nytt läsår:

```bash
python src/skapa_nytt_lasar.py 2025-2026
```

Detta skapar automatiskt:
- `data/raw/franvaro/2025-2026/` - för rådata
- `data/output/2025-2026/` - för rapporter
- `.gitkeep`-filer för versionskontroll

**Sedan:**
1. Uppdatera `LASAR` i `config_paths.py`
2. Lägg rådata i den nya mappen
3. Kör analysprocessen

### Manuell mappstruktur

Om du föredrar att skapa mappar manuellt:
```
data/raw/franvaro/YYYY-YYYY/
data/output/YYYY-YYYY/
```

## 🔧 Tekniska detaljer

- **Python-version:** 3.8+
- **Huvudbibliotek:** pandas, openpyxl, xlrd, xlwt
- **Datakällor:** Excel (.xls och .xlsx)

## 📝 Läsårshantering

Systemet är designat för att hantera data per läsår. Varje läsår får sin egen undermapp i både `raw` och `output`. 

**Mappstrukturen versioneras** (med `.gitkeep`-filer) men **innehållet ignoreras** av Git. Detta betyder:
- ✅ Tomma årsmappar commitas till repo
- ❌ Datafiler (`.xls`, `.xlsx`) versioneras INTE
- ✅ Enkelt att sätta upp projektet på nya maskiner

## 🛠️ Ny funktionalitet

### Blandklasser
- Systemet hanterar nu blandklasser (t.ex. "Rörvik 1-2") genom att kategorisera elever baserat på deras födelseår.
- Konfiguration för blandklasser finns i `config/blandklasser_config.py`.

### Loggning
- Om en klass inte kan kategoriseras, loggas ett varningsmeddelande i terminalen för felsökning.

Exempel på logg:
```
⚠️ Kunde inte bestämma årskurs för klass '1-2' (skola: 'Rörvik').
```
