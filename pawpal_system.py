"""PawPal+ backend logic layer.

Four core classes:
    Task      - a single care activity
    Pet       - an animal with a list of tasks
    Owner     - a person with multiple pets
    Scheduler - the brain that organizes tasks across pets
"""
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    description: str
    time: str = "08:00"                            # HH:MM
    duration_minutes: int = 15
    priority: str = "medium"                       # low / medium / high
    frequency: str = "once"                        # once / daily / weekly
    completed: bool = False
    pet_name: str = ""
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next occurrence, or None if not recurring."""
        if self.frequency == "daily":
            offset = timedelta(days=1)
        elif self.frequency == "weekly":
            offset = timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            completed=False,
            pet_name=self.pet_name,
            due_date=self.due_date + offset,
        )

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
            "due_date": self.due_date.isoformat(),
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
        """Return all incomplete tasks sorted by time, then priority."""
        tasks = self.owner.get_all_tasks()
        return self.sort_by_time([t for t in tasks if not t.completed])

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by HH:MM time; break ties by priority."""
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            tasks,
            key=lambda t: (t.time, priority_rank.get(t.priority, 1)),
        )

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

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and add its next occurrence if recurring."""
        task.mark_complete()
        new_task = task.next_occurrence()
        if new_task:
            pet = self.owner.find_pet(task.pet_name)
            if pet:
                pet.add_task(new_task)
        return new_task
