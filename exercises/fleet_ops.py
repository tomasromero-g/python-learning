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


v1 = Vehicle.from_string("CHV-103|Chevrolet|Cruze|32|100")
print(v1)
print(repr(v1))
