"""PawPal+ CLI demo script.

Creates an Owner, two Pets, and a handful of Tasks, then prints
Today's Schedule to the terminal.
"""
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create the owner
    owner = Owner("Dennis")

    # Create two pets
    biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby")

    # Add tasks out of order so we can verify sorting works
    biscuit.add_task(Task(description="Evening walk", time="18:00", duration_minutes=30, priority="high"))
    biscuit.add_task(Task(description="Morning walk", time="08:00", duration_minutes=30, priority="high"))
    biscuit.add_task(Task(description="Feeding", time="09:00", duration_minutes=10, priority="high"))
    whiskers.add_task(Task(description="Feeding", time="07:30", duration_minutes=5, priority="high"))
    whiskers.add_task(Task(description="Play time", time="14:00", duration_minutes=20, priority="medium"))

    # Register pets with the owner
    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    # Build the schedule
    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()

    # Print it
    print(f"\nToday's Schedule for {owner.name}")
    print("=" * 40)
    for task in schedule:
        print(
            f"{task.time}  {task.pet_name:<9}  {task.description} "
            f"({task.duration_minutes} min, priority: {task.priority})"
        )

    # Conflict check
    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        print("\nConflicts:")
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("\nNo conflicts detected.")


if __name__ == "__main__":
    main()
