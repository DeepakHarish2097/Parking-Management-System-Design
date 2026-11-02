import math
from datetime import datetime
from uuid import uuid4

VEHICLE_SPACES = ["two_wheeler", "compact", "large"]

vehicle_rate_info = {
    "bike": {
        "spaces": VEHICLE_SPACES[0:1],
        "first_2hr": 30,
        "after_2hr": 50,
    },
    "car": {
        "spaces": VEHICLE_SPACES[1:],
        "first_2hr": 50,
        "after_2hr": 75,
    },
    "truck": {
        "spaces": VEHICLE_SPACES[-1:],
        "first_2hr": 75,
        "after_2hr": 100,
    },
}


class Vehicle:
    def __init__(self, name: str, type: str, space: str, time: str, floor: int, slot: int) -> None:
        self.name = name.replace(" ", '')
        self.type = type
        self.space = space
        self.floor_no = floor
        self.slot_no = slot
        self.in_time = None

        hour, minute = time.split(":")
        if hour.isdigit() and minute.isdigit():
            today = datetime.now()
            self.in_time = datetime(today.year, today.month, today.day, int(hour), int(minute))
        else:
            raise TypeError("Time must be only in numbers")

    def get_info(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"""
Name: {self.name}
Type: {self.type}
In Time: {self.in_time.strftime("%d/%m/%Y, %H:%M")}
Floor: {self.floor_no}
Slot: {self.slot_no}
Space: {self.space}
"""


class Slot:
    def __init__(self, number: int, floor: int, space: str) -> None:
        self.number = number
        self.floor_no = floor
        self.space = space
        self.occupied: bool = False
        self.vehicle: str | None = None
        self.vehicle_type: str | None = None
        self.in_time: datetime | None = None

    def get_info(self) -> str:
        return_string = self.__str__()
        if not self.occupied:
            return return_string

        return_string += f"""Vehicle: {self.vehicle}
Vehicle Type: {self.vehicle_type}
In Time: {self.in_time.strftime("%d/%m/%Y, %H:%M")}
"""
        return return_string

    def __str__(self) -> str:
        return f"""
Slot Number: {self.number}
Floor Number: {self.floor_no}
Space: {self.space}
Occupied: {self.occupied}
"""


class Floor:
    def __init__(self, number: int) -> None:
        self.number = number
        self.slot_details = {i: {
            "available": 0,
            "queue": [],             # using list for now but need to implement a better efficient alternative
            "slots": {}
        } for i in VEHICLE_SPACES}
        self.total_slots = 0
        self.available_slots = 0

    def get_info(self) -> str:
        return self.__str__()

    def create_slots(self, slots: int) -> None:
        count = 0
        for space in VEHICLE_SPACES:
            for _ in range(slots):
                count += 1
                slot = Slot(count, self.number, space)
                self.slot_details[space]['available'] += 1
                self.slot_details[space]['queue'].append(count)
                self.slot_details[space]['slots'][count] = slot
                self.total_slots += 1
                self.available_slots += 1

    def get_slot(self, spaces: list[str]) -> Slot | None:
        slot = None
        for space in spaces:
            if self.slot_details[space]['available'] > 0:
                s_no = self.slot_details[space]['queue'][0]
                slot = self.slot_details[space]['slots'][s_no]
            if slot:
                break
        return slot

    def __str__(self) -> str:
        return f"""
Floor Number: {self.number}
Total Slots: {self.total_slots}
Available Slots: {self.available_slots}
"""


class ParkingDetail:
    def __init__(
        self,
        vehicle: str,
        vehicle_type: str,
        space: str,
        floor: int,
        slot: int,
        in_time: datetime,
        out_time: datetime,
        fare: float
    ) -> None:
        self.id = str(uuid4())
        self.vehicle = vehicle
        self.vehicle_type = vehicle_type
        self.space = space
        self.floor_no = floor
        self.slot_no = slot
        self.in_time = in_time
        self.out_time = out_time
        self.fare = float(fare)

    def get_info(self) -> str:
        return self.__str__() + f"""Vehicle Type: {self.vehicle_type}
Slot Space: {self.space}
Floor Number: {self.floor_no}
Slot Number: {self.slot_no}
In Time: {self.in_time.strftime("%d/%m/%Y, %H:%M")}
Out Time: {self.out_time.strftime("%d/%m/%Y, %H:%M")}
"""

    def __str__(self) -> str:
        return f"""
ID: {self.id}
Vehicle: {self.vehicle}
Fare: {self.fare:.02f}
"""


class ParkingManager:
    def __init__(self) -> None:
        self.total_floors = 0
        self.total_slots = 0
        self.available_slots = 0
        self.total_revenue = 0.0
        self.floors: dict[int, Floor] = {}
        self.vehicles: dict[str, Vehicle] = {}
        self.parking_details: dict[str, ParkingDetail] = {}

    def get_info(self) -> str:
        return self.__str__()

    def add_slots(self, floors: int, slots: int) -> str:
        self.total_floors += floors

        for f_no in range(1, floors+1):
            if f_no not in self.floors:
                floor = Floor(f_no)
                floor.create_slots(slots)
                self.total_slots += floor.total_slots
                self.available_slots += floor.total_slots
                self.floors[f_no] = floor

        return f"Parking Lot created with {floors} floors and {slots} slots."

    def park_vehicle(self, vehicle_name: str, type: str, time: str) -> str:
        spaces = vehicle_rate_info[type]['spaces']
        if self.available_slots > 0 and vehicle_name not in self.vehicles:
            for f_no in range(1, self.total_floors+1):
                floor = self.floors[f_no]
                slot = floor.get_slot(spaces)

                if slot:
                    vehicle = Vehicle(vehicle_name, type, slot.space, time, slot.floor_no, slot.number)
                    floor.available_slots -= 1
                    floor.slot_details[slot.space]['available'] -= 1
                    floor.slot_details[slot.space]['queue'].pop(0)
                    slot.occupied = True
                    slot.vehicle = vehicle.name
                    slot.vehicle_type = vehicle.type
                    slot.in_time = vehicle.in_time
                    self.available_slots -= 1
                    self.vehicles[vehicle.name] = vehicle
                    return f"{type} {vehicle_name} parked in floor {slot.floor_no}, slot {slot.number}."

        return f"Can not find space for {type} {vehicle_name}."

    def unpark_vehicle(self, vehicle_name: str) -> str:
        if vehicle_name in self.vehicles:
            vehicle = self.vehicles[vehicle_name]
            in_time = vehicle.in_time
            out_time = datetime.now()

            total_minutes = (out_time - in_time).total_seconds() // 60
            total_hours = math.ceil(total_minutes / 60)
            fare_details = vehicle_rate_info[vehicle.type]
            if total_hours <= 2:
                fare = total_hours * fare_details['first_2hr']
            else:
                fare = (2 * fare_details['first_2hr']) + ((total_hours-2) * fare_details['after_2hr'])

            floor = self.floors[vehicle.floor_no]
            slot = floor.slot_details[vehicle.space]['slots'][vehicle.slot_no]
            slot.occupied = False
            slot.vehicle = None
            slot.vehicle_type = None
            slot.in_time = None

            floor.available_slots += 1
            floor.slot_details[vehicle.space]['available'] += 1
            floor.slot_details[vehicle.space]['queue'].append(vehicle.slot_no)
            floor.slot_details[vehicle.space]['queue'].sort()
            floor.available_slots += 1

            parking_detail = ParkingDetail(
                vehicle.name, vehicle.type, vehicle.space, vehicle.floor_no,
                vehicle.slot_no, vehicle.in_time, out_time, fare
            )

            self.available_slots += 1
            self.total_revenue += fare
            self.parking_details[parking_detail.id] = parking_detail
            self.vehicles.pop(vehicle.name)

            return f"Total fare for {vehicle.type} {vehicle.name} is {fare}."

        return f"Unable to find vehicle {vehicle_name}"

    def get_total_revenue(self) -> str:
        return f"Total Revenue: {self.total_revenue:.02f}"

    def get_available_slots(self) -> str:
        return f"Available Slots: {self.available_slots}/{self.total_slots}"

    def get_most_used_vehicle(self) -> str:
        total_vehicles = {}
        for detail in self.parking_details.values():
            if detail.vehicle_type not in total_vehicles:
                total_vehicles[detail.vehicle_type] = 0
            total_vehicles[detail.vehicle_type] += 1

        max_count = max_vehicle = 0
        for vehicle, count in total_vehicles.items():
            if count > max_count:
                max_count, max_vehicle = count, vehicle

        return f"Most used vehicle: {max_vehicle} ({max_count})"

    def __str__(self) -> str:
        return f"""
Total Floors: {self.total_floors}
Total Slots: {self.total_slots}
Available Slots: {self.available_slots}
Total Revenue: {self.total_revenue:.02f}
"""
