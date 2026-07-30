import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Vehicle:
    created_vehicles = 0

    def __init__(
        self,
        vehicle_id: str,
        brand: str,
        model: str,
        max_range_km: int,
        battery_level: int,
    ):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.max_range_km = max_range_km
        self.battery_level = battery_level

        Vehicle.created_vehicles += 1

    def __str__(self):
        return (
            f"ID: {self.vehicle_id} | Brand: {self.brand} | Model: {self.model} | "
            f"Max range: {self.max_range_km}km | Battery level: {self.battery_level}%"
        )

    def __repr__(self):
        return f"Vehicle({self.vehicle_id!r}, {self.brand!r}, {self.model!r}, {self.max_range_km}, {self.battery_level})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.vehicle_id == other.vehicle_id

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.battery_level < other.battery_level

    def __add__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return Vehicle(
            f"{self.vehicle_id}+{other.vehicle_id}",
            f"HYBRID {self.brand}, {other.brand}",
            f"HYBRID {self.model}, {other.model}",
            self.max_range_km + other.max_range_km,
            int((self.battery_level + other.battery_level) / 2),
        )

    @classmethod
    def from_string(cls, string):
        expected_length = 5
        try:
            vehicle = string.split("|")
            vehicle_id, brand, model, max_range_km, battery_level = vehicle
            max_range_km, battery_level = int(max_range_km), int(battery_level)
        except ValueError:
            if len(vehicle) != expected_length:
                raise ValueError(
                    f"Expected {expected_length} pipe-separated values '|', but got {len(vehicle)}."
                )
            raise ValueError(
                "Invalid format: 'max_range_km' and 'battery_level' must be convertible to integers."
            )
        return cls(vehicle_id, brand, model, max_range_km, battery_level)

    @staticmethod
    def is_valid_battery(battery_level):
        return 0 <= battery_level <= 100

    @property
    def battery_level(self):
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value):
        if not Vehicle.is_valid_battery(value):
            raise ValueError(
                f"Expected battery value between 0 and 100, but got {value}."
            )
        self._battery_level = value

    @property
    def status(self):
        if 0 <= self.battery_level < 25:
            return "critical"
        elif 25 <= self.battery_level < 50:
            return "low"
        elif 50 <= self.battery_level < 75:
            return "ok"
        else:
            return "full"


class DeliveryDrone(Vehicle):
    def __init__(
        self,
        vehicle_id: str,
        brand: str,
        model: str,
        max_range_km: int,
        battery_level: int,
        payload_kg: int,
    ):
        super().__init__(vehicle_id, brand, model, max_range_km, battery_level)
        self.payload_kg = payload_kg

    def __str__(self):
        return super().__str__() + f" | Payload: {self.payload_kg}kg"

    def __repr__(self):
        return (
            f"DeliveryDrone({self.vehicle_id!r}, {self.brand!r}, "
            f"{self.model!r}, {self.max_range_km}, {self.battery_level}, {self.payload_kg})"
        )

    def __add__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return DeliveryDrone(
            f"{self.vehicle_id}+{other.vehicle_id}",
            f"HYBRID {self.brand}, {other.brand}",
            f"HYBRID {self.model}, {other.model}",
            self.max_range_km + other.max_range_km,
            int((self.battery_level + other.battery_level) / 2),
            self.payload_kg + other.payload_kg,
        )

    @classmethod
    def from_string(cls, string):
        expected_length = 6
        try:
            d_drone = string.split("|")
            vehicle_id, brand, model, max_range_km, battery_level, payload_kg = d_drone
            max_range_km, battery_level, payload_kg = (
                int(max_range_km),
                int(battery_level),
                int(payload_kg),
            )
        except ValueError:
            if len(d_drone) != expected_length:
                raise ValueError(
                    f"Expected {expected_length} pipe-separated values '|', but got {len(d_drone)}."
                )
            raise ValueError(
                "Invalid format: 'max_range_km', 'battery_level' and 'payload_kg' must be convertible to integers."
            )
        return cls(vehicle_id, brand, model, max_range_km, battery_level, payload_kg)


class CargoTruck(Vehicle):
    def __init__(
        self,
        vehicle_id: str,
        brand: str,
        model: str,
        max_range_km: int,
        battery_level: int,
        trailer_count: int,
    ):
        super().__init__(vehicle_id, brand, model, max_range_km, battery_level)
        self.trailer_count = trailer_count

    def __str__(self):
        return super().__str__() + f" | Trailer count: {self.trailer_count}"

    def __repr__(self):
        return (
            f"CargoTruck({self.vehicle_id!r}, {self.brand!r}, "
            f"{self.model!r}, {self.max_range_km}, {self.battery_level}, {self.trailer_count})"
        )

    def __add__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return CargoTruck(
            f"{self.vehicle_id}+{other.vehicle_id}",
            f"HYBRID {self.brand}, {other.brand}",
            f"HYBRID {self.model}, {other.model}",
            self.max_range_km + other.max_range_km,
            int((self.battery_level + other.battery_level) / 2),
            self.trailer_count + other.trailer_count,
        )

    @classmethod
    def from_string(cls, string):
        expected_length = 6
        try:
            c_truck = string.split("|")
            vehicle_id, brand, model, max_range_km, battery_level, trailer_count = (
                c_truck
            )
            max_range_km, battery_level, trailer_count = (
                int(max_range_km),
                int(battery_level),
                int(trailer_count),
            )
        except ValueError:
            if len(c_truck) != expected_length:
                raise ValueError(
                    f"Expected {expected_length} pipe-separated values '|', but got {len(c_truck)}."
                )
            raise ValueError(
                "Invalid format: 'max_range_km', 'battery_level' and 'trailer_count' must be convertible to integers."
            )
        return cls(vehicle_id, brand, model, max_range_km, battery_level, trailer_count)


class FleetManager:
    def __init__(self, vehicles=None):
        self.vehicles = vehicles if vehicles is not None else {}

    def add_vehicle(self, *args, **kwargs):
        if args:
            if not isinstance(args[0], Vehicle):
                raise TypeError(
                    f"Expected a Vehicle instance in args, but got {type(args[0]).__name__}."
                )
            vehicle = args[0]
        if kwargs:
            string = ""
            for index, value in enumerate(kwargs.values()):
                if index == len(kwargs) - 1:
                    string += f"{value}"
                    break
                string += f"{value}|"

            if "payload_kg" in kwargs.keys():
                vehicle = DeliveryDrone.from_string(string)
            elif "trailer_count" in kwargs.keys():
                vehicle = CargoTruck.from_string(string)
            else:
                vehicle = Vehicle.from_string(string)
        if self.vehicles.get(vehicle.vehicle_id):
            raise ValueError(
                f"There is already a vehicle with the id {vehicle.vehicle_id}."
            )
        self.vehicles[vehicle.vehicle_id] = vehicle
        return

    def get_critical_vehicles(self):
        critical_status = ("critical", "low")
        return [
            vehicle
            for vehicle in self.vehicles.values()
            if vehicle.status in critical_status
        ]

    def sort_fleet(self, key="max_range_km", reverse=True):
        return sorted(
            self.vehicles.values(), key=lambda v: getattr(v, key), reverse=reverse
        )

    def export_status(self, filename):
        vehicle_status = {}
        for vehicle in self.vehicles.values():
            vehicle_status[vehicle.vehicle_id] = vehicle.status
        with open(filename, "w") as f:
            json.dump(vehicle_status, f, indent=2)


v1 = Vehicle.from_string("CHV-103|Chevrolet|Cruze|13000|100")
v2 = Vehicle.from_string("NSN-182|Nissan|GTR|15000|78")
d1 = DeliveryDrone.from_string("001|Uber|TestModel|1500|54|5")
d2 = DeliveryDrone.from_string("002|Tesla|TestModel|3000|99|15")
c1 = CargoTruck.from_string("001|Trucks|TestModel|90000|37|100")
c2 = CargoTruck.from_string("002|Trucks|TestModel|184782|58|987")
manager = FleetManager()
manager.add_vehicle(v1)
manager.add_vehicle(d1)
manager.add_vehicle(c2)
manager.add_vehicle(
    id="CHV-003", brand="Chevrolet", model="Onix", max_range_km=1000, battery_level=38
)
manager.export_status("vehicles.json")
