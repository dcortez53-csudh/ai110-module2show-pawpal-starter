import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant. Add pets, schedule
tasks, and generate a daily plan that sorts by time and warns about conflicts.
"""
)

# --- Session state: the Owner survives reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

# --- Owner ---
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"], key="species_input")
with col3:
    breed = st.text_input("Breed (optional)", value="", key="breed_input")

if st.button("Add pet"):
    if owner.find_pet(pet_name):
        st.warning(f"A pet named {pet_name} already exists.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species, breed=breed))
        st.success(f"Added {pet_name} the {species}.")

if owner.pets:
    st.write("Current pets:")
    st.table([
        {"name": p.name, "species": p.species, "breed": p.breed, "task_count": p.task_count()}
        for p in owner.pets
    ])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")
if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    pet_options = [p.name for p in owner.pets]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        target_pet = st.selectbox("For pet", pet_options, key="task_pet")
    with col2:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    with col3:
        time_str = st.text_input("Time (HH:MM)", value="08:00", key="task_time")
    with col4:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20, key="task_duration")

    col5, col6 = st.columns(2)
    with col5:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
    with col6:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], key="task_freq")

    if st.button("Add task"):
        pet = owner.find_pet(target_pet)
        if pet:
            pet.add_task(Task(
                description=task_title,
                time=time_str,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
            ))
            st.success(f"Added '{task_title}' to {target_pet}.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([t.to_dict() for t in all_tasks])
    else:
        st.info("No tasks yet.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()

    if not schedule:
        st.info("No tasks to schedule yet.")
    else:
        st.success(f"Today's schedule for {owner.name}")
        st.table([
            {
                "time": t.time,
                "pet": t.pet_name,
                "task": t.description,
                "duration (min)": t.duration_minutes,
                "priority": t.priority,
            }
            for t in schedule
        ])

        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            st.warning("Conflicts detected:")
            for warning in conflicts:
                st.write(f"- {warning}")
        else:
            st.info("No conflicts detected.")
