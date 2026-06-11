import json
from datetime import datetime
import random
from functools import wraps
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


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


# Unfinished
def audit(operation: str):

    def decorator_function_audit(original_function):

        @wraps(original_function)
        def wrapper_function_audit(*args, **kwargs):
            return original_function()

        return wrapper_function_audit

    return decorator_function_audit


generate_logs("logs.json", 100)
