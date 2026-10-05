from datetime import date, timedelta

from pawpal_system import Task, Pet, Owner, Scheduler


# --- Existing basic tests ---

def test_mark_complete_changes_status():
    """Verify mark_complete() flips the completed flag."""
    task = Task(description="Walk the dog", time="08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    """Verify adding a task to a Pet increases its task count."""
    pet = Pet(name="Biscuit", species="Dog")
    assert pet.task_count() == 0
    pet.add_task(Task(description="Feeding", time="09:00"))
    assert pet.task_count() == 1
    pet.add_task(Task(description="Walk", time="18:00"))
    assert pet.task_count() == 2


# --- Sorting correctness ---

def test_sort_by_time_returns_chronological_order():
    """Verify tasks come back sorted by HH:MM regardless of insertion order."""
    owner = Owner("Test")
    pet = Pet(name="Rex")
    pet.add_task(Task(description="Evening", time="18:00"))
    pet.add_task(Task(description="Morning", time="08:00"))
    pet.add_task(Task(description="Noon", time="12:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.sort_by_time(owner.get_all_tasks())

    times = [t.time for t in result]
    assert times == ["08:00", "12:00", "18:00"]


def test_sort_by_time_breaks_ties_with_priority():
    """Verify same-time tasks order high priority first."""
    owner = Owner("Test")
    pet = Pet(name="Rex")
    pet.add_task(Task(description="Low", time="09:00", priority="low"))
    pet.add_task(Task(description="High", time="09:00", priority="high"))
    pet.add_task(Task(description="Medium", time="09:00", priority="medium"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    result = scheduler.sort_by_time(owner.get_all_tasks())

    priorities = [t.priority for t in result]
    assert priorities == ["high", "medium", "low"]


# --- Recurrence logic ---

def test_daily_task_creates_next_day_occurrence():
    """Marking a daily task complete adds a new task due tomorrow."""
    owner = Owner("Test")
    pet = Pet(name="Rex")
    daily = Task(description="Feed", time="07:00", frequency="daily")
    pet.add_task(daily)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    tomorrow = date.today() + timedelta(days=1)

    before = pet.task_count()
    new_task = scheduler.complete_task(daily)

    assert new_task is not None
    assert new_task.due_date == tomorrow
    assert new_task.completed is False
    assert pet.task_count() == before + 1


def test_weekly_task_creates_next_week_occurrence():
    """Marking a weekly task complete adds a new task due in 7 days."""
    owner = Owner("Test")
    pet = Pet(name="Rex")
    weekly = Task(description="Bath", time="10:00", frequency="weekly")
    pet.add_task(weekly)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    next_week = date.today() + timedelta(weeks=1)

    new_task = scheduler.complete_task(weekly)

    assert new_task is not None
    assert new_task.due_date == next_week


def test_once_task_does_not_recur():
    """A one-time task should not spawn a follow-up."""
    owner = Owner("Test")
    pet = Pet(name="Rex")
    once = Task(description="Vet visit", time="15:00", frequency="once")
    pet.add_task(once)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    before = pet.task_count()

    new_task = scheduler.complete_task(once)

    assert new_task is None
    assert pet.task_count() == before


# --- Conflict detection ---

def test_detect_conflicts_flags_duplicate_times():
    """Two tasks at the same time produce a conflict warning."""
    owner = Owner("Test")
    pet = Pet(name="Rex")
    pet.add_task(Task(description="Walk", time="08:00"))
    pet.add_task(Task(description="Meds", time="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(owner.get_all_tasks())

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_detect_conflicts_returns_empty_for_unique_times():
    """No conflicts when every task has a distinct time."""
    owner = Owner("Test")
    pet = Pet(name="Rex")
    pet.add_task(Task(description="Walk", time="08:00"))
    pet.add_task(Task(description="Feed", time="09:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(owner.get_all_tasks())

    assert warnings == []


# --- Edge cases ---

def test_empty_owner_has_empty_schedule():
    """A scheduler with no pets returns an empty schedule."""
    owner = Owner("Test")
    scheduler = Scheduler(owner)

    assert scheduler.get_todays_schedule() == []


def test_completed_tasks_are_excluded_from_schedule():
    """Completed tasks should not show up in today's schedule."""
    owner = Owner("Test")
    pet = Pet(name="Rex")
    done = Task(description="Done", time="08:00", completed=True)
    pending = Task(description="Pending", time="09:00")
    pet.add_task(done)
    pet.add_task(pending)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()

    descriptions = [t.description for t in schedule]
    assert "Done" not in descriptions
    assert "Pending" in descriptions
