from functools import wraps


class Creature:
    allowed_types = ("magic", "physic", "assasin", "summoner")
    total_population = 0
    global_bestiary = []

    def __init__(self, name, creature_type, hp, attack, defense, **kwargs):
        if not hp > 0:
            raise ValueError("HP must be greater than zero.")
        if not attack >= 0:
            raise ValueError("Attack must be greater than or equal to zero.")
        if not defense >= 0:
            raise ValueError("Defense must be greater than or equal to zero.")
        if not creature_type.lower() in Creature.allowed_types:
            raise ValueError(
                f"Creature's type '{creature_type}' isn't part of the allowed types."
            )

        self.name = name
        self.creature_type = creature_type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.extra_attributes = kwargs

        Creature.total_population += 1
        if Creature.total_population % 5 == 0:
            self.defense = round(self.defense * 1.2)
        Creature.global_bestiary.append(self)

    def calculate_power(self) -> float:
        return round((self.attack * 2) + (self.defense * 1.5) + (self.hp * 0.1), 2)


def summon_validator(hp_min, atk_min, def_min):

    def decorator_summon_validator(original_function):

        @wraps(original_function)
        def wrapper_summon_validator(*args, **kwargs):
            if not "hp" in kwargs.keys():
                raise ValueError("Required parameter 'HP' is missing.")
            if kwargs["hp"] < hp_min:
                raise ValueError(f"HP must be greater or equal than {hp_min}.")
            if not "attack" in kwargs.keys():
                raise ValueError("Required parameter 'Attack' is missing.")
            if kwargs["attack"] < atk_min:
                raise ValueError(f"Attack must be greater or equal than {atk_min}.")
            if not "defense" in kwargs.keys():
                raise ValueError("Required parameter 'Defense' is missing.")
            if kwargs["defense"] < def_min:
                raise ValueError(f"Defense must be greater or equal than {def_min}.")
            return original_function(*args, **kwargs)

        return wrapper_summon_validator

    return decorator_summon_validator


def summon_creature(**kwargs):
    pass


giga_zombie = Creature("Giga zombie", "Physic", 50000, 130, 200, phases=2)
