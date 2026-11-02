from models import ParkingManager

manager = ParkingManager()


def add_slots() -> str:
    floors = input("Enter number or floors: ")
    slots = input("Enter number of slots: ")
    if not floors.isdigit() and not slots.isdigit():
        return "Floors and slots must be only in numbers"
    response = manager.add_slots(int(floors), int(slots))
    return response


def park_vehicle() -> str:
    vehicle_type = input("Enter type of vehicle (car/bike/truck): ")
    name = input("Enter vehicle name: ")
    time = input("Enter the In Time (HH:MM): ")
    try:
        response = manager.park_vehicle(name, vehicle_type, time)
    except TypeError as e:
        return str(e)
    return response


def unpark_vehicle() -> str:
    name = input("Enter vehicle name: ")
    response = manager.unpark_vehicle(name)
    return response


def get_available_slots() -> str:
    return manager.get_available_slots()


def get_most_used_vehicle() -> str:
    return manager.get_most_used_vehicle()


def get_total_revenue() -> str:
    return manager.get_total_revenue()


operations = {
    "1": add_slots,
    "2": park_vehicle,
    "3": unpark_vehicle,
    "4": get_available_slots,
    "5": get_most_used_vehicle,
    "6": get_total_revenue,
}

prompt = """
Parking Management System

[1] Add Parking Lot
[2] Park Vehicle
[3] Unpark Vehicle
[4] Get Available Slots
[5] Get Most Used Vehicle
[6] Get Total Revenue

Enter "/bye" to exit.
Enter your option:
"""

command = input(prompt)
while command != "/bye":
    operation = operations.get(command, None)
    if operation:
        print(operation())
    else:
        print("Enter a valid input\n")
    command = input(prompt)
