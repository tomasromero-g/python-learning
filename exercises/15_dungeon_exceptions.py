import logging
from datetime import datetime
from functools import wraps
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logs = []


class DungeonError(Exception):
    def __init__(self, room_numb: int, message: str):
        self.room_numb = room_numb
        super().__init__(message)


class TrapTriggered(DungeonError):
    def __init__(self, room_numb: int, trap_type: str, dmg: int):
        self.trap_type = trap_type
        self.dmg = dmg
        super().__init__(
            room_numb,
            f"You've stepped on a {trap_type} trap and received {dmg} damage.",
        )


class OutOfResources(DungeonError):
    def __init__(
        self, room_numb: int, resource: str, missing_amount: int, needed_amount: int
    ):
        self.resource = resource
        self.missing_amount = missing_amount
        self.needed_amount = needed_amount
        super().__init__(
            room_numb,
            f"Out of {resource}. You needed {needed_amount} but you're lacking {missing_amount}.",
        )


class ImpossibleMob(DungeonError):
    def __init__(self, room_numb: int, monster_lv: int, group_lv: int):
        self.monster_lv = monster_lv
        self.group_lv = group_lv
        super().__init__(
            room_numb,
            f"Your group level must be at least {monster_lv} to fight this monster. Your group level is {group_lv}.",
        )


class Adventurer:
    def __init__(self, name: str, hp: int, lv: int, inventory: list):
        self.name = name
        self.hp = hp
        self.lv = lv
        self.inventory = inventory if inventory else []


class Room:
    def __init__(
        self,
        name: str,
        numb: int,
        error_prob: float,
        exc_types: list,
    ):
        self.name = name
        self.numb = numb
        self.error_prob = error_prob
        self.exc_types = exc_types


class EnterRoom:
    def __init__(self, room_numb: int):
        self.room_numb = room_numb

    def __enter__(self):
        logger.info("The user has entered the room.")
        self.enter_time = datetime.now()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        log = {
            "enter_time": self.enter_time.strftime("%H:%M:%S"),
            "room_numb": self.room_numb,
            "exc_type": str(exc_type) if exc_type else None,
            "exc_value": exc_value,
        }
        logs.append(log)
        return False


def retry_on(exc_types: list, n: int):

    def decorator(original_function):

        @wraps(original_function)
        def wrapper(*args, **kwargs):
            for i in range(n):
                try:
                    result = original_function(*args, **kwargs)
                    return result
                except Exception as e:
                    if isinstance(e, tuple(exc_types)):
                        if i + 1 == n:
                            raise RuntimeError("You ran out of attempts.") from e
                        logger.info(f"Retrying function... attempt {i + 1}.")
                    else:
                        raise

        return wrapper

    return decorator


@retry_on([TrapTriggered, OutOfResources, ImpossibleMob], 3)
def explore_room(room: Room):
    if not round(random.random(), 2) <= room.error_prob:
        logger.info("Room explored succesfully.")
        return
    e = random.choice(room.exc_types)
    if e == TrapTriggered:
        trap_types = ["Poison", "Fire", "Wind"]
        raise e(room.numb, random.choice(trap_types), random.randint(50, 1000))
    elif e == OutOfResources:
        resources = ["Wood", "Stone", "Elixir"]
        raise e(
            room.numb,
            random.choice(resources),
            random.randint(1, 3),
            random.randint(5, 10),
        )
    elif e == ImpossibleMob:
        raise e(room.numb, random.randint(50, 100), random.randint(40, 49))
    else:
        raise ValueError("Uknown exception.")


def traverse_rooms(rooms: list):
    for room in rooms:
        with EnterRoom(room.numb):
            explore_room(room)


adventurers = [
    Adventurer("Aran", 100, 5, ["potion", "sword"]),
    Adventurer("Beli", 80, 4, ["potion"]),
    Adventurer("Coro", 90, 6, []),
]

rooms = [
    Room("Trap Corridor", 1, 0.3, [TrapTriggered]),
    Room("Empty Storage", 2, 0.5, [OutOfResources]),
    Room("Dragon's Lair", 3, 0.2, [ImpossibleMob]),
    Room("Quiet Hallway", 4, 0.1, [TrapTriggered, OutOfResources]),
]


traverse_rooms(rooms)
