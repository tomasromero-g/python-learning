def show_inventory(inventory):
    print("=== INVENTARIO ===")
    print(f"- Madera: {inventory.get("wood", 0)}")
    print(f"- Piedra: {inventory.get("stone", 0)}")
    print(f"- Hierro: {inventory.get("iron", 0)}")
    print(f"- Carbón: {inventory.get("coal", 0)}")
    print(f"- Palo: {inventory.get("stick", 0)}")

def can_craft(inventory, item):
    if not item in recipes: # Check if the item exists in the recipes dictionary
        print("El item que querés craftear no existe.")
        return
    for key, quantity in (recipes.get(item)).items(): # Iterate on every item that's needed to craft the main item
        if not (inventory.get(key, 0) >= quantity): # Check if the quantity of that item is equal or greater than needed
            return False # If it's not, then just return False and end the loop
    return True # If it got out of the loop, then it means it's true

def craft(inventory, item):
    if not can_craft(inventory, item): # Check if the item can be crafted
        missing_materials(inventory, item)
        return
    for key_item, quantity_item in (recipes.get(item)).items(): # Iterate on every item that's needed to craft the main item
        for key_inventory in inventory.keys(): # Iterate on every key of the inventory dictionary
            if key_inventory == key_item: # Check if the items are the same
                inventory[key_inventory] -= quantity_item # Substracts one
    crafted_items.append(item)
    print("Agregado a los objetos crafteados.")

def missing_materials(inventory, item):
    for key_item, quantity_item in (recipes.get(item)).items(): # Iterate on every item + quantity that's needed to craft the main item
            for key_inventory, quantity_inventory in inventory.items(): # Iterate on every item + quantity of the inventory
                if key_inventory == key_item: # Check if the items are the same
                    if quantity_inventory < quantity_item: # Check if the item we are on has less quantity than needed to craft the main item
                        difference = quantity_item - quantity_inventory # Get the difference to print it more easily
                        print(f"Te faltan {difference} cantidad de {key_inventory} para poder craftear el item.")

inventory = {"wood": 10, "stone": 5, "iron": 3, "coal": 8, "stick": 1}
recipes = {
    "wooden_pickaxe": {"wood": 3, "stick": 2},
    "stone_pickaxe": {"stone": 3, "stick": 2},
    "iron_pickaxe": {"iron": 3, "stick": 2},
    "torch": {"coal": 1, "stick": 1},
    "crafting_table": {"wood": 4}}
crafted_items = []

print("================================")
print("Mostrando el inventario inicial:")
for key, quantity in inventory.items():
    print(key, quantity)

print("================================")
print("Intentando craftear pico de piedra...")
craft(inventory, "stone_pickaxe")

print("================================")
print("Intentando craftear antorcha...")
craft(inventory, "torch")

print("================================")
print("Intentando craftear pico de hierro...")
craft(inventory, "iron_pickaxe")

print("================================")
print("Inventario luego de craftear:")
for key, quantity in inventory.items():
    print(key, quantity)

print("================================")
print("Lista de objetos crafteados:")
for item in crafted_items:
    print(item)
print("================================")