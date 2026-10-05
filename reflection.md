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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
