"""PawPal+ CLI demo script.

Creates an Owner, two Pets, and a handful of Tasks, then demonstrates
sorting, conflict detection, and recurring task handling.
"""
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner("Dennis")

    biscuit = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby")

    # Tasks added out of order so we can verify sorting
    biscuit.add_task(Task(description="Evening walk", time="18:00", duration_minutes=30, priority="high"))
    biscuit.add_task(Task(description="Morning walk", time="08:00", duration_minutes=30, priority="high"))
    biscuit.add_task(Task(description="Feeding", time="09:00", duration_minutes=10, priority="high"))
    whiskers.add_task(Task(description="Feeding", time="07:30", duration_minutes=5, priority="high"))
    whiskers.add_task(Task(description="Play time", time="14:00", duration_minutes=20, priority="medium"))

    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    scheduler = Scheduler(owner)

    # --- Sorted schedule ---
    print(f"\nToday's Schedule for {owner.name}")
    print("=" * 60)
    for task in scheduler.get_todays_schedule():
        print(
            f"{task.time}  {task.pet_name:<9}  {task.description} "
            f"({task.duration_minutes} min, priority: {task.priority})"
        )

    # --- Conflict detection: add a duplicate time ---
    biscuit.add_task(Task(description="Medication", time="08:00", duration_minutes=5, priority="high"))
    schedule = scheduler.get_todays_schedule()
    conflicts = scheduler.detect_conflicts(schedule)
    print("\nConflict check:")
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")

    # --- Recurring task demo ---
    daily = Task(
        description="Daily feeding",
        time="07:00",
        duration_minutes=10,
        priority="high",
        frequency="daily",
    )
    whiskers.add_task(daily)
    print(f"\nBefore completion: {whiskers.task_count()} tasks for {whiskers.name}")
    new_task = scheduler.complete_task(daily)
    print(f"Marked '{daily.description}' complete.")
    print(f"Next occurrence due: {new_task.due_date} at {new_task.time}")
    print(f"After completion: {whiskers.task_count()} tasks for {whiskers.name}")


if __name__ == "__main__":
    main()
