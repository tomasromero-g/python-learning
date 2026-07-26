import json
import os
from functools import wraps

os.chdir(os.path.dirname(os.path.abspath(__file__)))
recruits = [
    {"class_name": "Warrior", "record": "Kael-12-150-30-20"},
    {"class_name": "Mage", "record": "Lyra-9-90-45-15"},
    {"class_name": "Warrior", "record": "bad-data"},
    {"class_name": "Necromancer", "record": "Zeta-5-60-20"},
]
filename = "recruits.json"
with open(filename, "w") as f:
    json.dump(recruits, f, indent=2)


class Adventurer:
    guild_tax = 0.1
    total_recruits = 0

    def __init__(self, *args):
        name, level, hp, attack = args
        stats = {"Level": level, "HP": hp, "Attack": attack}
        for stat, value in stats.items():
            if not isinstance(value, int):
                raise TypeError(
                    f"{stat} must be an integer, not a {type(value).__name__}"
                )

        self.name = name
        self.level = level
        self.hp = hp
        self.attack = attack

        Adventurer.total_recruits += 1

    def calculate_power(self) -> float:
        return (self.hp * 0.4) + (self.attack * 0.6) + (self.level * 5)

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "attack": self.attack,
        }

    @classmethod
    def from_record(cls, record: str):
        try:
            adventurer = record.split("-")
            adventurer[1], adventurer[2], adventurer[3] = (
                int(adventurer[1]),
                int(adventurer[2]),
                int(adventurer[3]),
            )
        except ValueError:
            raise ValueError("Level, HP and Attack must be integer values.")
        except IndexError:
            raise IndexError("You entered too few parameters for this class.")

        try:
            return cls(*adventurer)
        except ValueError:
            raise
        except TypeError:
            raise TypeError("You entered too many parameters for this class.")

    @staticmethod
    def is_raid_ready(min_level: int, adventurer_level: int) -> bool:
        return adventurer_level >= min_level


class Warrior(Adventurer):
    def __init__(self, name, level, hp, attack, armor):
        try:
            self.armor = int(armor)
        except ValueError:
            raise ValueError("Armor must be an integer value.")
        super().__init__(name, level, hp, attack)

    def calculate_power(self) -> float:
        return super().calculate_power() + self.armor * 2

    def to_dict(self):
        return super().to_dict() | {"armor": self.armor}


class Mage(Adventurer):
    guild_tax = 0.15

    def __init__(self, name, level, hp, attack, mana):
        try:
            self.mana = int(mana)
        except ValueError:
            raise ValueError("Mana must be an integer value.")
        super().__init__(name, level, hp, attack)

    def to_dict(self):
        return super().to_dict() | {"mana": self.mana}


def requires_min_level(n: int):

    def decorator_requires_min_level(original_function):

        @wraps(original_function)
        def wrapper_requires_min_level(adventurer, *args, **kwargs):
            if Adventurer.is_raid_ready(n, adventurer.level):
                return original_function(adventurer, *args, **kwargs)
            raise ValueError(
                f"You need to be level {n} to participate in the raid. Currently, you're level {adventurer.level}"
            )

        return wrapper_requires_min_level

    return decorator_requires_min_level


def create_from_report(filename):
    rejected = []
    adventurers = []
    available_classes = {"Warrior": Warrior, "Mage": Mage}
    with open(filename) as f:
        recruits = json.load(f)
    for recruit in recruits:
        try:
            adventurers.append(
                available_classes[recruit["class_name"]].from_record(recruit["record"])
            )
        except KeyError as e:
            recruit["error"] = f"Class {recruit['class_name']} does not exist."
            rejected.append(recruit)
        except ValueError as e:
            recruit["error"] = str(e)
            rejected.append(recruit)
        except IndexError as e:
            recruit["error"] = str(e)
            rejected.append(recruit)
        except TypeError as e:
            recruit["error"] = str(e)
            rejected.append(recruit)
    return adventurers, rejected


def adventurers_power(adventurers: list) -> list:
    return [adventurer.calculate_power() for adventurer in adventurers]


def adventurers_by_power(adventurers: list) -> list:
    return sorted(adventurers, key=lambda a: (-a.calculate_power(), a.name))


@requires_min_level(5)
def start_raid(adventurer: Adventurer):
    print("Starting raid...")
    print("Raid has started! Good luck, adventurer!")


def group_loot(total_gold: int, *adventurers, **bonuses) -> dict:
    gold_per_adventurer = {}
    bonuses_clean = {key.lower(): value for key, value in bonuses.items()}
    individual_gold = total_gold / len(adventurers)
    for adventurer in adventurers:
        current_gold = individual_gold
        if adventurer.name.lower() in bonuses_clean:
            current_gold += bonuses_clean[adventurer.name.lower()]
        gold_per_adventurer[adventurer.name] = round(
            current_gold * (1 - adventurer.guild_tax)
        )
    return gold_per_adventurer


def guild_report(sorted_adv: list, rejected_adv: list, gold_per_adv: dict):
    report = {}
    report["sorted_adventurers"] = [adv.to_dict() for adv in sorted_adv]
    report["rejected_adventurers"] = rejected_adv
    report["gold_per_adventurer"] = gold_per_adv
    with open("raid_report.json", "w") as f:
        json.dump(report, f, indent=2)


adventurers, rejected = create_from_report(filename)
all_powers = adventurers_power(adventurers)
sorted_by_power = adventurers_by_power(adventurers)
for adventurer in adventurers:
    start_raid(adventurer)
gold_per_adventurer = group_loot(5000, *adventurers, Lyra=150)
guild_report(sorted_by_power, rejected, gold_per_adventurer)
