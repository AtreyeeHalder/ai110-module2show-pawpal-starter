import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")
st.caption("A smart pet care scheduling assistant")

# ── Session state ─────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Owner & Pet Setup ─────────────────────────────────────────────
st.subheader("Owner & Pet Setup")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")

col3, col4, col5, col6 = st.columns(4)
with col3:
    pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
with col4:
    pet_gender = st.selectbox("Gender", ["Male", "Female"])
with col5:
    pet_animal = st.selectbox("Animal", ["dog", "cat", "rabbit", "bird", "other"])
with col6:
    pet_breed = st.text_input("Breed", value="Shih Tzu")

if st.button("Create Owner & Pet", type="primary"):
    owner = Owner(name=owner_name)
    pet = Pet(
        name=pet_name,
        age=pet_age,
        gender=pet_gender,
        animal=pet_animal,
        breed=pet_breed,
    )
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(
        f"Created owner **{owner_name}** with pet **{pet_name}** "
        f"({pet_animal}, {pet_breed}, age {pet_age})."
    )

if st.session_state.owner:
    o = st.session_state.owner
    pets_info = " | ".join(p.get_info() for p in o.pets)
    st.info(f"**Owner:** {o.name}  —  {pets_info}")

st.divider()

# ── Add Tasks ─────────────────────────────────────────────────────
st.subheader("Add Tasks")

col_a, col_b, col_c = st.columns(3)
with col_a:
    task_title = st.text_input("Task description", value="Morning walk")
with col_b:
    task_time = st.time_input("Scheduled time", value=datetime.time(8, 0))
with col_c:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])

if st.button("Add Task"):
    if not st.session_state.owner or not st.session_state.owner.pets:
        st.warning("Create an owner and pet first.")
    else:
        time_str = task_time.strftime("%I:%M %p")  # e.g. "08:00 AM"
        task = Task(description=task_title, time=time_str, frequency=frequency)
        pet = st.session_state.owner.pets[-1]
        pet.add_task(task)
        st.success(
            f"Added **{task_title}** at {time_str} ({frequency}) to **{pet.name}**."
        )

st.divider()

# ── Schedule View ─────────────────────────────────────────────────
st.subheader("Schedule")

if not st.session_state.owner:
    st.info("Set up an owner and pet above to view the schedule.")
else:
    scheduler = Scheduler(st.session_state.owner)

    # Conflict detection banner
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    elif scheduler.owner.get_all_tasks():
        st.success("No scheduling conflicts detected.")

    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        show_filter = st.selectbox(
            "Show tasks", ["All", "Pending only", "Completed only"]
        )
    with col_f2:
        pet_names = ["All pets"] + [p.name for p in st.session_state.owner.pets]
        pet_filter = st.selectbox("Filter by pet", pet_names)

    pet_name_filter = None if pet_filter == "All pets" else pet_filter
    completed_filter = (
        None
        if show_filter == "All"
        else show_filter == "Completed only"
    )

    filtered = scheduler.filter_tasks(
        pet_name=pet_name_filter, completed=completed_filter
    )

    # Sort filtered results chronologically using the Scheduler's sort logic
    try:
        sorted_tasks = sorted(
            filtered,
            key=lambda pair: datetime.datetime.strptime(pair[1].time, "%I:%M %p"),
        )
    except ValueError:
        sorted_tasks = filtered  # fall back to original order on bad time format

    if sorted_tasks:
        rows = [
            {
                "Pet": pet.name,
                "Task": task.description,
                "Time": task.time,
                "Frequency": task.frequency,
                "Due Date": str(task.due_date),
                "Status": "Done" if task.completed else "Pending",
            }
            for pet, task in sorted_tasks
        ]
        st.table(rows)

        pending_count = sum(1 for _, t in sorted_tasks if not t.completed)
        done_count = sum(1 for _, t in sorted_tasks if t.completed)
        m1, m2 = st.columns(2)
        m1.metric("Pending tasks", pending_count)
        m2.metric("Completed tasks", done_count)
    else:
        st.info("No tasks match the current filters.")

    st.divider()

    # ── Mark Task Complete ─────────────────────────────────────────
    st.subheader("Mark Task Complete")

    pending_pairs = scheduler.get_pending_tasks()
    if pending_pairs:
        task_options = [
            f"{pet.name} — {task.description} @ {task.time}"
            for pet, task in pending_pairs
        ]
        selected = st.selectbox("Select a pending task", task_options)
        if st.button("Mark Complete", type="primary"):
            idx = task_options.index(selected)
            sel_pet, sel_task = pending_pairs[idx]
            success = scheduler.mark_task_complete(sel_pet.name, sel_task.description)
            if success:
                st.success(
                    f"Marked **{sel_task.description}** complete for **{sel_pet.name}**."
                )
                if sel_task.frequency in ("daily", "weekly"):
                    st.info(
                        f"A new **{sel_task.frequency}** occurrence has been scheduled automatically."
                    )
            else:
                st.error("Could not mark task complete — task not found.")
    else:
        st.success("All tasks are complete! Nothing left to do.")

    st.divider()

    # ── Reset ──────────────────────────────────────────────────────
    if st.button("Reset All Tasks to Pending"):
        scheduler.reset_all_tasks()
        st.success("All tasks have been reset to pending.")
