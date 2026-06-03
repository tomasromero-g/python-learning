import random
from datetime import datetime
import os
from functools import wraps


def create_serverlog():
    services = ["AuthService", "DBService", "APIGateway", "CacheService"]
    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    users = ["admin", "root", "support01", "operator", "supervisor"]
    crud = ["GET", "POST", "PUT", "DELETE"]
    endpoints = ["users", "products", "orders", "settings", "profile"]

    py_file_path = os.path.dirname(
        os.path.abspath(__file__)  # Route of the directory where .py file is
    )
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
                f"{datetime.now()} | {random.choice(levels)} | {random.choice(services)} | {random.choice(messages)}\n"
            )


def register_operation(operation_name):

    def decorator_register_operation(original_function):

        @wraps(original_function)
        def wrapper_register_operation(*args, **kwargs):
            return original_function(*args, **kwargs)

        return wrapper_register_operation

    return decorator_register_operation


@register_operation
def load_logs(filepath):
    pass


create_serverlog()
