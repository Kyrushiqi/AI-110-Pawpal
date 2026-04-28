import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler, TaskType, Frequency

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

PRIORITY_LABELS = ["High", "Medium", "Low"]

# Session vault — persists across every Streamlit rerun for this browser tab.
if "owner" not in st.session_state:
    st.session_state.owner = None
if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1
if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

# ── Step 1: Create / Edit Owner ───────────────────────────────────────────────
st.subheader("Step 1: Owner")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    walk_options = ["morning", "afternoon", "evening"]
    preferred_walk = st.selectbox("Preferred walk time", walk_options)

if st.button("Create Owner"):
    st.session_state.owner = Owner(
        ownerID=1,
        ownerName=owner_name,
        preferred_walk_time=preferred_walk,
    )
    st.session_state.next_pet_id = 1
    st.session_state.next_task_id = 1
    st.success(f"Owner '{owner_name}' created.")

# Edit Owner — only shown once an owner exists
if st.session_state.owner:
    o = st.session_state.owner
    pet_names = [p.petName for p in o.pets] or ["none yet"]
    st.caption(
        f"Active owner: **{o.ownerName}** | Walk preference: {o.preferred_walk_time} "
        f"| Pets: {pet_names}"
    )

    with st.expander("Edit Owner"):
        edit_owner_name = st.text_input("New owner name", value=o.ownerName, key="edit_owner_name")
        edit_walk = st.selectbox(
            "New preferred walk time",
            walk_options,
            index=walk_options.index(o.preferred_walk_time),
            key="edit_walk",
        )
        if st.button("Update Owner"):
            o.ownerName = edit_owner_name
            o.preferred_walk_time = edit_walk
            st.success("Owner updated!")
            st.rerun()

st.divider()

# ── Step 2: Add / Edit / Delete Pets ─────────────────────────────────────────
st.subheader("Step 2: Pets")

if st.session_state.owner is None:
    st.warning("Create an owner first (Step 1).")
else:
    owner = st.session_state.owner
    species_options = ["dog", "cat", "bird", "other"]

    # Add a new pet
    col3, col4 = st.columns(2)
    with col3:
        pet_name = st.text_input("Pet name", value="Mochi", key="new_pet_name")
    with col4:
        species = st.selectbox("Species", species_options, key="new_pet_species")

    if st.button("Add Pet"):
        existing_names = [p.petName for p in owner.pets]
        if pet_name in existing_names:
            st.error(f"'{pet_name}' is already added. Use a different name.")
        else:
            owner.addPet(Pet(
                petID=st.session_state.next_pet_id,
                species=species,
                petName=pet_name,
                ownerID=owner.ownerID,
            ))
            st.session_state.next_pet_id += 1
            st.success(f"Pet '{pet_name}' ({species}) added!")
            st.rerun()

    # Edit / Delete existing pets
    if owner.pets:
        st.markdown("**Pets registered:**")
        st.table([
            {"Pet ID": p.petID, "Name": p.petName, "Species": p.species}
            for p in owner.pets
        ])

        pet_name_map = {p.petName: p for p in owner.pets}
        selected_pet_name = st.selectbox(
            "Select a pet to edit or delete", list(pet_name_map.keys()), key="manage_pet"
        )
        selected_pet = pet_name_map[selected_pet_name]

        col_edit, col_del = st.columns(2)

        with col_edit:
            with st.expander(f"Edit '{selected_pet_name}'"):
                new_pet_name = st.text_input(
                    "New pet name", value=selected_pet.petName, key="edit_pet_name"
                )
                new_species = st.selectbox(
                    "New species",
                    species_options,
                    index=species_options.index(selected_pet.species),
                    key="edit_pet_species",
                )
                if st.button("Update Pet"):
                    other_names = [p.petName for p in owner.pets if p.petID != selected_pet.petID]
                    if new_pet_name in other_names:
                        st.error(f"Another pet named '{new_pet_name}' already exists.")
                    else:
                        selected_pet.petName = new_pet_name
                        selected_pet.species = new_species
                        st.success("Pet updated!")
                        st.rerun()

        with col_del:
            st.markdown("")  # vertical spacer to align button
            st.markdown("")
            if st.button(f"Delete '{selected_pet_name}'", type="primary"):
                owner.removePet(selected_pet.petID)   # Owner.removePet() from pawpal_system.py
                st.success(f"Pet '{selected_pet_name}' and all its tasks removed.")
                st.rerun()

st.divider()

# ── Step 3: Add / Edit / Delete Tasks ────────────────────────────────────────
st.subheader("Step 3: Care Tasks")

if not st.session_state.owner or not st.session_state.owner.pets:
    st.warning("Add at least one pet first (Step 2).")
else:
    owner = st.session_state.owner
    pet_options = {p.petName: p.petID for p in owner.pets}
    task_type_values = [t.value for t in TaskType]
    freq_values = [f.value for f in Frequency]

    # Add a new task
    selected_pet_name = st.selectbox("Assign task to", list(pet_options.keys()), key="new_task_pet")

    col_a, col_b = st.columns(2)
    with col_a:
        task_type = st.selectbox("Task type", task_type_values, key="new_task_type")
        description = st.text_input("Description", value="Morning walk around the block", key="new_task_desc")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="new_task_dur")
    with col_b:
        frequency = st.selectbox("Frequency", freq_values, key="new_task_freq")
        priority_label = st.selectbox("Priority", PRIORITY_LABELS, key="new_task_pri")

    if st.button("Add Task"):
        pet_id = pet_options[selected_pet_name]
        pet = owner.getPet(pet_id)
        new_task = Task(
            taskID=st.session_state.next_task_id,
            taskType=TaskType(task_type),
            description=description,
            duration=float(duration),
            frequency=Frequency(frequency),
            priority=priority_label,
            petID=pet_id,
        )
        pet.addTask(new_task)               # Pet.addTask() from pawpal_system.py
        st.session_state.next_task_id += 1
        st.success(f"Added '{task_type}' task to {selected_pet_name}!")
        st.rerun()

    # Show all tasks across all pets
    all_tasks = owner.getAllTasks()
    if all_tasks:
        st.markdown("**All tasks (across all pets):**")
        st.table([
            {
                "Pet": owner.getPet(t.petID).petName,
                "Type": t.taskType.value,
                "Description": t.description,
                "Duration (min)": t.duration,
                "Frequency": t.frequency.value,
                "Priority": t.priority,
                "Done": t.is_completed,
            }
            for t in all_tasks
        ])

        # Edit / Delete existing tasks
        task_label_map = {
            f"[{owner.getPet(t.petID).petName}] {t.priority} — {t.taskType.value}: {t.description}": t
            for t in all_tasks
        }
        chosen_label = st.selectbox(
            "Select a task to edit or delete", list(task_label_map.keys()), key="manage_task"
        )
        chosen_task = task_label_map[chosen_label]
        chosen_pet = owner.getPet(chosen_task.petID)

        col_tedit, col_tdel = st.columns(2)

        with col_tedit:
            with st.expander(f"Edit selected task"):
                edit_pet_name = st.selectbox(
                    "Reassign to pet",
                    list(pet_options.keys()),
                    index=list(pet_options.keys()).index(chosen_pet.petName),
                    key="edit_task_pet",
                )
                edit_type = st.selectbox(
                    "Task type",
                    task_type_values,
                    index=task_type_values.index(chosen_task.taskType.value),
                    key="edit_task_type",
                )
                edit_desc = st.text_input(
                    "Description", value=chosen_task.description, key="edit_task_desc"
                )
                edit_dur = st.number_input(
                    "Duration (minutes)",
                    min_value=1,
                    max_value=240,
                    value=int(chosen_task.duration),
                    key="edit_task_dur",
                )
                edit_freq = st.selectbox(
                    "Frequency",
                    freq_values,
                    index=freq_values.index(chosen_task.frequency.value),
                    key="edit_task_freq",
                )
                edit_pri_label = st.selectbox(
                    "Priority",
                    PRIORITY_LABELS,
                    index=PRIORITY_LABELS.index(chosen_task.priority),
                    key="edit_task_pri",
                )

                if st.button("Update Task"):
                    new_pet_id = pet_options[edit_pet_name]
                    new_pet = owner.getPet(new_pet_id)

                    # Move task to new pet if reassigned
                    if new_pet_id != chosen_task.petID:
                        chosen_pet.removeTask(chosen_task.taskID)   # Pet.removeTask()
                        chosen_task.petID = new_pet_id
                        new_pet.tasks.append(chosen_task)

                    # Update task fields in-place (dataclass attributes are mutable)
                    chosen_task.taskType = TaskType(edit_type)
                    chosen_task.description = edit_desc
                    chosen_task.duration = float(edit_dur)
                    chosen_task.frequency = Frequency(edit_freq)
                    chosen_task.priority = edit_pri_label
                    st.success("Task updated!")
                    st.rerun()

        with col_tdel:
            st.markdown("")  # vertical spacer
            st.markdown("")
            if st.button("Delete selected task", type="primary"):
                chosen_pet.removeTask(chosen_task.taskID)   # Pet.removeTask() from pawpal_system.py
                st.success("Task deleted.")
                st.rerun()

    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ── Step 4: Generate Schedule ─────────────────────────────────────────────────
st.subheader("Step 4: Generate Schedule")

if not st.session_state.owner or not st.session_state.owner.pets:
    st.warning("Add an owner and at least one pet first.")
else:
    owner = st.session_state.owner
    available_minutes = st.number_input(
        "Available time today (minutes)", min_value=10, max_value=480, value=60
    )

    if st.button("Generate schedule"):
        scheduler = Scheduler(owner)
        schedule = scheduler.generateSchedule(float(available_minutes))

        if not schedule:
            st.warning(
                "No tasks fit within the available time "
                "(or all tasks are completed / their type is in your avoid list)."
            )
        else:
            total = sum(t.duration for t in schedule)
            st.success(
                f"Scheduled {len(schedule)} task(s) across "
                f"{len({t.petID for t in schedule})} pet(s) — "
                f"{total} of {available_minutes} min used."
            )
            for i, task in enumerate(schedule, start=1):
                pet = owner.getPet(task.petID)
                pet_name = pet.petName if pet else f"Pet {task.petID}"
                st.markdown(
                    f"**{i}. [{task.taskType.value.upper()}]** for **{pet_name}** "
                    f"— {task.duration} min | {task.priority} priority | {task.frequency.value}"
                )
                st.caption(task.description)

    # Mark a task complete
    all_tasks = owner.getAllTasks()
    pending = [t for t in all_tasks if not t.is_completed]
    if pending:
        st.markdown("---")
        st.markdown("**Mark a task complete:**")
        task_labels = {
            f"[{owner.getPet(t.petID).petName}] {t.priority} — {t.taskType.value}: {t.description}": t.taskID
            for t in pending
        }
        chosen_label = st.selectbox("Select task", list(task_labels.keys()), key="complete_task")
        if st.button("Mark complete"):
            scheduler = Scheduler(owner)
            if scheduler.markTaskComplete(task_labels[chosen_label]):
                st.success("Task marked as complete!")
                st.rerun()
            else:
                st.error("Task not found.")
