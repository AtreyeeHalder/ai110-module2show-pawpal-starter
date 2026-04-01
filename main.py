from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner("Alex")

# Create pets
buddy = Pet(name="Buddy", age=3, gender="Male", animal="Dog", breed="Golden Retriever")
luna = Pet(name="Luna", age=5, gender="Female", animal="Cat", breed="Siamese")

owner.add_pet(buddy)
owner.add_pet(luna)

# Add tasks OUT OF ORDER to verify sorting works
buddy.add_task(Task(description="Flea medication", time="12:00 PM", frequency="monthly"))
buddy.add_task(Task(description="Evening walk",    time="05:00 PM", frequency="daily"))
buddy.add_task(Task(description="Morning walk",    time="07:00 AM", frequency="daily"))

luna.add_task(Task(description="Evening feeding",  time="06:00 PM", frequency="daily"))
luna.add_task(Task(description="Brush fur",        time="09:30 AM", frequency="weekly"))
luna.add_task(Task(description="Afternoon nap",    time="02:00 PM", frequency="daily"))
luna.add_task(Task(description="Morning feeding",  time="07:00 AM", frequency="daily"))  # conflicts with Buddy's Morning walk

# Mark tasks complete
buddy.tasks[0].mark_complete()   # Flea medication
luna.tasks[2].mark_complete()    # Afternoon nap

scheduler = Scheduler(owner)

# --- All tasks sorted by time ---
print("=" * 45)
print("       ALL TASKS (sorted by time)")
print("=" * 45)
for pet, task in scheduler.get_all_tasks_sorted_by_time():
    status = "✓" if task.completed else "○"
    print(f"  {task.time}  [{status}] {pet.name}: {task.description}")

# --- Filter: Buddy's tasks only ---
print("\n" + "=" * 45)
print("       BUDDY'S TASKS")
print("=" * 45)
for pet, task in scheduler.filter_tasks(pet_name="Buddy"):
    status = "✓" if task.completed else "○"
    print(f"  {task.time}  [{status}] {task.description}")

# --- Filter: pending tasks only ---
print("\n" + "=" * 45)
print("       PENDING TASKS (all pets)")
print("=" * 45)
for pet, task in scheduler.filter_tasks(completed=False):
    status = "○"
    print(f"  {task.time}  [{status}] {pet.name}: {task.description}")

# --- Filter: completed tasks only ---
print("\n" + "=" * 45)
print("       COMPLETED TASKS (all pets)")
print("=" * 45)
for pet, task in scheduler.filter_tasks(completed=True):
    status = "✓"
    print(f"  {task.time}  [{status}] {pet.name}: {task.description}")

# --- Filter: Luna's pending tasks ---
print("\n" + "=" * 45)
print("       LUNA'S PENDING TASKS")
print("=" * 45)
for pet, task in scheduler.filter_tasks(pet_name="Luna", completed=False):
    print(f"  {task.time}  [○] {task.description}")

print("=" * 45)

# --- Conflict detection ---
print("\n" + "=" * 45)
print("       SCHEDULE CONFLICTS")
print("=" * 45)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts detected.")
print("=" * 45)
