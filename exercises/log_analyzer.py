import random
from datetime import datetime
import os
from functools import wraps
from pprint import pprint

py_file_path = os.path.dirname(
    os.path.abspath(__file__)  # Route of the directory where .py file is
)


def create_serverlog():
    services = ["AuthService", "DBService", "APIGateway", "CacheService"]
    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    users = ["admin", "root", "support01", "operator", "supervisor"]
    crud = ["GET", "POST", "PUT", "DELETE"]
    endpoints = ["users", "products", "orders", "settings", "profile"]
    directory = os.path.join(py_file_path, "server.log")
    with open(directory, "w", encoding="utf-8") as log:
        for i in range(30):
            messages = [
                f"User {random.choice(users)} logged in",
                f"Connection timeout on port {random.randint(1000, 9999)}",
                f"{random.randint(1, 5)} failed attempts from user {random.choice(users)}",
                f"Request {random.choice(crud)} /api/v2/{random.choice(endpoints)} - {random.randint(1, 999)}ms",
            ]
            log.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {random.choice(levels)} | "
                f"{random.choice(services)} | {random.choice(messages)}\n"
            )


def register_operation(operation_name: str):

    def decorator_register_operation(original_function):

        @wraps(original_function)
        def wrapper_register_operation(*args, **kwargs):
            start_time = datetime.now()
            result = original_function(*args, **kwargs)
            end_time = datetime.now()
            total_time = end_time - start_time
            message = (
                f"[START] '{operation_name}' - {start_time.time().strftime('%H:%M:%S')}\n"
                f"[END] '{operation_name}' - {end_time.time().strftime('%H:%M:%S')}\n"
                f"[DURATION] '{operation_name}' - {total_time.total_seconds():.4f}s\n"
            )
            print(message, end="")
            directory = os.path.join(py_file_path, "auditory.log")
            with open(directory, "a", encoding="utf-8") as log:
                log.write(message)
            return result

        return wrapper_register_operation

    return decorator_register_operation


@register_operation("Load logs")
def load_logs(filepath):
    filepath = os.path.join(py_file_path, filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            keys = [
                {
                    "timestamp": split[0].strip(),
                    "level": split[1].strip(),
                    "service": split[2].strip(),
                    "message": split[3].strip(),
                }
                for line in f.readlines()
                for split in [line.split("|", maxsplit=3)]
                if len(split) >= 4
            ]
            f.seek(0)
            file_lines_amount = sum(1 for line in f)
            correct_lines_amount = len(keys)
            if file_lines_amount > correct_lines_amount:
                print(
                    f"There were {file_lines_amount - correct_lines_amount} lines that didn't "
                    "respect the format and weren't added to the list."
                )
    except FileNotFoundError:
        print(f"We couldn't find the file located at {filepath}.")
        raise
    except PermissionError:
        print(f"You don't have permission to access the file located at {filepath}.")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}.")
        raise
    return keys


@register_operation("Save report")
def save_report(logs: dict):
    filepath = os.path.join(py_file_path, "report.csv")
    valid_registers = [
        register for register in logs if register["level"] in ("ERROR", "CRITICAL")
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("timestamp,level,service,message\n")
        for register in valid_registers:
            f.write(
                f"{register["timestamp"]},{register["level"]},{register["service"]},{register["message"]}\n"
            )


@register_operation("Analyze logs")
def analyze_logs(logs: dict) -> dict:
    total_registers = len(logs)  # First pair
    all_levels = [log["level"] for log in logs]
    levels = set(all_levels)
    by_level = {level: all_levels.count(level) for level in levels}  # Second pair
    all_services = [log["service"] for log in logs]
    services = set(all_services)
    by_service = {  # Third pair
        service: all_services.count(service) for service in services
    }
    all_critic_services = [
        log["service"] for log in logs if log["level"] in ("ERROR", "CRITICAL")
    ]
    critic_services = set(all_critic_services)
    amount_critic_services = {
        service: all_critic_services.count(service) for service in critic_services
    }
    top3_critic_services = sorted(  # Fourth pair
        amount_critic_services,
        key=amount_critic_services.get,
        reverse=True,
    )[:3]
    all_hours = [log["timestamp"][11:13] for log in logs]
    hours = set(all_hours)
    registers_by_hour = {hour: all_hours.count(hour) for hour in hours}
    most_active_hour = max(registers_by_hour, key=registers_by_hour.get)  # Fifth pair
    ratio_error = round(len(all_critic_services) / total_registers, 4)  # Sixth pair
    return {
        "total_registers": total_registers,
        "by_level": by_level,
        "by_service": by_service,
        "top3_critic_services": top3_critic_services,
        "most_active_hour": most_active_hour,
        "ratio_error": ratio_error,
    }


@register_operation("Filter logs")
def filter_logs(logs: dict, *levels, service=None, has=None) -> list:
    if levels:
        logs = [log for log in logs if log["level"] in levels]
    if service:
        logs = [log for log in logs if log["service"] == service]
    if has:
        logs = [log for log in logs if has.lower() in log["message"].lower()]
    return list(logs)


print("Creating logs...")
create_serverlog()
print("\n=== LOGS ===")
logs = load_logs("server.log")
pprint(logs)
print("\n=== ANALYSIS ===")
data = analyze_logs(logs)
pprint(data)
print("\n=== FILTERING ===")
filtered = filter_logs(logs, "ERROR", "CRITICAL", service="DBService", has="TIMEOUT")
pprint(filtered)
print("\nSaving report...")
save_report(logs)
