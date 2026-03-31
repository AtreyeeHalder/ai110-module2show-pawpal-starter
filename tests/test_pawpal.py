import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


# Task Completion
def test_mark_complete_changes_status():
    task = Task(description="Walk", time="08:00 AM", frequency="daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# Task Addition
def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", age=3, gender="Male", animal="Dog", breed="Labrador")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feed", time="07:00 AM", frequency="daily"))
    assert len(pet.tasks) == 1
