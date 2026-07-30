import random
import math


def load_data():
    for player in players:
        blocks = random.randint(200, 1500)
        mobs = random.randint(10, 200)
        deaths = random.randint(0, 30)
        score = math.floor((blocks * 0.5) + (mobs * 3) - (deaths * 5))
        current = {
            "name": player,
            "mined_blocks": blocks,
            "slained_mobs": mobs,
            "deaths": deaths,
            "score": score,
        }
        players_database[player] = current
    print("Datos de la semana generados.")


def set_rank():
    if not players_database:
        print("Aún no se cargaron los datos de la semana.")
        return
    for player in players_database:
        if (players_database[player])["score"] >= 800:
            (players_database[player])["rank"] = "Leyenda"
        elif 500 <= (players_database[player])["score"] <= 799:
            (players_database[player])["rank"] = "Veterano"
        elif 200 <= (players_database[player])["score"] <= 499:
            (players_database[player])["rank"] = "Soldado"
        else:
            (players_database[player])["rank"] = "Recluta"
    print("Rangos cargados.")


def report():
    database = sorted_database(players_database)
    mvp = database[0]
    risk = max(database, key=lambda p: p['deaths'])
    miner = max(database, key=lambda p: p['mined_blocks'])
    print("╔══════════════════════════════════════╗")
    print("     TABLERO GUILD - SEMANA ACTUAL     ")
    print("╚══════════════════════════════════════╝")
    print()
    for index, player in enumerate(database, start=1):
        print(
            (
                f"#{index:<2} "
                f"{player['rank']:14} | "
                f"{player['name']:13} | "
                f"{player['score']:10} | "
                f"{player['deaths']:^14}"
            )
        )
    print("──────────────────────────────────────")
    print(f"🏅 MVP de la semana: {mvp['name']} ({mvp['score']} pts)")
    print(f"💀 Mayor riesgo de vida: {risk['name']} ({risk['deaths']} muertes)")
    print(f"⛏️ Minero élite: {miner['name']} ({miner['mined_blocks']} bloques)")
    print("──────────────────────────────────────")


def sorted_database(database):
    players = []
    for player in database.values():
        players.append(player)
    return sorted(players, key=lambda p: (p["score"], -p["deaths"]), reverse=True)


players = ["Steve", "Alex", "Notch", "Herobrine", "Creeper_Jr", "Enderman"]
players_database = {}
load_data()
set_rank()
report()
