"""
Konfiguration för blandklasser (klasser med elever från flera årskurser).

Denna fil definierar vilka klasser som innehåller elever från flera årskurser
och hur eleverna ska kategoriseras baserat på personnummer.
"""

from typing import Dict, List, Tuple

# Blandklasser: klassnamn -> (årskurs_mappning)
# Format: {
#     "klassnamn": {
#         "årskurser": ["Åk 1", "Åk 2"],  # Vilka årskurser som finns i klassen
#         "födelseår_mappning": {
#             "18": "Åk 1",  # Födelseår 2018 -> Åk 1
#             "17": "Åk 2",  # Födelseår 2017 -> Åk 2
#         }
#     }
# }

BLANDKLASSER_CONFIG: Dict[str, Dict] = {
    "rörvik 1-2": {
        "årskurser": ["Åk 1", "Åk 2"],
        "födelseår_mappning": {
            "18": "Åk 1",  # Födda 2018
            "17": "Åk 2",  # Födda 2017
        }
    },
    # Lägg till fler blandklasser här vid behov
    # "Annan skola 2-3": {
    #     "årskurser": ["Åk 2", "Åk 3"],
    #     "födelseår_mappning": {
    #         "17": "Åk 2",
    #         "16": "Åk 3",
    #     }
    # },
}


def är_blandklass(klassnamn: str) -> bool:
    """
    Kontrollera om en klass är en blandklass.
    
    Args:
        klassnamn: Namnet på klassen att kontrollera
        
    Returns:
        True om klassen är definierad som blandklass, annars False
    """
    if not isinstance(klassnamn, str):
        return False
    
    # Trimma och normalisera klassnamnet
    klassnamn = klassnamn.strip()
    
    # Exakt matchning
    if klassnamn in BLANDKLASSER_CONFIG:
        return True
    
    # Kontrollera även om klassnamnet innehåller någon av de konfigurerade namnen
    for config_klass in BLANDKLASSER_CONFIG.keys():
        if config_klass.lower() in klassnamn.lower():
            return True
    
    return False


def få_årskurs_för_blandklass(klassnamn: str, personnummer: str) -> str:
    """
    Bestäm årskurs för en elev i en blandklass baserat på personnummer.
    
    Args:
        klassnamn: Namnet på blandklassen
        personnummer: Elevens personnummer (förväntas vara minst 2 tecken långt)
        
    Returns:
        Årskurs (t.ex. "Åk 1", "Åk 2") eller None om årskurs inte kan bestämmas
    """
    if not isinstance(klassnamn, str) or not isinstance(personnummer, str):
        return None
    
    klassnamn = klassnamn.strip()
    personnummer = str(personnummer).strip()
    
    # Hitta matchande konfiguration
    config = None
    if klassnamn in BLANDKLASSER_CONFIG:
        config = BLANDKLASSER_CONFIG[klassnamn]
    else:
        # Försök hitta genom partiell matchning
        for config_klass, conf in BLANDKLASSER_CONFIG.items():
            if config_klass.lower() in klassnamn.lower():
                config = conf
                break
    
    if not config:
        return None
    
    # Extrahera födelseår (första två siffrorna i personnumret)
    if len(personnummer) < 2:
        return None
    
    födelseår_kort = personnummer[:2]
    
    # Slå upp i mappningen
    födelseår_mappning = config.get("födelseår_mappning", {})
    årskurs = födelseår_mappning.get(födelseår_kort)
    
    return årskurs


def få_alla_blandklasser() -> List[str]:
    """
    Returnera en lista med alla konfigurerade blandklasser.
    
    Returns:
        Lista med klassnamn för alla blandklasser
    """
    return list(BLANDKLASSER_CONFIG.keys())


def få_blandklass_info(klassnamn: str) -> Dict:
    """
    Hämta fullständig konfiguration för en blandklass.
    
    Args:
        klassnamn: Namnet på blandklassen
        
    Returns:
        Dictionary med konfiguration eller None om klassen inte finns
    """
    if klassnamn in BLANDKLASSER_CONFIG:
        return BLANDKLASSER_CONFIG[klassnamn]
    
    # Försök partiell matchning
    for config_klass, conf in BLANDKLASSER_CONFIG.items():
        if config_klass.lower() in klassnamn.lower():
            return conf
    
    return None
