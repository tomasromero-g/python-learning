def build_register(**kwargs) -> dict:
    allowed_keys = ["solo_activos", "nivel_minimo", "clase"]
    for key in kwargs.keys():  # Restrinction: keys not in allowed_keys
        if key not in allowed_keys:
            raise ValueError(f"El kwarg {key} no está permitido.")
    filtered_list = filter_list(**kwargs)
    return create_dict(filtered_list)


def filter_list(**kwargs) -> list:
    filtered_list = members
    if "solo_activos" in kwargs:  # Check if "solo_activos"
        if kwargs["solo_activos"]:
            filtered_list = [
                member for member in filtered_list if member["activo"] == True
            ]
    if "nivel_minimo" in kwargs:  # Check if "nivel_minimo"
        filtered_list = [
            member
            for member in filtered_list
            if member["nivel"] >= kwargs["nivel_minimo"]
        ]
    if "clase" in kwargs:  # Check if "clase"
        filtered_list = [
            member for member in filtered_list if member["clase"] == kwargs["clase"]
        ]
    return filtered_list


def create_dict(filtered_list: list) -> dict:
    register_dict = {}
    register_dict["directorio"] = {
        member["nombre"]: member["nivel"] for member in filtered_list
    }
    register_dict["clases_unicas"] = {member["clase"] for member in filtered_list}
    register_dict["ricos"] = [
        member["nombre"]
        for member in sorted(filtered_list, key=lambda m: m["kamas"], reverse=True)
        if member["kamas"] > 1_000_000
    ]
    return register_dict


def achievements_report(members: list) -> dict:
    achievements_ranking = {
        member["nombre"]: len(member["logros"])
        for member in sorted(members, key=lambda m: len(m["logros"]), reverse=True)
    }

    all_achievements = [
        achievement for member in members for achievement in member["logros"]
    ]
    set_achievements = set(all_achievements)
    achievements_amount = {
        achievement: all_achievements.count(achievement)
        for achievement in set_achievements
    }
    most_common_achievement = max(achievements_amount, key=achievements_amount.get)

    exclusive_members = {
        member["nombre"]
        for member in members
        if not any(
            set(member["logros"]) == set(member2["logros"])
            for member2 in members
            if member2["nombre"] != member["nombre"]
        )
    }

    return {
        "ranking_logros": achievements_ranking,
        "logro_mas_comun": most_common_achievement,
        "miembros_exclusivos": exclusive_members,
    }


members = [
    {
        "nombre": "Arkhen",
        "clase": "Iop",
        "nivel": 187,
        "activo": True,
        "kamas": 4500000,
        "logros": ["Conquistador", "Gladiador", "Viajero"],
    },
    {
        "nombre": "Sylvara",
        "clase": "Eniripsa",
        "nivel": 134,
        "activo": True,
        "kamas": 890000,
        "logros": ["Sanador", "Viajero"],
    },
    {
        "nombre": "Drakthos",
        "clase": "Sram",
        "nivel": 200,
        "activo": False,
        "kamas": 12000000,
        "logros": ["Conquistador", "Sombra", "Leyenda"],
    },
    {
        "nombre": "Pumuki",
        "clase": "Osamodas",
        "nivel": 98,
        "activo": True,
        "kamas": 210000,
        "logros": ["Viajero"],
    },
    {
        "nombre": "Velkan",
        "clase": "Xelor",
        "nivel": 200,
        "activo": True,
        "kamas": 7800000,
        "logros": ["Leyenda", "Conquistador", "Cronista"],
    },
    {
        "nombre": "Nyra",
        "clase": "Cra",
        "nivel": 155,
        "activo": False,
        "kamas": 3300000,
        "logros": ["Gladiador", "Viajero", "Exploradora"],
    },
    {
        "nombre": "Zorrath",
        "clase": "Sacrier",
        "nivel": 176,
        "activo": True,
        "kamas": 670000,
        "logros": ["Gladiador", "Conquistador"],
    },
    {
        "nombre": "Thessia",
        "clase": "Eniripsa",
        "nivel": 143,
        "activo": True,
        "kamas": 1500000,
        "logros": ["Sanador", "Cronista", "Viajero"],
    },
]

cases = [
    {"name": "registro completo", "kwargs": {}},
    {"name": "solo activos", "kwargs": {"solo_activos": True}},
    {"name": "nivel >= 150", "kwargs": {"nivel_minimo": 150}},
    {"name": "clase Eniripsa", "kwargs": {"clase": "Eniripsa"}},
    {"name": "clave inválida", "kwargs": {"bad_key": True}},
]

for case in cases:
    print(f"--- Caso: {case['name']} ---")
    try:
        result = build_register(**case["kwargs"])
        print("directorio:", result["directorio"])
        print("clases_unicas:", sorted(result["clases_unicas"]))
        print("ricos:", result["ricos"])
    except Exception as error:
        print("Error:", type(error).__name__, error)
    print()

print("--- Reporte de logros ---")
report = achievements_report(members)
print("ranking_logros:", report["ranking_logros"])
print("logro_mas_comun:", report["logro_mas_comun"])
print("miembros_exclusivos:", sorted(report["miembros_exclusivos"]))