from pawpal_system import Task, Pet


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
