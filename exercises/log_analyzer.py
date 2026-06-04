import random
from datetime import datetime
import os
from functools import wraps

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
                f"[DURATION] '{operation_name}' - {total_time.total_seconds():4f}s\n"
            )
            print(message)
            directory = os.path.join(py_file_path, "auditory.log")
            with open(directory, "a", encoding="utf-8") as log:
                log.write(message)
            return result

        return wrapper_register_operation

    return decorator_register_operation


# Unfinished
@register_operation("Load logs")
def load_logs(filepath):
    try:
        with open(filepath, "r") as f:
            while True:
                line = f.readline()
                parts = line.split("|", maxsplit=3)      
    except FileNotFoundError:
        print(f"We couldn't find the file located at {filepath}.")
        raise
    except PermissionError:
        print(f"You don't have permission to access the file located at {filepath}.")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}.")
        raise


create_serverlog()
load_logs("a")
