# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    - There will be 3 classes: owner, pet, and task. The Owner owns pet(s) and manages tasks. An owner can have 0 or many pets and tasks.
- What classes did you include, and what responsibilities did you assign to each?
    - Owner
        - Attributes: int ownerID, String ownerName, Pet[] pets, Task[] tasks, String ownerPreferences
        - Methods: addPet(Pet pet), setOwnerPreferences(String preferences), generateSchedule(), displaySchedule()
    - Pet
        - Attributes: int petID, String species, String petName, String ownerName
        - Methods: getownerName()
    - Task
        - Attributes: int taskID, String taskType, double duration, int priority
        - Methods:
        setTaskType(String taskType) --> walk, feed, med, enrichment, grooming, setDuration(double duration), setPriority(int rank)

**b. Design changes**

- Did your design change during implementation? Yes
- If yes, describe at least one change and why you made it.
1. **Added a TaskType menu (Enum)**
    - Before, task types were typed as plain text — someone could accidentally write "wlak" instead of "walk" and the app wouldn't catch it. Now only valid options (walk, feed, med, enrichment, grooming) are allowed.

2. **Pet now stores the owner's ID, not their name**
    - Before, Pet stored the owner's name as text. If the owner ever changed their name, the pet's record would show the old name. Using the ID keeps both records in sync automatically.

3. **Task now knows which pet it belongs to**
    - Tasks like "feed" or "walk" are done for a specific pet, but the original design didn't track that. Adding petID to Task makes that connection explicit, which the schedule display uses to show the pet's name.

4. **OwnerPreferences became its own structured object**
    - Before, owner preferences were a single text blob the app couldn't read or act on. Now it's a proper object with specific fields — preferred walk time and task types to avoid — so the scheduler can actually use these preferences to filter and plan.

5. **Added addTask with a duplicate priority check**
    - Without this, two tasks could have the same priority number, making it unclear which should come first. Now the app raises an error if you try to add a task with a priority that's already taken.

6. **Added removePet and removeTask**
    - The original design could only add pets and tasks, never remove them. Your app's core requirements include editing tasks, so these methods were necessary.

7. **generateSchedule now takes a time budget**
    - Before it was an empty placeholder. Now it accepts the number of available minutes, skips task types the owner wants to avoid, sorts by priority, and fits as many tasks as possible into the time window.

8. **displaySchedule now prints a readable plan**
    - Also previously empty. It now calls generateSchedule and prints each task with its priority, type, pet name, and duration in a numbered list.

**c.  3 core actions:**
1) Let a user enter basic owner + pet info
2) Let a user add/edit tasks (duration + priority at minimum)
3) Generate a daily schedule/plan based on constraints and priorities. The app should explain its plan.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers four main constraints:

1. **Priority** — Tasks are ranked High, Medium, or Low. `generateSchedule` and `getTasksByPriority` always sort by this order so the most critical care (medication, feeding) is handled before optional activities (enrichment, grooming).

2. **Available time budget** — `generateSchedule(available_minutes)` uses a greedy approach: it walks the priority-sorted list and adds each task only if its duration fits within the remaining time. Tasks that don't fit are skipped entirely rather than partially scheduled.

3. **Owner preferences** — The `avoid_task_types` list on the Owner lets the scheduler silently exclude task types the owner doesn't want to handle on a given day. This runs as a filter before any sorting, so avoided tasks never compete for time slots.

4. **Completion status** — Pending and completed tasks are tracked separately. Conflict detection and time-budget scheduling only consider incomplete tasks, so finishing a task clears it from active constraints automatically.

Priority was treated as the most important constraint because a pet's health needs (medication, meals) must be met regardless of how much time is available — it would be wrong for an enrichment task to displace a feeding just because it appeared earlier in the list. Time budget came second because it reflects a real-world limit the owner faces every day. Preferences and completion status act as pre-filters that keep the core scheduling logic simple.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Exact time match vs. overlapping duration windows**

`check_conflict()` flags a conflict only when two tasks share the exact same start time (e.g., both at `07:15`). It does not check whether a task's duration causes it to overlap with a later task — for example, a 30-minute walk starting at `07:00` and a feeding starting at `07:15` would not be flagged even though they overlap in real time.

This is a reasonable tradeoff for a pet care app at this stage: most pet tasks (feeding, grooming, medication) are short and discrete, so exact-time collisions are the most common scheduling mistake. Duration-overlap detection would require converting `"HH:MM"` strings into comparable time ranges and handling edge cases like midnight rollovers, adding complexity for a relatively rare scenario. If the app grew to include longer tasks like vet appointments or training sessions, duration-based conflict checking would become a meaningful next step.

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
