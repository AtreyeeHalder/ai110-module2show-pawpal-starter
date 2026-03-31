from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    description: str
    time: str           # e.g. "08:00 AM"
    frequency: str      # e.g. "daily", "weekly", "monthly"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reset(self) -> None:
        """Reset completion status (e.g. start of a new cycle)."""
        self.completed = False

    def __str__(self) -> str:
        status = "Done" if self.completed else "Pending"
        return f"[{status}] {self.description} at {self.time} ({self.frequency})"


@dataclass
class Pet:
    name: str
    age: int
    gender: str
    animal: str
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a formatted string with all pet details."""
        return (
            f"Name: {self.name} | Animal: {self.animal} | Breed: {self.breed} | "
            f"Age: {self.age} | Gender: {self.gender}"
        )

    def eat(self, time: str) -> None:
        """Record that the pet was fed at the given time."""
        print(f"{self.name} was fed at {time}.")

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> list[Task]:
        """Return all incomplete tasks for this pet."""
        return [t for t in self.tasks if not t.completed]

    def get_completed_tasks(self) -> list[Task]:
        """Return all completed tasks for this pet."""
        return [t for t in self.tasks if t.completed]


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
        if time not in self.feeding_times:
            self.feeding_times.append(time)

    def remove_feeding_time(self, time: str) -> None:
        """Remove a feeding time from the schedule."""
        if time in self.feeding_times:
            self.feeding_times.remove(time)

    def get_schedule(self) -> list[str]:
        """Return the list of scheduled feeding times."""
        return list(self.feeding_times)

    def mark_fed(self, time: str) -> None:
        """Mark the pet as fed at the given time."""
        self.pet.eat(time)


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
        return list(self.appointments)

    def remove_appointment(self, appointment_id: int) -> None:
        """Remove the appointment with the given id."""
        self.appointments = [a for a in self.appointments if a.id != appointment_id]

    def get_next_appointment(self) -> Optional[Appointment]:
        """Return the next upcoming appointment (earliest date), or None if there are none."""
        if not self.appointments:
            return None
        return min(self.appointments, key=lambda a: a.date)


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs across every pet this owner has."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The 'Brain' — retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner):
        self.owner: Owner = owner

    def get_tasks_for_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks for a specific pet by name."""
        pet = self.owner.get_pet(pet_name)
        return pet.tasks if pet else []

    def get_all_tasks_sorted_by_time(self) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs sorted by scheduled time."""
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda pair: pair[1].time)

    def get_pending_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all incomplete (pet, task) pairs across every pet."""
        return [(pet, task) for pet, task in self.owner.get_all_tasks() if not task.completed]

    def get_completed_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all completed (pet, task) pairs across every pet."""
        return [(pet, task) for pet, task in self.owner.get_all_tasks() if task.completed]

    def mark_task_complete(self, pet_name: str, task_description: str) -> bool:
        """Mark the first matching task complete for the named pet; returns True if found, False otherwise."""
        tasks = self.get_tasks_for_pet(pet_name)
        for task in tasks:
            if task.description == task_description:
                task.mark_complete()
                return True
        return False

    def reset_all_tasks(self) -> None:
        """Reset completion status on every task (e.g. start of a new day/week)."""
        for _, task in self.owner.get_all_tasks():
            task.reset()

    def summary(self) -> str:
        """Print a formatted summary of all tasks grouped by pet."""
        lines = [f"=== Schedule for {self.owner.name}'s pets ==="]
        for pet in self.owner.pets:
            lines.append(f"\n{pet.name}:")
            if not pet.tasks:
                lines.append("  (no tasks)")
            for task in pet.tasks:
                lines.append(f"  {task}")
        return "\n".join(lines)
