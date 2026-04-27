from pawpal_system import Task, TaskType, Frequency, Pet, Owner, Scheduler

# --- Setup Owner ---
owner = Owner(ownerID=1, ownerName="Alex")

# --- Create Pets ---
buddy = Pet(petID=1, species="Dog", petName="Buddy", ownerID=1)
mochi = Pet(petID=2, species="Cat", petName="Mochi", ownerID=1)

owner.addPet(buddy)
owner.addPet(mochi)

# --- Add Tasks to Buddy (Dog) ---
buddy.addTask(Task(
    taskID=1,
    taskType=TaskType.WALK,
    description="Morning walk around the block",
    duration=30.0,
    frequency=Frequency.DAILY,
    priority=1,
    petID=buddy.petID,
))
buddy.addTask(Task(
    taskID=2,
    taskType=TaskType.FEED,
    description="Morning kibble — 1 cup dry food",
    duration=5.0,
    frequency=Frequency.DAILY,
    priority=2,
    petID=buddy.petID,
))
buddy.addTask(Task(
    taskID=3,
    taskType=TaskType.MED,
    description="Heartworm prevention tablet",
    duration=2.0,
    frequency=Frequency.MONTHLY,
    priority=3,
    petID=buddy.petID,
))

# --- Add Tasks to Mochi (Cat) ---
mochi.addTask(Task(
    taskID=4,
    taskType=TaskType.FEED,
    description="Wet food — half pouch",
    duration=5.0,
    frequency=Frequency.DAILY,
    priority=1,
    petID=mochi.petID,
))
mochi.addTask(Task(
    taskID=5,
    taskType=TaskType.GROOMING,
    description="Brush coat to reduce shedding",
    duration=10.0,
    frequency=Frequency.WEEKLY,
    priority=2,
    petID=mochi.petID,
))
mochi.addTask(Task(
    taskID=6,
    taskType=TaskType.ENRICHMENT,
    description="Laser pointer play session",
    duration=15.0,
    frequency=Frequency.DAILY,
    priority=3,
    petID=mochi.petID,
))

# --- Build Scheduler ---
scheduler = Scheduler(owner)

# --- Print Today's Schedule ---
available_minutes = 60.0

print("=" * 45)
print(f"  PawPal — Today's Schedule for {owner.ownerName}")
print("=" * 45)

schedule = scheduler.generateSchedule(available_minutes)

if not schedule:
    print("No tasks fit within the available time.")
else:
    total = sum(t.duration for t in schedule)
    for i, task in enumerate(schedule, start=1):
        pet = owner.getPet(task.petID)
        pet_name = pet.petName if pet else f"Pet {task.petID}"
        print(f"\n  {i}. {task.taskType.value.upper()} — {pet_name}")
        print(f"     {task.description}")
        print(f"     Duration : {task.duration} min  |  Frequency : {task.frequency.value}")
        print(f"     Priority : {task.priority}  |  Status : {'done' if task.is_completed else 'pending'}")

    print("\n" + "-" * 45)
    print(f"  Total time scheduled : {total} / {available_minutes} min")
    print("=" * 45)
