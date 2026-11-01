from datetime import datetime
from uuid import uuid4

VEHICLE_SPACES = ["two_wheeler", "compact", "large"]

vehicle_rate_info = {
    "bike": {
        "type": VEHICLE_SPACES[0:1],
        "first_2hr": 30,
        "after_2hr": 50,
    },
    "car": {
        "type": VEHICLE_SPACES[1:],
        "first_2hr": 50,
        "after_2hr": 75,
    },
    "truck": {
        "type": VEHICLE_SPACES[-1:],
        "first_2hr": 75,
        "after_2hr": 100,
    },
}


class Vehicle:
    def __init__(self, name: str, type: str, space: str, time: str, floor: int, slot: int) -> None:
        self.name = name.replace(" ", '').upper()
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
            "count": 0,
            "queue": [],             # using list for now but need to implement a better efficient alternative
            "slots": {}
        } for i in VEHICLE_SPACES}
        self.total_slots = 0
        self.available_slots = 0

    def get_info(self) -> str:
        return self.__str__()

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
        self.floors = {}
        self.vehicles = {}
        self.parking_details = {}

    def get_info(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"""
Total Floors: {self.total_floors}
Total Slots: {self.total_slots}
Available Slots: {self.available_slots}
Total Revenue: {self.total_revenue:.02f}
"""
