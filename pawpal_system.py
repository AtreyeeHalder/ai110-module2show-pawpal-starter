from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Optional


@dataclass
class Task:
    description: str
    time: str           # e.g. "08:00 AM"
    frequency: str      # e.g. "daily", "weekly", "monthly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reset(self) -> None:
        """Reset completion status (e.g. start of a new cycle)."""
        self.completed = False

    def __str__(self) -> str:
        status = "Done" if self.completed else "Pending"
        return f"[{status}] {self.description} at {self.time} ({self.frequency}) — due {self.due_date}"


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
        """Return the soonest upcoming appointment, or ``None`` if the list is empty.

        Uses ``min()`` with ``Appointment.date`` as the key, which performs a
        single linear scan (O(n)) over all stored appointments.  Date strings
        must follow a lexicographically sortable format (e.g. ``"YYYY-MM-DD"``)
        for the comparison to be chronologically correct.

        Returns:
            The ``Appointment`` object with the earliest ``date`` value, or
            ``None`` if no appointments have been added yet.
        """
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
        """Return all (pet, task) pairs sorted chronologically by scheduled time.

        Parses each task's time string with strptime (format ``%I:%M %p``) so
        that ``"08:00 AM"`` sorts before ``"01:00 PM"`` regardless of
        lexicographic order.

        Returns:
            A list of (Pet, Task) tuples ordered from earliest to latest
            scheduled time.  Ties in time are kept in insertion order
            (stable sort).

        Raises:
            ValueError: If any task's ``time`` field does not match the
                expected ``%I:%M %p`` format (e.g. ``"8:00 AM"`` instead of
                ``"08:00 AM"``).
        """
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda pair: datetime.strptime(pair[1].time, "%I:%M %p"))

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs filtered by pet name and/or completion status.

        Applies up to two independent filters in sequence:
        1. If ``pet_name`` is provided, discard pairs whose pet does not match.
        2. If ``completed`` is provided, discard pairs whose task completion
           flag does not match the requested value.

        Both filters are optional and can be combined freely.

        Args:
            pet_name:  Name of the pet to restrict results to.  Pass ``None``
                (default) to include tasks from all pets.
            completed: ``True`` to return only completed tasks, ``False`` to
                return only pending tasks, or ``None`` (default) to return
                tasks regardless of their completion status.

        Returns:
            A list of (Pet, Task) tuples that satisfy all supplied filters.
            Returns an empty list if no tasks match.
        """
        results = self.owner.get_all_tasks()
        if pet_name is not None:
            results = [(pet, task) for pet, task in results if pet.name == pet_name]
        if completed is not None:
            results = [(pet, task) for pet, task in results if task.completed == completed]
        return results

    def get_pending_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all incomplete (pet, task) pairs across every pet.

        Returns:
            A list of (Pet, Task) tuples where ``task.completed`` is ``False``.
            Returns an empty list if every task has been marked complete.
        """
        return [(pet, task) for pet, task in self.owner.get_all_tasks() if not task.completed]

    def get_completed_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all completed (pet, task) pairs across every pet.

        Returns:
            A list of (Pet, Task) tuples where ``task.completed`` is ``True``.
            Returns an empty list if no tasks have been marked complete yet.
        """
        return [(pet, task) for pet, task in self.owner.get_all_tasks() if task.completed]

    def mark_task_complete(self, pet_name: str, task_description: str) -> bool:
        """Mark the first matching incomplete task complete for the named pet.

        Searches the pet's task list for the first task whose description
        matches ``task_description`` and whose ``completed`` flag is ``False``.
        When found, calls ``task.mark_complete()`` and, for recurring
        frequencies, appends a new Task due at the next occurrence:

        - ``"daily"``  → next due date is today + 1 day (``timedelta(days=1)``)
        - ``"weekly"`` → next due date is today + 7 days (``timedelta(weeks=1)``)
        - ``"monthly"`` or any other frequency → no new task is created

        Args:
            pet_name:         Name of the pet whose task list to search.
            task_description: Exact description string of the task to complete.

        Returns:
            ``True`` if a matching pending task was found and marked complete.
            ``False`` if the pet does not exist or no matching pending task
            was found.
        """
        pet = self.owner.get_pet(pet_name)
        if not pet:
            return False
        for task in pet.tasks:
            if task.description == task_description and not task.completed:
                task.mark_complete()
                if task.frequency == "daily":
                    next_due = date.today() + timedelta(days=1)
                elif task.frequency == "weekly":
                    next_due = date.today() + timedelta(weeks=1)
                else:
                    next_due = None
                if next_due:
                    pet.add_task(Task(
                        description=task.description,
                        time=task.time,
                        frequency=task.frequency,
                        due_date=next_due,
                    ))
                return True
        return False

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for time slots shared by more than one task.

        Groups all tasks across every pet by their ``time`` field into a
        dictionary keyed on time string.  Any time slot that contains more
        than one (pet, task) pair is considered a conflict, and one warning
        string is generated per conflicting slot.

        This method is purely read-only: it never modifies any task or pet
        and never raises an exception.

        Returns:
            A list of human-readable warning strings, one per conflicting time
            slot, each identifying how many tasks overlap and listing the pet
            names and task descriptions involved.  Returns an empty list if no
            two tasks share the same scheduled time.

        Example return value::

            [
                "WARNING: 2 tasks overlap at 08:00 AM — Buddy: 'Morning Walk', Luna: 'Breakfast'"
            ]
        """
        # Group (pet, task) pairs by scheduled time
        time_groups: dict[str, list[tuple[Pet, Task]]] = {}
        for pet, task in self.owner.get_all_tasks():
            time_groups.setdefault(task.time, []).append((pet, task))

        warnings = []
        for time_slot, pairs in time_groups.items():
            if len(pairs) > 1:
                descriptions = ", ".join(
                    f"{pet.name}: '{task.description}'" for pet, task in pairs
                )
                warnings.append(
                    f"WARNING: {len(pairs)} tasks overlap at {time_slot} — {descriptions}"
                )
        return warnings

    def reset_all_tasks(self) -> None:
        """Reset completion status on every task (e.g. start of a new day/week)."""
        for _, task in self.owner.get_all_tasks():
            task.reset()

    def summary(self) -> str:
        """Build and return a formatted summary of all tasks grouped by pet.

        Iterates over every pet owned by the owner, printing each pet's name
        as a section header followed by its tasks using ``Task.__str__()``.
        Pets with no tasks are shown with an ``(no tasks)`` placeholder.

        Returns:
            A multi-line string starting with a header line that includes the
            owner's name, followed by one section per pet.  The string is
            suitable for printing directly to the console.
        """
        lines = [f"=== Schedule for {self.owner.name}'s pets ==="]
        for pet in self.owner.pets:
            lines.append(f"\n{pet.name}:")
            if not pet.tasks:
                lines.append("  (no tasks)")
            for task in pet.tasks:
                lines.append(f"  {task}")
        return "\n".join(lines)
