import json
import os
from pprint import pprint

os.chdir(os.path.dirname(os.path.abspath(__file__)))
recruits = [
    {"class_name": "Warrior", "record": "Kael-12-150-30"},
    {"class_name": "Mage", "record": "Lyra-9-90-45"},
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

    def calculate_power(self):
        return (self.hp * 0.4) + (self.attack * 0.6) + (self.level * 5)

    @classmethod
    def from_record(cls, record):
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
            raise IndexError("You entered less parameters than the class needed.")

        try:
            return cls(*adventurer)
        except ValueError:
            raise
        except TypeError:
            raise TypeError("You entered more parameters than the class needed.")

    @staticmethod
    def is_raid_ready(min_level, adventurer_level):
        return adventurer_level >= min_level


class Warrior(Adventurer):
    def __init__(self, name, level, hp, attack, armor):
        try:
            self.armor = int(armor)
        except ValueError:
            raise ValueError("Armor must be an integer value.")
        super().__init__(name, level, hp, attack)

    def calculate_power(self):
        return super().calculate_power() + self.armor * 2


class Mage(Adventurer):
    guild_tax = 0.15

    def __init__(self, name, level, hp, attack, mana):
        try:
            self.mana = int(mana)
        except ValueError:
            raise ValueError("Mana must be an integer value.")
        super().__init__(name, level, hp, attack)


def create_from_report(filename):  # INCOMPLETE
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
            recruit["error"] = str(e)
            rejected.append(recruit)
        except ValueError as e:
            recruit["error"] = str(e)
            rejected.append(recruit)
    return adventurers, rejected


Mage.from_record("Tomi-150")
