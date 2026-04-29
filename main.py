from pawpal_system import Task, TaskType, Frequency, Pet, Owner, Scheduler

# --- Setup Owner ---
owner = Owner(ownerID=1, ownerName="Alex")

# --- Create Pets ---
buddy = Pet(petID=1, species="Dog",    petName="Buddy", ownerID=1)
mochi = Pet(petID=2, species="Cat",    petName="Mochi", ownerID=1)
zeze  = Pet(petID=3, species="Bird",   petName="Zeze",  ownerID=1)

owner.addPet(buddy)
owner.addPet(mochi)
owner.addPet(zeze)

# --- Add Tasks OUT OF ORDER (times intentionally scrambled across all pets) ---

# Buddy — evening → morning → afternoon
buddy.addTask(Task(
    taskID=1, taskType=TaskType.MED,
    description="Heartworm prevention tablet",
    duration=2.0, frequency=Frequency.MONTHLY,
    priority="High", petID=buddy.petID, time="19:00",
))
buddy.addTask(Task(
    taskID=2, taskType=TaskType.WALK,
    description="Morning walk around the block",
    duration=30.0, frequency=Frequency.DAILY,
    priority="Medium", petID=buddy.petID, time="06:30",
))
buddy.addTask(Task(
    taskID=3, taskType=TaskType.FEED,
    description="Afternoon kibble — 1 cup dry food",
    duration=5.0, frequency=Frequency.DAILY,
    priority="High", petID=buddy.petID, time="13:00",
))

# Mochi — afternoon → morning → noon
mochi.addTask(Task(
    taskID=4, taskType=TaskType.ENRICHMENT,
    description="Laser pointer play session",
    duration=15.0, frequency=Frequency.DAILY,
    priority="Low", petID=mochi.petID, time="16:45",
))
mochi.addTask(Task(
    taskID=5, taskType=TaskType.FEED,
    description="Wet food — half pouch",
    duration=5.0, frequency=Frequency.DAILY,
    priority="High", petID=mochi.petID, time="07:15",
))
mochi.addTask(Task(
    taskID=6, taskType=TaskType.GROOMING,
    description="Brush coat to reduce shedding",
    duration=10.0, frequency=Frequency.WEEKLY,
    priority="Medium", petID=mochi.petID, time="12:00",
))

# Zeze — noon → early morning → late evening
# taskID=7 shares 07:15 with Mochi's feed (cross-pet conflict)
# taskID=9 shares 13:00 with Buddy's feed (cross-pet conflict)
zeze.addTask(Task(
    taskID=7, taskType=TaskType.ENRICHMENT,
    description="Out-of-cage flight time",
    duration=20.0, frequency=Frequency.DAILY,
    priority="Medium", petID=zeze.petID, time="07:15",
))
zeze.addTask(Task(
    taskID=8, taskType=TaskType.FEED,
    description="Seed mix and fresh fruit",
    duration=5.0, frequency=Frequency.DAILY,
    priority="High", petID=zeze.petID, time="08:00",
))
zeze.addTask(Task(
    taskID=9, taskType=TaskType.GROOMING,
    description="Mist feathers with water bottle",
    duration=3.0, frequency=Frequency.WEEKLY,
    priority="Low", petID=zeze.petID, time="13:00",
))

# --- Build Scheduler ---
scheduler = Scheduler(owner)

# Mark a few tasks complete so status column shows variety
scheduler.markTaskComplete(taskID=2)   # Buddy's walk → done
scheduler.markTaskComplete(taskID=5)   # Mochi's feed → done
scheduler.markTaskComplete(taskID=8)   # Zeze's feed  → done

SEP = "=" * 58

# ── 1. sort_by_time — earliest → latest ──────────────────────────────────────
print(SEP)
print("  sort_by_time()  —  earliest → latest")
print(SEP)
for task in scheduler.sort_by_time():
    pet = owner.getPet(task.petID)
    status = "done" if task.is_completed else "pending"
    print(f"  {task.time}  [{task.priority:6}]  "
          f"{task.taskType.value:<12}  {pet.petName:<6}  {status:<7}  {task.description}")

# ── 2. sort_by_time — latest → earliest ──────────────────────────────────────
print()
print(SEP)
print("  sort_by_time(descending=True)  —  latest → earliest")
print(SEP)
for task in scheduler.sort_by_time(descending=True):
    pet = owner.getPet(task.petID)
    status = "done" if task.is_completed else "pending"
    print(f"  {task.time}  [{task.priority:6}]  "
          f"{task.taskType.value:<12}  {pet.petName:<6}  {status:<7}  {task.description}")

# ── 3. filter_tasks_by_pet_name — grouped alphabetically ─────────────────────
print()
print(SEP)
print("  filter_tasks_by_pet_name()  —  all tasks sorted by pet name A→Z")
print(SEP)
for task in scheduler.filter_tasks_by_pet_name():
    pet = owner.getPet(task.petID)
    status = "done" if task.is_completed else "pending"
    print(f"  {pet.petName:<6}  {task.time}  [{task.priority:6}]  "
          f"{task.taskType.value:<12}  {status:<7}  {task.description}")
print(SEP)

# ── 4. check_conflict — warn before adding a new clashing task ────────────────
print()
print(SEP)
print("  check_conflict()  —  pre-add warning for a single candidate task")
print(SEP)
candidate = Task(
    taskID=99, taskType=TaskType.MED,
    description="Flea treatment",
    duration=5.0, frequency=Frequency.MONTHLY,
    priority="High", petID=buddy.petID, time="07:15",  # clashes with Mochi + Zeze
)
warning = scheduler.check_conflict(candidate)
if warning:
    print(f"  {warning}")
else:
    print("  No conflict — safe to add.")

# ── 5. detect_conflicts — full audit of all scheduled tasks ───────────────────
print()
print(SEP)
print("  detect_conflicts()  —  full audit of all conflicting time slots")
print(SEP)
conflicts = scheduler.detect_conflicts()
if not conflicts:
    print("  No conflicts found.")
else:
    for time, tasks in sorted(conflicts.items()):
        print(f"  {time}  ({len(tasks)} tasks):")
        for t in tasks:
            pet = owner.getPet(t.petID)
            status = "done" if t.is_completed else "pending"
            print(f"    [{t.priority:6}]  {t.taskType.value:<12}  "
                  f"{pet.petName:<6}  {status:<7}  {t.description}")
print(SEP)

# ── 6. generateSchedule — today's plan within a time budget ──────────────────
available_minutes = 60.0
print()
print(SEP)
print(f"  Today's Schedule  —  {available_minutes:.0f} min available")
print(SEP)
schedule = scheduler.generateSchedule(available_minutes)
if not schedule:
    print("  No tasks fit within the available time.")
else:
    total = 0.0
    for i, task in enumerate(schedule, start=1):
        pet = owner.getPet(task.petID)
        print(f"  {i}. [{task.priority:6}]  {task.time}  {task.taskType.value:<12}  "
              f"{pet.petName:<6}  {task.duration:.0f} min  —  {task.description}")
        total += task.duration
    print(f"\n  Total: {total:.0f} / {available_minutes:.0f} min used")
print(SEP)
