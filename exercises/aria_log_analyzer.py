import json
from datetime import datetime
import random
from functools import wraps
import os
from pprint import pprint

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def audit(operation: str):

    def decorator_function_audit(original_function):

        @wraps(original_function)
        def wrapper_function_audit(*args, **kwargs):
            logs = []
            try:
                result = original_function(*args, **kwargs)
                status = "OK"
                if isinstance(result, (list, dict)):
                    detail = f"{len(result)} elements processed."
                else:
                    detail = "Ejecution completed succesfully."
            except Exception as e:
                status = "ERROR"
                detail = str(e)
                error = e

            if os.path.exists("auditory.json"):
                with open("auditory.json") as f:
                    logs = json.load(f)
            log = {
                "operation": operation,
                "function": original_function.__name__,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "status": status,
                "detail": detail,
            }
            logs.append(log)
            with open("auditory.json", "w") as f:
                json.dump(logs, f, indent=2)
            if log["status"] == "ERROR":
                raise error
            return result

        return wrapper_function_audit

    return decorator_function_audit


@audit("Generate logs")
def generate_logs(file: str, n: int):
    levels = ("INFO", "WARNING", "ERROR", "CRITICAL")
    modules = ("vission", "lenguage", "memory", "engine", "ethic")
    messages_by_level = {
        "INFO": [
            "Process started successfully",
            "Configuration loaded",
            "Connection established",
        ],
        "WARNING": [
            "Resource threshold approaching",
            "Slow response time detected",
            "Retry initiated",
        ],
        "ERROR": [
            "Failed to detect objects",
            "Database write error",
            "Invalid input format",
        ],
        "CRITICAL": [
            "Kernel panic occurred",
            "Memory leak detected",
            "Hardware failure imminent",
        ],
    }
    events = list()
    for i in range(n):
        random_level = random.choice(levels)
        if random.random() > 0.15:
            metrics = {
                "cpu": round(random.uniform(0, 100.0), 2),
                "ram": random.randint(500, 32000),
                "latency_ms": random.randint(0, 1000),
            }
        else:
            metrics = "CORRUPTED"
        events.append(
            {
                "id": i + 1,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "level": random_level,
                "module": random.choice(modules),
                "message": random.choice(messages_by_level[random_level]),
                "metrics": metrics,
            }
        )

    with open(file, "w") as f:
        json.dump(events, f, indent=2)


@audit("Load")
def load_logs(file: str) -> list:
    expected_keys = (
        "id",
        "level",
        "message",
        "metrics",
        "module",
        "timestamp",
    )
    valid_and_invalid_logs = []

    if not os.path.exists(file):
        print("File doesn't exists.")
        raise FileNotFoundError
    with open(file) as f:
        logs = json.load(f)

    for log in logs:
        failed = False
        errors = []
        missing_keys = []

        for expected_key in expected_keys:
            if expected_key not in log.keys():
                missing_keys.append(expected_key)
        if missing_keys:
            errors.append(f"Missing fields: {', '.join(missing_keys)}")
            failed = True

        if not isinstance(log.get("metrics"), dict):
            failed = True
            errors.append("Metrics is not a dictionary")

        if failed:
            log["_valid"] = False
            log["_reason"] = "; ".join(errors)
        else:
            log["_valid"] = True
        valid_and_invalid_logs.append(log)
    return valid_and_invalid_logs


generate_logs("logs.json", 150)
logs = load_logs("logs.json")
pprint(logs)
