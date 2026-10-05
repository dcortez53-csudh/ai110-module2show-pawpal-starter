# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule for Dennis
========================================
07:30  Whiskers   Feeding (5 min, priority: high)
08:00  Biscuit    Morning walk (30 min, priority: high)
09:00  Biscuit    Feeding (10 min, priority: high)
14:00  Whiskers   Play time (20 min, priority: medium)
18:00  Biscuit    Evening walk (30 min, priority: high)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

The suite covers 11 tests across five areas:
- **Task basics** — `mark_complete()` flips the status flag; adding a task increases `Pet.task_count()`
- **Sorting** — tasks are returned in chronological order; same-time tasks sort by priority (high → medium → low)
- **Recurrence** — daily tasks spawn a new instance due tomorrow; weekly tasks spawn one due in 7 days; one-time tasks do not recur
- **Conflicts** — duplicate times produce a warning; unique times return an empty list
- **Edge cases** — empty owner returns an empty schedule; completed tasks are excluded from today's schedule

Sample test output:

```
collected 11 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED                       [  9%]
tests/test_pawpal.py::test_add_task_increases_count PASSED                           [ 18%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED           [ 27%]
tests/test_pawpal.py::test_sort_by_time_breaks_ties_with_priority PASSED             [ 36%]
tests/test_pawpal.py::test_daily_task_creates_next_day_occurrence PASSED             [ 45%]
tests/test_pawpal.py::test_weekly_task_creates_next_week_occurrence PASSED           [ 54%]
tests/test_pawpal.py::test_once_task_does_not_recur PASSED                           [ 63%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED             [ 72%]
tests/test_pawpal.py::test_detect_conflicts_returns_empty_for_unique_times PASSED    [ 81%]
tests/test_pawpal.py::test_empty_owner_has_empty_schedule PASSED                     [ 90%]
tests/test_pawpal.py::test_completed_tasks_are_excluded_from_schedule PASSED         [100%]

==================================== 11 passed in 0.06s ====================================
```

**Confidence level:** ⭐⭐⭐⭐ (4/5)
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.
| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by `HH:MM` string, with priority as a tie-breaker. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Filter by pet name or completion state. |
| Conflict handling | `Scheduler.detect_conflicts()` | Detects tasks with identical start times and returns a list of warning strings instead of raising. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.complete_task()` | Daily tasks get a new instance with `due_date + 1 day`; weekly tasks get `+ 7 days`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
