name = input("Ingrese el nombre de su personaje: ")
while not name.isalpha():
    print("Ingresó un nombre incorrecto. Intentelo de nuevo.")
    name = input("Ingrese el nombre de su personaje: ")

lvl = int(input("Ingrese el nivel de su personaje: "))

charclass = input("Ingrese el nombre de su clase: ")
while not charclass.isalpha():
    print("Ingresó un nombre incorrecto. Intentelo de nuevo.")
    charclass = input("Ingrese el nombre de su clase: ")

player = {"name": name, "lvl": lvl, "class": charclass, "title": None}
allowed_classes = ["iop", "feca", "xelor", "sadida"]
access = True
reason = None

if player["name"].lower() == "rushu":
    access = False
    reason = "No podés acceder. Te llamas Rushu."
elif player["lvl"] < 60:
    access = False
    reason = "No podés acceder. Tu nivel es menor a 60. ¡Seguí jugando!"
elif not (player["class"].lower() in allowed_classes):
    access = False
    reason = "No podés acceder. Tu clase no está permitida."

if access:
    access = "✅ Acceso concedido"
    if player["lvl"] > 100:
        player["title"] = "Veterano"
else:
    access = "❌ Acceso denegado"

print("")
print("=== CONTROL DE ACCESO - OTO MUSTAM ===")
print(f"Personaje: {player['name']}")
print(f"Clase    : {player['class']}")
print(f"Nivel    : {player['lvl']}")
if player["title"] is not None:
    print(f"Título   : {player['title']}")
print(f"Resultado: {access}")
if reason:
    print(f"Razón    : {reason}")
print("======================================")