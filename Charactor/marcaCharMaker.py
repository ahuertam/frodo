import random

class MarcaNameGenerator:
    """
    Generador de nombres para Aventuras en la Marca del Este.
    Intenta respetar la sonoridad del mundo de Valion y sus diferentes razas.
    """

    def __init__(self):
        self.syllables = {
            "human": {
                "prefixes": ["Val", "Ro", "Ci", "Mar", "Tor", "Bel", "Ar", "Dan", "Gor", "San", "Per", "Jor"],
                "suffixes": ["ion", "eda", "nea", "ca", "or", "an", "on", "us", "ez", "do", "ge", "te"],
                "mid": ["li", "re", "mi", "na", "te", "la", "so", "da"]
            },
            "elf": {
                "prefixes": ["Fe", "Te", "Sil", "Gal", "Aer", "Thal", "Elen", "Cae", "Fin", "Iau"],
                "suffixes": ["riel", "slin", "gol", "ion", "or", "th", "dil", "wyn", "ae", "on"],
                "mid": ["me", "ne", "den", "la", "ra", "th", "s"]
            },
            "dwarf": {
                "prefixes": ["Stein", "Thor", "Gro", "Bal", "Dur", "Kim", "Bom", "Dwal", "Thra", "Kaz"],
                "suffixes": ["kel", "in", "or", "gar", "ur", "bar", "grim", "oak", "ir", "drin"],
                "mid": ["g", "k", "d", "b", "z"]
            },
            "halfling": {
                "prefixes": ["Bil", "Fro", "Mer", "Pip", "Sam", "Tol", "Ber", "Fol", "Milo"],
                "suffixes": ["bo", "do", "ry", "in", "wise", "man", "co", "grin", "bur"],
                "mid": ["ba", "lo", "da", "ni"]
            },
            "gnome": {
                "prefixes": ["Sal", "Fem", "Gla", "Fol", "Tim", "Ben", "Wil", "Nim"],
                "suffixes": ["morin", "eriel", "forin", "salin", "ble", "wick", "to", "gnus"],
                "mid": ["mo", "fe", "li", "sa"]
            },
            "orc": {
                "prefixes": ["Un", "Groz", "Krug", "Zog", "Mog", "Thrak", "Nar", "Gul"],
                "suffixes": ["goloz", "tar", "mash", "gash", "dush", "ak", "uk", "or"],
                "mid": ["ga", "zu", "ra", "k"]
            },
             "drow": {
                "prefixes": ["Xor", "Ziy", "Vico", "Ril", "Phae", "Driz", "Zak"],
                "suffixes": ["andor", "arid", "na", "vir", "zzt", "fein", "ra", "m"],
                "mid": ["an", "ar", "or", "x"]
            }
        }
        
        # Nombres completos de ejemplo o específicos del lore para mezclar
        self.lore_names = {
            "human": ["Robleda", "Valion", "Cirinea", "Pedro", "Cristóbal", "Salvador"],
            "dwarf": ["Steinkel"],
            "gnome": ["Salmorin", "Sildengol", "Temeslin", "Femeriel"],
            "drow": ["Xorandor", "Ziyarid"],
            "enemy": ["Ungoloz", "Augelmir"]
        }

    def generate(self, race="human", gender="any"):
        """
        Genera un nombre basado en la raza.
        """
        race = race.lower()
        if race not in self.syllables:
            # Fallback to human or generic fantasy logic
            race = "human"
            
        parts = self.syllables[race]
        
        # Simple construction: Prefix + (Optional Mid) + Suffix
        # Weighted choice to sometimes include a middle syllable
        structure = random.choices(["PS", "PMS", "P"], weights=[50, 40, 10], k=1)[0]
        
        name = ""
        prefix = random.choice(parts["prefixes"])
        suffix = random.choice(parts["suffixes"])
        
        if structure == "PS":
            name = prefix + suffix
        elif structure == "PMS":
            mid = random.choice(parts["mid"])
            name = prefix + mid + suffix
        else:
             # Just a prefix-like name or from lore list sometimes?
             # Let's stick to constructed for uniqueness, maybe add another syllable
             name = prefix + random.choice(parts["suffixes"]) # Fallback to PS for now to ensure length
             
        # Capitalize
        name = name.capitalize()
        
        return name

    def generate_full_name(self, race="human"):
        firstname = self.generate(race)
        
        # Apellidos o títulos simples
        lastname = ""
        if race == "human":
             lastname = random.choice(["de Robleda", "el Bravo", "Sánchez", "Gil", "García", "del Este", "Valiente"])
        elif race == "dwarf":
             lastname = random.choice(["Barbadura", "Martillo", "Escudoferreo", "Rocadura", "de la Montaña"])
        elif race == "elf":
             lastname = random.choice(["Hojaverde", "Estrellada", "Luzdebosque", "Caminante", "Silvano"])
        elif race == "halfling":
             lastname = random.choice(["Piesligeros", "Colina", "Sotomonte", "Bolsón", "Gamyi"])
             
        if lastname:
            return f"{firstname} {lastname}"
        return firstname

if __name__ == "__main__":
    generator = MarcaNameGenerator()
    print("--- Generador de Nombres de la Marca del Este ---")
    print(f"Humano: {generator.generate_full_name('human')}")
    print(f"Elfo: {generator.generate_full_name('elf')}")
    print(f"Enano: {generator.generate_full_name('dwarf')}")
    print(f"Halfling: {generator.generate_full_name('halfling')}")
    print(f"Gnomo: {generator.generate_full_name('gnome')}")
    print(f"Elfo Oscuro: {generator.generate_full_name('drow')}")
    print(f"Semiorco: {generator.generate_full_name('orc')}")
