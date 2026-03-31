from dataclasses import dataclass
from typing import Optional


@dataclass
class Pet:
    name: str
    age: int
    gender: str
    animal: str
    breed: str

    def get_info(self) -> str:
        """Return a formatted string with all pet details."""
        pass

    def eat(self, time: str) -> None:
        """Record that the pet was fed at the given time."""
        pass


@dataclass
class Appointment:
    date: str
    address: str
    vet_name: str
    reason: str


class FoodSchedule:
    def __init__(self, pet: Pet):
        self.pet: Pet = pet
        self.feeding_times: list[str] = []

    def add_feeding_time(self, time: str) -> None:
        """Add a feeding time to the schedule."""
        pass

    def remove_feeding_time(self, time: str) -> None:
        """Remove a feeding time from the schedule."""
        pass

    def get_schedule(self) -> list[str]:
        """Return the list of scheduled feeding times."""
        pass

    def mark_fed(self, time: str) -> None:
        """Mark the pet as fed at the given time."""
        pass


class VetAppointments:
    def __init__(self, pet: Pet):
        self.pet: Pet = pet
        self.appointments: list[Appointment] = []

    def add_appointment(
        self, date: str, address: str, vet_name: str, reason: str
    ) -> None:
        """Create and store a new Appointment."""
        pass

    def view_appointments(self) -> list[Appointment]:
        """Return all appointments for this pet."""
        pass

    def remove_appointment(
        self, date: str, address: str, vet_name: str, reason: str
    ) -> None:
        """Remove a matching appointment from the list."""
        pass

    def get_next_appointment(self) -> Optional[Appointment]:
        """Return the next upcoming appointment, or None if there are none."""
        pass
