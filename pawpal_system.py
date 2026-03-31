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
    id: int
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

    def _next_id(self) -> int:
        """Return the next available ID, reusing gaps left by removals."""
        if not self.appointments:
            return 1
        return max(a.id for a in self.appointments) + 1

    def add_appointment(
        self, date: str, address: str, vet_name: str, reason: str
    ) -> Appointment:
        """Create and store a new Appointment with an auto-assigned id."""
        appointment = Appointment(
            id=self._next_id(),
            date=date,
            address=address,
            vet_name=vet_name,
            reason=reason,
        )
        self.appointments.append(appointment)
        return appointment

    def view_appointments(self) -> list[Appointment]:
        """Return all appointments for this pet."""
        pass

    def remove_appointment(self, appointment_id: int) -> None:
        """Remove the appointment with the given id."""
        pass

    def get_next_appointment(self) -> Optional[Appointment]:
        """Return the next upcoming appointment, or None if there are none."""
        pass
