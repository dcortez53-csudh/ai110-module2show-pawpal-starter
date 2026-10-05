"""PawPal+ backend logic layer.

Four core classes:
    Task      - a single care activity
    Pet       - an animal with a list of tasks
    Owner     - a person with multiple pets
    Scheduler - the brain that organizes tasks across pets
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    description: str
    time: str = "08:00"            # HH:MM
    duration_minutes: int = 15
    priority: str = "medium"       # low / medium / high
    frequency: str = "once"        # once / daily / weekly
    completed: bool = False
    pet_name: str = ""             # filled in when added to a Pet

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """Return this task as a plain dictionary."""
        return {
            "description": self.description,
            "time": self.time,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "completed": self.completed,
            "pet_name": self.pet_name,
        }


@dataclass
class Pet:
    name: str
    species: str = ""
    breed: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str) -> None:
        """Remove a task by description."""
        self.tasks = [t for t in self.tasks if t.description != description]

    def task_count(self) -> int:
        """Return the number of tasks for this pet."""
        return len(self.tasks)


class Owner:
    def __init__(self, name: str):
        """Initialize an owner with an empty list of pets."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def find_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_todays_schedule(self) -> List[Task]:
        """Return all tasks sorted by time."""
        return self.sort_by_time(self.owner.get_all_tasks())

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by HH:MM time string."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to a given pet."""
        return [
            t for t in self.owner.get_all_tasks()
            if t.pet_name.lower() == pet_name.lower()
        ]

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning strings for tasks with the same time."""
        warnings: List[str] = []
        seen = {}
        for task in tasks:
            if task.time in seen:
                warnings.append(
                    f"Conflict at {task.time}: '{seen[task.time]}' "
                    f"and '{task.description}'"
                )
            else:
                seen[task.time] = task.description
        return warnings

    def handle_recurring(self, task: Task) -> Optional[Task]:
        """If a completed task is recurring, create the next occurrence."""
        if not task.completed or task.frequency == "once":
            return None
        new_task = Task(
            description=task.description,
            time=task.time,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
            completed=False,
            pet_name=task.pet_name,
        )
        pet = self.owner.find_pet(task.pet_name)
        if pet:
            pet.add_task(new_task)
        return new_task
