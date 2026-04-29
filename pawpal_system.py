from dataclasses import dataclass, field
from enum import Enum


class TaskType(Enum):
    """Enumeration of possible task types for pet care."""
    WALK = "walk"
    FEED = "feed"
    MED = "med"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"


class Frequency(Enum):
    """Enumeration of possible frequencies for tasks."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    AS_NEEDED = "as_needed"


@dataclass
class Task:
    """Represents a single care activity assigned to a pet, with scheduling metadata and completion state."""
    taskID: int
    taskType: TaskType
    description: str
    duration: float       # in minutes
    frequency: Frequency
    priority: str         # "High", "Medium", or "Low"
    petID: int = 0        # which pet this task belongs to
    is_completed: bool = False
    time: str = "00:00"   # scheduled time of day in "HH:MM" 24-hour format

    def complete(self):
        """Mark this task as completed."""
        self.is_completed = True

    def reset(self):
        """Reset this task to incomplete."""
        self.is_completed = False

    def setTaskType(self, taskType: TaskType):
        """Update the type of care this task represents."""
        self.taskType = taskType

    def setDescription(self, description: str):
        """Update the human-readable description of this task."""
        self.description = description

    def setDuration(self, duration: float):
        """Update the estimated duration of this task in minutes."""
        self.duration = duration

    def setFrequency(self, frequency: Frequency):
        """Update how often this task should recur."""
        self.frequency = frequency

    def setPriority(self, rank: str):
        """Update the scheduling priority: 'High', 'Medium', or 'Low'."""
        self.priority = rank


@dataclass
class Pet:
    """Represents a pet belonging to an owner, holding all of that pet's care tasks."""
    petID: int
    species: str
    petName: str
    ownerID: int           # reference by ID to avoid sync issues with Owner
    tasks: list[Task] = field(default_factory=list)

    def addTask(self, task: Task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def removeTask(self, taskID: int):
        """Remove the task with the given ID from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.taskID != taskID]

    def getTask(self, taskID: int) -> Task | None:
        """Return the task matching taskID, or None if not found."""
        return next((t for t in self.tasks if t.taskID == taskID), None)

    def getPendingTasks(self) -> list[Task]:
        """Return all incomplete tasks for this pet."""
        return [t for t in self.tasks if not t.is_completed]


@dataclass
class Owner:
    """Represents a pet owner with their preferences and the list of pets they are responsible for."""
    ownerID: int
    ownerName: str
    pets: list[Pet] = field(default_factory=list)
    preferred_walk_time: str = "morning"        # "morning", "afternoon", "evening"
    avoid_task_types: list[TaskType] = field(default_factory=list)

    def addPet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def removePet(self, petID: int):
        """Remove the pet with the given ID from this owner's pet list."""
        self.pets = [p for p in self.pets if p.petID != petID]

    def getPet(self, petID: int) -> Pet | None:
        """Return the pet matching petID, or None if not found."""
        return next((p for p in self.pets if p.petID == petID), None)

    def getAllTasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """
    The brain of PawPal. Retrieves, organizes, and manages tasks across all
    pets belonging to an owner, respecting owner preferences.
    """

    def __init__(self, owner: Owner):
        """Bind the scheduler to a single owner whose pets and tasks it will manage."""
        self.owner = owner

    def getAllTasks(self) -> list[Task]:
        """Return every task across all pets owned by this owner."""
        return self.owner.getAllTasks()

    def getPendingTasks(self) -> list[Task]:
        """Return all incomplete tasks across every pet."""
        return [t for t in self.getAllTasks() if not t.is_completed]

    _PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

    def getTasksByPriority(self, pending_only: bool = False) -> list[Task]:
        """Return tasks sorted High → Medium → Low, excluding avoided task types."""
        tasks = self.getPendingTasks() if pending_only else self.getAllTasks()
        avoid = self.owner.avoid_task_types
        eligible = [t for t in tasks if t.taskType not in avoid]
        return sorted(eligible, key=lambda t: self._PRIORITY_ORDER.get(t.priority, 99))

    def getTasksByPet(self, petID: int, pending_only: bool = False) -> list[Task]:
        """Return tasks for a specific pet sorted by priority, or an empty list if the pet doesn't exist."""
        pet = self.owner.getPet(petID)
        if pet is None:
            return []
        tasks = pet.getPendingTasks() if pending_only else pet.tasks
        return sorted(tasks, key=lambda t: self._PRIORITY_ORDER.get(t.priority, 99))

    _RECURRING = {Frequency.DAILY, Frequency.WEEKLY, Frequency.MONTHLY}

    def markTaskComplete(self, taskID: int) -> bool:
        """Mark a task complete by ID and, for recurring frequencies, enqueue the next occurrence.

        Returns True if the task was found, False otherwise.
        """
        for task in self.getAllTasks():
            if task.taskID == taskID:
                task.complete()
                if task.frequency in self._RECURRING:
                    self._enqueueNextOccurrence(task)
                return True
        return False

    def _enqueueNextOccurrence(self, completed_task: Task):
        """Copy a completed recurring task as a new pending entry, assigning it the next available ID."""
        all_ids = [t.taskID for t in self.getAllTasks()]
        new_id = max(all_ids) + 1 if all_ids else 1
        pet = self.owner.getPet(completed_task.petID)
        if pet is None:
            return
        pet.addTask(Task(
            taskID=new_id,
            taskType=completed_task.taskType,
            description=completed_task.description,
            duration=completed_task.duration,
            frequency=completed_task.frequency,
            priority=completed_task.priority,
            petID=completed_task.petID,
            time=completed_task.time,
        ))

    def resetDailyTasks(self):
        """Resets completion status for all DAILY tasks (call at start of each day)."""
        for task in self.getAllTasks():
            if task.frequency == Frequency.DAILY:
                task.reset()

    def generateSchedule(self, available_minutes: float) -> list[Task]:
        """Return the highest-priority pending tasks that fit within available_minutes, excluding avoided types."""
        schedule = []
        remaining = available_minutes
        for task in self.getTasksByPriority(pending_only=True):
            if task.duration <= remaining:
                schedule.append(task)
                remaining -= task.duration
        return schedule

    def filter_tasks_by_pet_name(self) -> list[Task]:
        """Return all tasks (pending and done) grouped and sorted alphabetically by pet name."""
        return sorted(self.getAllTasks(), key=lambda t: self.owner.getPet(t.petID).petName)

    def sort_by_time(self, pending_only: bool = False, descending: bool = False) -> list[Task]:
        """Sort tasks by 'HH:MM' start time; pending_only excludes done tasks, descending reverses order."""
        tasks = self.getPendingTasks() if pending_only else self.getAllTasks()
        return sorted(tasks, key=lambda t: t.time, reverse=descending)

    def check_conflict(self, task: Task) -> str | None:
        """Return a warning string if a pending task already occupies the candidate's time slot, else None."""
        for existing in self.getPendingTasks():
            if existing.time == task.time:
                pet = self.owner.getPet(existing.petID)
                pet_name = pet.petName if pet else f"Pet {existing.petID}"
                return (f"Warning: '{task.description}' at {task.time} conflicts with "
                        f"'{existing.description}' ({pet_name})")
        return None

    def detect_conflicts(self) -> dict[str, list[Task]]:
        """Return a dict of 'HH:MM' → [Task, ...] for every pending time slot with 2 or more tasks."""
        time_slots: dict[str, list[Task]] = {}
        for task in self.getPendingTasks():
            time_slots.setdefault(task.time, []).append(task)
        return {time: tasks for time, tasks in time_slots.items() if len(tasks) > 1}

    def displaySchedule(self, available_minutes: float):
        """Print a formatted daily schedule of tasks that fit within available_minutes."""
        schedule = self.generateSchedule(available_minutes)
        if not schedule:
            print("No tasks fit within the available time.")
            return

        print(f"Daily Schedule ({available_minutes} min available):")
        for i, task in enumerate(schedule, start=1):
            pet = self.owner.getPet(task.petID)
            pet_name = pet.petName if pet else f"Pet {task.petID}"
            status = "done" if task.is_completed else "pending"
            print(f"  {i}. [{task.priority}] {task.taskType.value} for {pet_name}"
                  f" — {task.duration} min | {task.frequency.value} | {status}"
                  f"\n     {task.description}")
