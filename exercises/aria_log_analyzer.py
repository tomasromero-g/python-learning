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
            error = None
            try:
                result = original_function(*args, **kwargs)
                status = "OK"
                if isinstance(result, (list, dict)):
                    detail = f"{len(result)} elements processed."
                else:
                    detail = "Execution completed succesfully."
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


@audit("Generation")
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


@audit("Loading")
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


@audit("Reparation")
def repair_logs(logs: list) -> dict:
    repaired = []
    unrecoverable = []
    clean = []
    for log in logs:
        if log["_valid"]:
            clean.append(log)
        elif "missing" in log["_reason"].lower():
            unrecoverable.append(log)
        else:
            log["metrics"] = {"cpu": -1, "ram": -1, "latency_ms": -1}
            log["_repaired"] = True
            repaired.append(log)
    return {"repaired": repaired, "unrecoverable": unrecoverable, "clean": clean}


@audit("Consult")
def analyze(repaired_logs: dict, **filters) -> list:
    logs = repaired_logs["repaired"] + repaired_logs["clean"]
    if "level" in filters:
        logs = [log for log in logs if log["level"] == filters["level"]]
    if "module" in filters:
        logs = [log for log in logs if log["module"] == filters["module"]]
    if "cpu_min" in filters:
        logs = [log for log in logs if log["metrics"]["cpu"] >= filters["cpu_min"]]
    if "valids_only" in filters:
        logs = [log for log in logs if log.get("_valid")]
    return sorted(
        logs, key=lambda l: (l["timestamp"], l["metrics"]["latency_ms"]), reverse=True
    )


@audit("Report")
def export_report(repaired_logs: dict, output_file: str):
    logs = (
        repaired_logs["repaired"]
        + repaired_logs["clean"]
        + repaired_logs["unrecoverable"]
    )
    total = len(logs)
    valids = len([log for log in logs if log["_valid"]])
    repaired = len(repaired_logs["repaired"])
    unrecoverables = len(repaired_logs["unrecoverable"])
    all_levels_logs = [log["level"] for log in logs if log.get("level")]
    levels_set = set(all_levels_logs)
    by_level = {level: all_levels_logs.count(level) for level in levels_set}
    all_modules_logs = [log["module"] for log in logs if log.get("module")]
    modules_set = set(all_modules_logs)
    by_module = {module: all_modules_logs.count(module) for module in modules_set}
    all_latencys = sum(log["metrics"]["latency_ms"] for log in repaired_logs["clean"])
    avg_latency_ms = round(
        all_latencys / len(repaired_logs["clean"]) if repaired_logs["clean"] else 0, 2
    )
    all_critical_error = [
        log
        for log in repaired_logs["clean"]
        if log["level"] in ("CRITICAL", "ERROR") and log["metrics"]["cpu"] > 85
    ]
    critical_events = sorted(
        all_critical_error, key=lambda l: l["metrics"]["latency_ms"], reverse=True
    )
    top5_high_cpu = sorted(
        repaired_logs["clean"], key=lambda l: l["metrics"]["cpu"], reverse=True
    )[0:5]
    with open(output_file, "w") as f:
        report = {
            "summary": {
                "total": total,
                "valids": valids,
                "repaired": repaired,
                "unrecoverables": unrecoverables,
                "by_level": by_level,
                "by_module": by_module,
                "avg_latency_ms": avg_latency_ms,
            },
            "critical_events": critical_events,
            "top5_high_cpu": top5_high_cpu,
        }
        json.dump(report, f, indent=2)


generate_logs("logs.json", 1500)
logs = load_logs("logs.json")
repaired_logs = repair_logs(logs)
filtered_logs = analyze(repaired_logs)
export_report(repaired_logs, "report.json")
