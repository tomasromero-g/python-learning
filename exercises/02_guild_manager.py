def register_adventurer(name, charclass, level):
    allowed_classes = ["iop", "cra", "sacrier", "feca"]
    if not charclass.lower() in allowed_classes:
        print("No se registró al personaje. Tu clase no es valida.")
        return
    return {"Nombre": name, "Clase": charclass.capitalize(), "Nivel": level }

def add_to_guild(guild_list, adventurer):
    if not adventurer:
        print("El aventurero no existe.")
        return
    if adventurer.get("Nivel") > 10:
        guild_list.append(adventurer)
        print("Miembro añadido.")
        return
    print("No se añadió el miembro al gremio. Su nivel era menor a 10.")

def show_guild(guild_list):
    if not guild_list:
        print("No hay miembros en el gremio.")
        return
    for i, adventurer in enumerate(guild_list, start=1):
        print(
            f"[#{i}] Nombre: {adventurer.get('Nombre')}"
             f" | Clase: {adventurer.get('Clase')}"
              f" | Nivel: {adventurer.get('Nivel')}") 

def search_adventurer(guild_list, name):
    for adventurer in guild_list:
        if adventurer.get("Nombre").lower() == name.lower():
            print("Aventurero encontrado.")
            return adventurer
    print("El aventurero no fue encontrado.")

# Implementación con los 4 aventureros
guild = []

# Registrar aventureros
adv1 = register_adventurer("Thor", "iop", 15)  # Datos bien
adv2 = register_adventurer("Loki", "cra", 20)  # Datos bien
adv3 = register_adventurer("Odin", "warrior", 12)  # Datos mal (clase inválida)
adv4 = register_adventurer("Freya", "feca", 8)  # Datos mal (nivel bajo)

# Añadir al gremio (solo si se registraron correctamente)
add_to_guild(guild, adv1)
add_to_guild(guild, adv2)
add_to_guild(guild, adv3)
add_to_guild(guild, adv4)

# Mostrar gremio
print("\nMiembros del gremio:")
show_guild(guild)

# Buscar aventurero
print("\nBuscando a Thor:")
search_adventurer(guild, "Thor")

print("\nBuscando a Odin:")
search_adventurer(guild, "Odin")