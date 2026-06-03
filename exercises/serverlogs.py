import datetime
import random
import os
import time


def login():
    while True:
        name = input("¡Bienvenido al server! Ingrese su nombre (salga con 'salir'): ")
        if name.lower() == "salir":
            break
        add_player(name)


def add_player(name):
    connection_date = datetime.date.today()
    connection_time = datetime.datetime.now()
    login_id = random.randint(0, 999999)
    player = {
        "name": name,
        "connection_date": connection_date,
        "connection_time": connection_time,
        "login_id": login_id,
    }
    players_database[name] = player
    print("Jugador conectado.")


def set_actions():
    while True:
        if not players_database:
            print("No hay jugadores conectados.")
            break
        name = input(
            "Ingrese el nombre de su personaje para realizar acciones (salga con 'salir'): "
        )
        if name.lower() == "salir":
            break
        while not (name in players_database):
            name = input("Ese jugador no existe. Intentelo de nuevo: ")
        if (players_database.get(name)).get(
            "actions"
        ):  # Verify if actions exists, if it does, then continues to the other character
            print("Tu personaje realizó la cantidad permitida de acciones.")
            continue
        actions_in_session = []
        actions_amount = random.randrange(3, 7)  # Ammount of actions to realise
        for action in range(actions_amount):
            action_timestamp = (
                random.choice(actions),
                datetime.datetime.now().strftime("%H:%M:%S"),
            )  # Creates a tuple with the action + timestamp
            actions_in_session.append(action_timestamp)  # Appends it to a list
            time.sleep(3)
        (players_database.get(name))[
            "actions"
        ] = actions_in_session  # Add the whole list full of tuples right to the dictionary
        print("Acciones cargadas.")


def logoff():
    posibles = ["si", "no"]
    while True:
        if not players_database:
            print("No hay jugadores conectados.")
            break
        opt = input("¿Quieres salir del juego? (si/no): ")
        while not (opt.lower() in posibles):
            opt = input("Ingresate una opción incorrecta. Ingresa 'si' o 'no': ")
        if opt.lower() == "si":
            name = input("Ingrese el nombre de su personaje (salga con 'salir'): ")
            if name.lower() == "salir":
                break
            while not (name in players_database):
                name = input("Ese jugador no existe. Intentelo de nuevo: ")
            create_log(name)
            players_database.pop(name)
            print(f"Jugador {name} desconectado.")
        else:
            break


def report(name):
    lineas = [
        "=========== REPORTE DE SESIÓN ========",
        f"Nombre del jugador: {players_database.get(name).get('name')}",
        f"ID de sesión: {players_database.get(name).get('login_id')}",
        f"Hora de entrada: {players_database.get(name).get('connection_time').strftime('%H:%M:%S')}",
        f"Hora de salida: {datetime.datetime.now().strftime('%H:%M:%S')}",
        f"Duración de la sesión: {session_time(name)}",
        "Actividades realizadas...",
        "------------------------------",
        ennumerate_actions(name),
        "------------------------------",
        f"Score de productividad: {productivity_score(name):.2f}%",
    ]
    return "\n".join(lineas)


def session_time(name):
    login_time = (players_database.get(name)).get("connection_time")
    logoff_time = datetime.datetime.now()
    total_time = divmod((logoff_time - login_time).seconds, 60)
    return f"{total_time[0]} minutos y {total_time[1]} segundos."


def ennumerate_actions(name):
    lineas = []
    for index, action in enumerate(
        (players_database.get(name)).get("actions"), start=1
    ):
        lineas.append(f"Acción número {index}: {action}")
    return "\n".join(lineas)


def productivity_score(name):
    productive = 0
    total_actions = 0
    not_productive = ["murió por creeper", "entró al Nether"]
    for action in (players_database.get(name)).get("actions"):
        if not (action[0] in not_productive):
            productive += 1
        total_actions += 1
    return round((productive / total_actions) * 100, 2)


def create_log(name):
    path = "server_logs"
    if not os.path.exists(path):
        os.mkdir(path)
    file = f"sesion_{name}_{(players_database.get(name)).get('login_id')}.txt"
    full_path = os.path.join(path, file)
    with open(full_path, "a", encoding="utf-8") as f:
        f.write(report(name))
        f.write("\n")


players_database = {}
actions = [
    "minó bloques",
    "construyó estructura",
    "murió por creeper",
    "crafteo item",
    "entró al Nether",
    "comerció con aldeano",
    "encontró diamantes",
]

login()
set_actions()
logoff()
