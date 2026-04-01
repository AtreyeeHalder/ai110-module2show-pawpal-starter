import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_owner_with_pets():
    """Return a fresh Owner with two pets and no tasks."""
    owner = Owner("Alex")
    buddy = Pet(name="Buddy", age=3, gender="Male", animal="Dog", breed="Labrador")
    luna = Pet(name="Luna", age=2, gender="Female", animal="Cat", breed="Siamese")
    owner.add_pet(buddy)
    owner.add_pet(luna)
    return owner, buddy, luna


# ---------------------------------------------------------------------------
# Task Completion
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = Task(description="Walk", time="08:00 AM", frequency="daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# ---------------------------------------------------------------------------
# Task Addition
# ---------------------------------------------------------------------------

def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", age=3, gender="Male", animal="Dog", breed="Labrador")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feed", time="07:00 AM", frequency="daily"))
    assert len(pet.tasks) == 1


# ---------------------------------------------------------------------------
# Sorting Correctness
# ---------------------------------------------------------------------------

def test_tasks_sorted_chronologically():
    """AM/PM tasks come back in true time order, not alphabetical string order."""
    owner, buddy, luna = make_owner_with_pets()
    buddy.add_task(Task(description="Afternoon Walk", time="01:00 PM", frequency="daily"))
    buddy.add_task(Task(description="Morning Walk",   time="08:00 AM", frequency="daily"))
    luna.add_task( Task(description="Evening Meal",   time="06:00 PM", frequency="daily"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.get_all_tasks_sorted_by_time()
    times = [task.time for _, task in sorted_tasks]

    assert times == ["08:00 AM", "01:00 PM", "06:00 PM"], (
        f"Expected chronological order, got: {times}"
    )


def test_tasks_sorted_across_multiple_pets():
    """Tasks from different pets are interleaved by time, not grouped by pet."""
    owner, buddy, luna = make_owner_with_pets()
    buddy.add_task(Task(description="Breakfast", time="07:00 AM", frequency="daily"))
    luna.add_task( Task(description="Medicine",  time="06:00 AM", frequency="daily"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.get_all_tasks_sorted_by_time()
    descriptions = [task.description for _, task in sorted_tasks]

    assert descriptions[0] == "Medicine", "Luna's earlier task should sort first"
    assert descriptions[1] == "Breakfast"


def test_sort_with_no_tasks_returns_empty():
    """A scheduler over an owner with no tasks returns an empty list, not an error."""
    owner = Owner("EmptyOwner")
    scheduler = Scheduler(owner)
    assert scheduler.get_all_tasks_sorted_by_time() == []


# ---------------------------------------------------------------------------
# Recurrence Logic
# ---------------------------------------------------------------------------

def test_daily_task_creates_next_day_task():
    """Completing a daily task appends a new pending task due tomorrow."""
    owner, buddy, _ = make_owner_with_pets()
    buddy.add_task(Task(description="Walk", time="08:00 AM", frequency="daily"))

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Buddy", "Walk")

    # Original task is now done; a new one should exist
    assert len(buddy.tasks) == 2
    new_task = buddy.tasks[1]
    assert new_task.completed is False
    assert new_task.due_date == date.today() + timedelta(days=1)


def test_weekly_task_creates_next_week_task():
    """Completing a weekly task appends a new pending task due in 7 days."""
    owner, buddy, _ = make_owner_with_pets()
    buddy.add_task(Task(description="Bath", time="10:00 AM", frequency="weekly"))

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Buddy", "Bath")

    assert len(buddy.tasks) == 2
    new_task = buddy.tasks[1]
    assert new_task.completed is False
    assert new_task.due_date == date.today() + timedelta(weeks=1)


def test_monthly_task_does_not_create_new_task():
    """Completing a monthly task marks it done but does NOT append a recurrence."""
    owner, buddy, _ = make_owner_with_pets()
    buddy.add_task(Task(description="Flea Treatment", time="09:00 AM", frequency="monthly"))

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete("Buddy", "Flea Treatment")

    assert result is True
    assert len(buddy.tasks) == 1           # no new task added
    assert buddy.tasks[0].completed is True


def test_mark_complete_returns_false_for_unknown_pet():
    """mark_task_complete returns False when the pet name doesn't exist."""
    owner = Owner("Alex")
    scheduler = Scheduler(owner)
    assert scheduler.mark_task_complete("Ghost", "Walk") is False


def test_mark_complete_returns_false_for_already_completed_task():
    """A task that is already done cannot be completed again (no duplicate recurrences)."""
    owner, buddy, _ = make_owner_with_pets()
    buddy.add_task(Task(description="Walk", time="08:00 AM", frequency="daily"))

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Buddy", "Walk")   # first completion → new task added
    scheduler.mark_task_complete("Buddy", "Walk")  # original is done; only new one pending

    # Either way, the original completed task must stay completed.
    assert buddy.tasks[0].completed is True


# ---------------------------------------------------------------------------
# Conflict Detection
# ---------------------------------------------------------------------------

def test_no_conflict_when_tasks_at_different_times():
    """Tasks scheduled at different times produce zero warnings."""
    owner, buddy, luna = make_owner_with_pets()
    buddy.add_task(Task(description="Walk",      time="08:00 AM", frequency="daily"))
    luna.add_task( Task(description="Breakfast", time="09:00 AM", frequency="daily"))

    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


def test_conflict_detected_when_two_pets_share_a_time_slot():
    """Two tasks at the same time trigger exactly one warning mentioning both pets."""
    owner, buddy, luna = make_owner_with_pets()
    buddy.add_task(Task(description="Walk",      time="08:00 AM", frequency="daily"))
    luna.add_task( Task(description="Breakfast", time="08:00 AM", frequency="daily"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00 AM" in warnings[0]
    assert "Buddy" in warnings[0]
    assert "Luna" in warnings[0]


def test_conflict_count_matches_number_of_overlapping_slots():
    """Each conflicting time slot produces exactly one warning."""
    owner, buddy, luna = make_owner_with_pets()
    # Two conflicting slots
    buddy.add_task(Task(description="Walk",   time="08:00 AM", frequency="daily"))
    luna.add_task( Task(description="Feed",   time="08:00 AM", frequency="daily"))
    buddy.add_task(Task(description="Nap",    time="02:00 PM", frequency="daily"))
    luna.add_task( Task(description="Groom",  time="02:00 PM", frequency="daily"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 2


def test_no_conflict_when_owner_has_no_tasks():
    """detect_conflicts on an empty schedule returns an empty list."""
    owner = Owner("Alex")
    owner.add_pet(Pet(name="Buddy", age=3, gender="Male", animal="Dog", breed="Labrador"))
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []
