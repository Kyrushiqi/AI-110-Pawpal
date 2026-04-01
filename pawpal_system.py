from dataclasses import dataclass, field
from enum import Enum


class TaskType(Enum):
    WALK = "walk"
    FEED = "feed"
    MED = "med"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"


@dataclass
class Pet:
    petID: int
    species: str
    petName: str
    ownerID: int  # reference by ID to avoid sync issues with Owner


@dataclass
class Task:
    taskID: int
    taskType: TaskType
    duration: float  # in minutes
    priority: int    # lower number = higher priority; must be unique across tasks
    petID: int       # which pet this task belongs to

    def setTaskType(self, taskType: TaskType):
        self.taskType = taskType

    def setDuration(self, duration: float):
        self.duration = duration

    def setPriority(self, rank: int):
        self.priority = rank


@dataclass
class OwnerPreferences:
    preferred_walk_time: str = "morning"   # "morning", "afternoon", "evening"
    avoid_task_types: list[TaskType] = field(default_factory=list)


@dataclass
class Owner:
    ownerID: int
    ownerName: str
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    ownerPreferences: OwnerPreferences = field(default_factory=OwnerPreferences)

    def addPet(self, pet: Pet):
        self.pets.append(pet)

    def removePet(self, petID: int):
        self.pets = [p for p in self.pets if p.petID != petID]

    def addTask(self, task: Task):
        if any(t.priority == task.priority for t in self.tasks):
            raise ValueError(f"A task with priority {task.priority} already exists.")
        self.tasks.append(task)

    def removeTask(self, taskID: int):
        self.tasks = [t for t in self.tasks if t.taskID != taskID]

    def setOwnerPreferences(self, preferences: OwnerPreferences):
        self.ownerPreferences = preferences

    def generateSchedule(self, available_minutes: float) -> list[Task]:
        """
        Returns tasks sorted by priority that fit within available_minutes.
        Excludes task types the owner wants to avoid.
        """
        eligible = [
            t for t in self.tasks
            if t.taskType not in self.ownerPreferences.avoid_task_types
        ]
        sorted_tasks = sorted(eligible, key=lambda t: t.priority)

        schedule = []
        remaining = available_minutes
        for task in sorted_tasks:
            if task.duration <= remaining:
                schedule.append(task)
                remaining -= task.duration

        return schedule

    def displaySchedule(self, available_minutes: float):
        schedule = self.generateSchedule(available_minutes)
        if not schedule:
            print("No tasks fit within the available time.")
            return

        print(f"Daily Schedule ({available_minutes} min available):")
        for i, task in enumerate(schedule, start=1):
            pet = next((p for p in self.pets if p.petID == task.petID), None)
            pet_name = pet.petName if pet else f"Pet {task.petID}"
            print(f"  {i}. [{task.priority}] {task.taskType.value} "
                  f"for {pet_name} — {task.duration} min")
