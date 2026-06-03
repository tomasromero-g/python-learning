import time
from functools import wraps
import inspect


def log_call(original_function):

    @wraps(original_function)
    def log_wrapper(*args, **kwargs):
        log = {}
        log["timestamp"] = round(time.time(), 2)
        log["function"] = original_function.__name__
        log["args"] = args
        log["kwargs"] = kwargs
        try:
            result = original_function(*args, **kwargs)
            log["status"] = "ok"
            log["result"] = result
        except Exception as e:
            result = e
            log["status"] = "error"
            log["result"] = result
            audit_log.append(log)
            raise
        audit_log.append(log)
        return result

    return log_wrapper


# Structure: player = {"name": "Iop", "role": "Warrior", "level": 45, ...}
def require_role(*allowed_roles):

    def role_decorator_function(original_function):

        @wraps(original_function)
        def role_wrapper(*args, **kwargs):
            player = kwargs.get("player")
            if not player:
                raise ValueError("No ingresaste la información del jugador.")
            if not player.get("role"):
                raise KeyError("No ingresaste el rol.")
            if not (player["role"].lower() in allowed_roles):
                raise UnauthorizedRoleError(
                    f"Tu rol '{player['role']}' no está entre los permitidos para esta funcionalidad."
                )
            return original_function(*args, **kwargs)

        return role_wrapper

    return role_decorator_function


def validate_args(**expected_types):

    def validateargs_decorator_function(original_function):

        @wraps(original_function)
        def validateargs_wrapper(*args, **kwargs):
            params = inspect.getfullargspec(original_function).args
            for key, value in expected_types.items():
                if key in params:

                    if not (key in kwargs):
                        index = params.index(key)
                        if not (isinstance(args[index], value)):
                            raise TypeError(
                                f"Parámetro '{key}: {args[index]}': se esperaba {value.__name__},"
                                f" se recibió {type(args[index]).__name__}"
                            )
                        continue

                    else:
                        if not (isinstance(kwargs[key], value)):
                            raise TypeError(
                                f"Parámetro '{key}: {kwargs[key]}': se esperaba {value.__name__},"
                                f" se recibió {type(kwargs[key]).__name__}"
                            )
                        continue

                raise KeyError(
                    f"Parámetro {key} no fue encontrado en los argumentos de la llamada."
                )
            return original_function(*args, **kwargs)

        return validateargs_wrapper

    return validateargs_decorator_function


class UnauthorizedRoleError(Exception):
    pass


@log_call
@require_role("admin", "moderator")
@validate_args(target_name=str, player=dict)
def ban_player(target_name: str, player: dict = None):
    print("===============")
    print(f"Buscando jugador {target_name}...")
    print("===============")
    print(f"Jugador {target_name} encontrado.")
    print("===============")
    print("Baneando...")
    print("===============")
    print(f"Jugador {target_name} baneado.")
    print("===============")


@log_call
@require_role("warrior", "sacrier")
@validate_args(skill_name=str, player=dict)
def use_skill(skill_name: str, player: dict = None):
    print("===============")
    print(f"Usando skill {skill_name}...")
    print("===============")
    print("Skill utilizada con éxito!")
    print("===============")


@log_call
@require_role("admin", "moderator")
@validate_args(target_name=str, level=int, player=dict)
def promote_player(target_name: str, level: int, player: dict = None):
    print("===============")
    print(f"Promoviendo jugador {target_name}...")
    print("===============")
    print(f"Aumentando su nivel de {level} a {level + 10}...")
    print("===============")
    print("Jugador promovido con éxito!")
    print("===============")


def report():
    total_calls = len(audit_log)
    succesful_calls = sum(1 for log in audit_log if log.get("status") == "ok")
    failed_calls = sum(1 for log in audit_log if log.get("status") == "error")
    error_rate = round(failed_calls / total_calls, 1)
    all_functions = [log["function"] for log in audit_log]
    set_functions = set(all_functions)
    functions_amount = {funct: all_functions.count(funct) for funct in set_functions}
    most_called = max(functions_amount, key=functions_amount.get)
    errors_amount = [log["function"] for log in audit_log if log["status"] == "error"]
    functions_with_errors = set(filter(lambda f: f in errors_amount, set_functions))
    errors_by_function = {
        function_name: errors_amount.count(function_name)
        for function_name in functions_with_errors
    }
    return {
        "total_calls": total_calls,
        "succesful_calls": succesful_calls,
        "failed_calls": failed_calls,
        "error_rate": error_rate,
        "most_called": most_called,
        "errors_by_function": errors_by_function
        }


audit_log = []

class FaultyInt(int):
    def __add__(self, other):
        raise RuntimeError("Error interno de la función")

try:
    ban_player("Valkyr", player={"name": "AdminUser", "role": "admin"})
except Exception as e:
    print(f"Capturado: {type(e).__name__} - {e}")

try:
    promote_player("Héroe", 5, player={"name": "AdminUser", "role": "admin"})
except Exception as e:
    print(f"Capturado: {type(e).__name__} - {e}")

try:
    ban_player("Tramposo", player={"name": "Noob", "role": "sacrier"})
except Exception as e:
    print(f"Capturado: {type(e).__name__} - {e}")

try:
    use_skill("Disparo", player={"name": "Archer", "role": "archer"})
except Exception as e:
    print(f"Capturado: {type(e).__name__} - {e}")

try:
    promote_player("Héroe", "diez", player={"name": "AdminUser", "role": "admin"})
except Exception as e:
    print(f"Capturado: {type(e).__name__} - {e}")

try:
    promote_player("Buggy", FaultyInt(3), player={"name": "AdminUser", "role": "admin"})
except Exception as e:
    print(f"Capturado: {type(e).__name__} - {e}")

print(report())