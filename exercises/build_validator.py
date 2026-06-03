def validate_stats(stats: dict):
    for key in stats.keys():  # All keys are valid?
        if not (key in valid_stats):
            raise KeyError(f"El stat {key} no es válido.")
    for value in stats.values():
        if not isinstance(value, int):  # Is integer?
            raise TypeError(f"El valor {value} no es entero, es {type(value)}")
        if value < 0:  # Is negative?
            raise ValueError(f"El valor {value} es negativo.")
    if sum(stats.values()) != total_points:  # It sums 150?
        raise ValueError(
            f"La suma de stats no da {total_points}, da {sum(stats.values())}"
        )


def validate_class(charclass: str, stats: dict):
    if not charclass in valid_classes:
        raise ValueError(f"La clase {charclass} no es válida.")
    for stat, value in class_requirements[charclass].items():
        user_stat_value = stats[stat]
        if user_stat_value < value:
            raise ValueError(
                f"Clase {charclass} no cumple requisitos: "
                f"{stat} necesita {value}, tenés {user_stat_value} (faltan {value - user_stat_value})"
            )


def register_build(name: str, charclass: str, **stats) -> dict:
    try:
        validate_stats(stats)
        validate_class(charclass, stats)
    except KeyError as e:
        print(f"Error de clave. {e}")
    except TypeError as e:
        print(f"Error de tipo. {e}")
    except ValueError as e:
        print(f"Error de valor. {e}")
    else:
        new_build = {}
        total_power = (
            lambda s: s["fuerza"] * 0.4
            + s["inteligencia"] * 0.35
            + s["agilidad"] * 0.25
        )
        new_build = {
            "nombre": name,
            "clase": charclass,
            "stats": stats,
            "poder_total": total_power(stats),
        }
        return new_build
    finally:
        print(f"[LOG] Intento de registro procesado para: {name}")


def process_builds(builds_list: list) -> list:
    passed = []
    failed = []
    for build in builds_list:
        result = register_build(build[0], build[1], **build[2])
        if result:
            passed.append(result)
        else:
            failed.append(build[0])
    return passed, failed


valid_stats = ["fuerza", "agilidad", "inteligencia", "defensa", "suerte"]
valid_classes = ["guerrero", "mago", "arquero", "asesino"]

class_requirements = {
    "guerrero": {"fuerza": 40, "defensa": 30},
    "mago": {"inteligencia": 50, "suerte": 20},
    "arquero": {"agilidad": 45, "suerte": 25},
    "asesino": {"agilidad": 50, "fuerza": 30},
}

total_points = 150  # Each build must sum exactly this

test_builds = [
    (
        "Arthas",
        "guerrero",
        {"fuerza": 70, "agilidad": 20, "inteligencia": 10, "defensa": 30, "suerte": 20},
    ),
    (
        "Jaina",
        "mago",
        {"fuerza": 10, "agilidad": 15, "inteligencia": 80, "defensa": 20, "suerte": 25},
    ),
    (
        "Glitch",
        "arquero",
        {"fuerza": 20, "agilidad": 40, "inteligencia": 10, "defensa": 30, "suerte": 50},
    ),  # requirement error
    (
        "Error404",
        "mago",
        {
            "fuerza": "mucho",
            "agilidad": 10,
            "inteligencia": 50,
            "defensa": 30,
            "suerte": 10,
        },
    ),  # type error
    (
        "Sombra",
        "asesino",
        {"fuerza": 40, "agilidad": 60, "inteligencia": 10, "defensa": 20, "suerte": 20},
    ),
    (
        "Roto",
        "mago",
        {"fuerza": 10, "agilidad": 10, "inteligencia": 50, "defensa": 10, "suerte": 10},
    ),  # sum error
]

print("=== Prueba individual de register_build ===")
for name, charclass, stats in test_builds:
    print(f"\nBuild: {name} ({charclass})")
    build = register_build(name, charclass, **stats)
    if build:
        print("Registrado con éxito:", build)
    else:
        print("No se registró.")

print("\n=== Resumen con process_builds ===")
passed, failed = process_builds(test_builds)
print("Pasaron:", [b["nombre"] for b in passed])
print("Fallaron:", failed)
