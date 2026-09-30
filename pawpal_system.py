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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        ...

    def to_dict(self) -> dict:
        """Return this task as a plain dictionary."""
        ...


@dataclass
class Pet:
    name: str
    species: str = ""
    breed: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        ...

    def remove_task(self, description: str) -> None:
        """Remove a task by description."""
        ...

    def task_count(self) -> int:
        """Return the number of tasks for this pet."""
        ...


class Owner:
    def __init__(self, name: str):
        """Initialize an owner with an empty list of pets."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        ...

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        ...

    def find_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None."""
        ...


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_todays_schedule(self) -> List[Task]:
        """Return all tasks sorted by time."""
        ...

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by HH:MM time string."""
        ...

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to a given pet."""
        ...

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        ...

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warning strings for tasks with the same time."""
        ...

    def handle_recurring(self, task: Task) -> Optional[Task]:
        """If a recurring task is completed, return the next instance."""
        ...
