from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner("Alex")

# Create pets
buddy = Pet(name="Buddy", age=3, gender="Male", animal="Dog", breed="Golden Retriever")
luna = Pet(name="Luna", age=5, gender="Female", animal="Cat", breed="Siamese")

owner.add_pet(buddy)
owner.add_pet(luna)

# Add tasks to Buddy
buddy.add_task(Task(description="Morning walk", time="07:00 AM", frequency="daily"))
buddy.add_task(Task(description="Flea medication", time="12:00 PM", frequency="monthly"))

# Add tasks to Luna
luna.add_task(Task(description="Brush fur", time="09:30 AM", frequency="weekly"))
luna.add_task(Task(description="Evening feeding", time="06:00 PM", frequency="daily"))

# Use Scheduler to print Today's Schedule
scheduler = Scheduler(owner)

print("=" * 40)
print("         TODAY'S SCHEDULE")
print("=" * 40)

for pet, task in scheduler.get_all_tasks_sorted_by_time():
    status = "✓" if task.completed else "○"
    print(f"{task.time}  [{status}] {pet.name}: {task.description} ({task.frequency})")

print("=" * 40)
