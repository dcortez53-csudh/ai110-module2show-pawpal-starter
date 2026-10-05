# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The system is built around four classes: Task, Pet, Owner, and Scheduler. Task represents a single care activity (a walk, feeding, medication, etc.) with a description, time, duration, priority, frequency, and completion status. Pet holds a pet's basic infor plus a list of assigned tasks. Owner holds a person's name and a list of pets, and provides a single place to access every task across all pets. Schedule is the brain, it takes an Owner and produces a daily plan by soritng tasks by time, filtering by pet or completion status, detecting time conflicts, and handling recurring tasks. I chose this four-class split because it maps cleanly to the scenario: each class owns one layer of the data, and the Scheduler handles all the algorithmic work without cluttering the data classes.

**b. Design changes**

No changes were made at this stage. The AI review flagged a few minor considerations (task-pet association in 'get_all_tasks()', description-based removal, conflict detection scope), but none required a design change before implementation. I'll revisit them if they become real issues during Phase 2.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three constraints: task time ('HH:MM''), priority level (low/medium/high), and completion status. Time is the primary sort key because a pet owner's day is anchored to specific moments: morning walk, evening feeding, medication windows. Priority is used as a tie-breaker when two tasks share the same time, so high-priority items appear first if there's a conflict. Completion status is used to filter out tasks already done for the day, so the schedule only shows what's still outstanding.

**b. Tradeoffs**

The scheduler only checks for **exact time matches** when detecing conflicts, not overlapping durations. A 30-minute walk starting at 08:00 and a 10-minute feeding starting at 08:15 will not be flagged, even though the feeding overlaps the walk. This tradeoff is reasonable because (a) the project spec asks for "basic conflict detection," and (b) a strict overlap check would require normalizing times into datetime objects and comparing intervals, which adds complexity for a demo. The current approach catches the most common real-world case: two tasks scheduled at the exact same minute.

---

## 3. AI Collaboration

**a. How you used AI**

I used an AI coding assistant as a design and implementation partner across every phase. In Phase 1, I asked it to draft a Mermaid UML diagram from my brainstormed class list, then to generate dataclass skeletons that matched the diagram. In Phase 2, I asked it to flesh out the method bodies — for example, "How should the Scheduler retrieve all tasks from the Owner's pets?" — and to draft a CLI demo script. In Phase 4, I asked it how to use `timedelta` for daily and weekly recurrence, and how to write a lightweight conflict detector that returns warnings instead of crashing. In Phase 5, I asked it to draft pytest cases covering sorting, recurrence, and conflicts. The most useful prompts were specific and referenced the actual code: "Based on my skeletons in pawpal_system.py, how should the Scheduler retrieve all tasks from the Owner's pets?" and "Give me three edge cases that might break the conflict detector." Vague prompts like "make this better" produced generic suggestions that didn't fit the design.

**b. Judgment and verification**

One suggestion I did not accept as written: in Phase 1, the AI proposed a separate `Schedule` class to hold the sorted output, with a reference back to the Scheduler. That would have added a fifth class that wasn't in my UML and didn't have a clear responsibility — the schedule is just a list of Tasks, not a persistent entity. I rejected it and kept the design at four classes, with `Scheduler.get_todays_schedule()` returning `List[Task]` directly. I documented this in reflection §1b as "no changes made" because the rejection was about scope, not a design fix. I verified the choice by reading the four classes afterward and confirming no information was missing — every method still had a home, and the schedule output was still accessible from the Scheduler.

---

## 4. Testing and Verification

**a. What you tested**

The pytest suite covers 11 tests across five groups. Task basics: that `mark_complete()` flips the completion flag, and that `Pet.add_task()` increases the task count. Sorting: that tasks come back in chronological order regardless of insertion order, and that same-time tasks sort by priority (high → medium → low). Recurrence: that completing a daily task creates a new instance due tomorrow, a weekly task creates one due in 7 days, and a one-time task does not recur. Conflict detection: that duplicate times produce a warning, and unique times return an empty list. Edge cases: that an empty owner returns an empty schedule, and that completed tasks are excluded from today's schedule. These tests are important because they lock in the exact behaviors the scheduler is supposed to have — sorting, recurrence, and conflict detection are the "smart" features the project is graded on, and a silent regression in any of them would be invisible from the UI alone.

**b. Confidence**

Confidence level: 4 out of 5 stars. All 11 tests pass, the CLI demo behaves correctly, and the Streamlit UI exercises the same code paths. The main uncertainty is the conflict detector — it only catches exact time matches, not overlapping durations. If I had more time, I would add tests for overlapping intervals (e.g., a 30-minute task at 08:00 and a 10-minute task at 08:15), tasks that span midnight, and malformed time strings like "8:5" or "25:00".

---

## 5. Reflection

**a. What went well**

The part I'm most satisfied with is the CLI-first workflow. Building and verifying `main.py` before touching Streamlit meant that by the time I wired `app.py` to `pawpal_system.py`, the backend was already known-good. Every bug I hit (a sorting tie-breaker, a missing `pet_name` on tasks) surfaced in the terminal where it was easy to debug, not in the browser where it would have been harder to isolate.

**b. What you would improve**

If I had another iteration, I would add a proper date layer. Right now `due_date` exists on Task but the schedule only considers today — every task is treated as if it happens today. A real pet care app would need to know that a weekly bath is due next Tuesday, and only show today's tasks. I would also replace the exact-time conflict detection with interval overlap detection, so back-to-back tasks that actually overlap get flagged.

**c. Key takeaway**

The most important thing I learned is that working with AI on a coding task is really about being a careful reader and decider, not a typist. The AI produced a first draft of everything — UML, dataclasses, method bodies, tests — but the good parts came from me asking specific questions and the design staying coherent from one phase to the next. When I let the AI expand the scope (like the extra `Schedule` class), it drifted from the design. When I kept it anchored to the four classes and the phase goals, it was genuinely useful.