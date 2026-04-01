from dataclasses import dataclass, field


@dataclass
class Pet:
    petID: int
    species: str
    petName: str
    ownerName: str

    def getOwnerName(self) -> str:
        return self.ownerName


@dataclass
class Task:
    taskID: int
    taskType: str
    duration: float
    priority: int

    def setTaskType(self, taskType: str):
        self.taskType = taskType

    def setDuration(self, duration: float):
        self.duration = duration

    def setPriority(self, rank: int):
        self.priority = rank


@dataclass
class Owner:
    ownerID: int
    ownerName: str
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    ownerPreferences: str = ""

    def addPet(self, pet: Pet):
        self.pets.append(pet)

    def setOwnerPreferences(self, preferences: str):
        self.ownerPreferences = preferences

    def generateSchedule(self):
        pass

    def displaySchedule(self):
        pass
