import random
import math


def check():
    if not characters_database:
        print("Aún no se cargó ningún personaje.")
        return True
    return False


def create_character(name, character_class, *stats):
    character = {}
    stats_list = ["hp", "mana", "fuerza", "defensa", "velocidad"]
    stats_given = len(stats)
    stats_left = 5 - stats_given
    c = 0
    if stats_given > 5: # Check if there are more than 5 stats
        print(f"Ingresó {stats_given} stats. El máximo permitido es 5.")
        return
    
    character["name"] = name
    if not ((str(character_class.replace(" ", ""))).isalpha()):
        print("Por favor, ingrese una clase válida y vuelva a intentarlo.")
        return
    character["character_class"] = character_class
    
    if stats_given: # Firstly, check if there is any stat entered
        for i, stat in enumerate(stats): # If there is, then iterate on every stat given by the user
            if not (str(stat).isdigit()): # Check if the argument is a number
                print("Sólo se pueden ingresar números como estadística.")
                return
            character[stats_list[i - c]] = stat 
                # player[stats[index - c]] let us set every stat on order without having to repeat,
                # and substracting c allow us to prevent trying to access an unwanted stat, since we delete the element
            stats_list.pop(i - c) # Delete the element we just accessed, to not use it again by error
            c += 1 # Add 1 so we know how much to substract
        c = 0
        for i in range(stats_left): # Another for to add the stats that weren't added by the user, if there are any
            character[stats_list[i - c]] = random.randint(10, 50)
            stats_list.pop(i - c)
            c += 1
        characters_database[name] = character
        print("Personaje agregado.")
        return
    
    for i in range(5): # If there aren't stats entered
        character[stats_list[i - c]] = random.randint(10, 50)
        stats_list.pop(i - c)
        c += 1
    characters_database[name] = character
    print("Personaje agregado.")
    return


def equip(**equipments):
    if check():
        return
    equipment = {}
    for slot, item in equipments.items():
         equipment[slot] = item
    return equipment


def calculate_power(character, **bonuses):
    if check():
        return
    for stat, amount in bonuses.items():
        character[stat] += amount 
    basepower = (character["hp"] * 0.3 +
                character["mana"] * 0.2 +
                character["fuerza"] * 0.5 + 
                character["defensa"] * 0.4 + 
                character["velocidad"] * 0.3)
    return math.floor(basepower)


def set_tier(character):
    if check():
        return
    if character["power"] >= 120:
        return "S-Tier"
    elif 90 <= character["power"] <= 119:
        return "A-Tier"
    elif 60 <= character["power"] <= 89:
        return "B-Tier"
    else:
        return "F-Tier"


def report():
    if check():
        return
    characters = sorted(list(characters_database.values()), key=lambda p: p["power"], reverse=True)
    strongest = max(characters, key=lambda c: c["fuerza"])
    slowest = min(characters, key=lambda c: c["velocidad"])
    print("╔══════════════════════════════════════╗")
    print("  RANKING DE PERSONAJES -- ROBLOX RPG)  ")
    print("╚══════════════════════════════════════╝")
    print("")
    for index, character in enumerate(characters, start=1):
        print(
            f"#{index} {character["tier"]:<10} | {character["name"]:<15} | "
            f"Clase: {character["character_class"]:<15} | Poder: {character["power"]}"
        )
    print("──────────────────────────────────────")
    print(f"💪 Más fuerte: {strongest["name"]} (fuerza: {strongest["fuerza"]})")
    print(f"🐢 Más lento: {slowest["name"]} (velocidad: {slowest["velocidad"]})")
    print("──────────────────────────────────────")


characters_database = {}

create_character("tomi", "dragón", 50, 39, 20, 1)
create_character("male", "leviatan", 20)
create_character("martin", "stormcaller")
create_character("luna", "hada", 45, 60, 25, 35)

characters_database["tomi"]["equipment"] = equip(casco="Casco de Cuero",
                                    pechera="Malla de Hierro",
                                    arma="Espada Corta",
                                    botas="Botas de Tela",
                                    escudo="Escudo de Madera")
characters_database["male"]["equipment"] = equip(capucha="Capucha de Mago",
                                    tunica="Túnica de Seda",
                                    arma="Báculo de Cristal",
                                    anillo="Sortija de Oro")
characters_database["martin"]["equipment"] = equip(arma="Daga de Cobre",
                                      amuleto="Diente de Lobo")
characters_database["luna"]["equipment"] = equip(corona="Corona de Plata",
                                      vestido="Vestido de Gasa",
                                      arma="Varita de Luz",
                                      anillo="Anillo de Poder")

characters_database["tomi"]["power"] = calculate_power(characters_database["tomi"],
                                                       hp=50, 
                                                       mana=20, 
                                                       fuerza=15, 
                                                       defensa=10, 
                                                       velocidad=5)
characters_database["male"]["power"] = calculate_power(characters_database["male"], 
                                                       mana=100, 
                                                       velocidad=20, 
                                                       fuerza=5)
characters_database["martin"]["power"] = calculate_power(characters_database["martin"],
                                                         defensa=200)
characters_database["luna"]["power"] = calculate_power(characters_database["luna"],
                                                       mana=80, 
                                                       fuerza=10, 
                                                       velocidad=40)

characters_database["tomi"]["tier"] = set_tier(characters_database["tomi"])
characters_database["male"]["tier"] = set_tier(characters_database["male"])
characters_database["martin"]["tier"] = set_tier(characters_database["martin"])
characters_database["luna"]["tier"] = set_tier(characters_database["luna"])

report()