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

## Smarter Scheduling

The `Scheduler` class was extended with five new features beyond basic priority sorting:

- **`sort_by_time(pending_only, descending)`** — sorts tasks by their `HH:MM` start time, earliest to latest by default. Pass `descending=True` to reverse, or `pending_only=True` to hide completed tasks.
- **`filter_tasks_by_pet_name()`** — returns all tasks across every pet, alphabetically grouped by pet name (Buddy → Mochi → Zeze).
- **`_enqueueNextOccurrence`** — called automatically when a daily, weekly, or monthly task is marked complete. Creates a fresh pending copy so recurring tasks never fall off the schedule.
- **`check_conflict(task)`** — pre-add safety check. Before inserting a new task, call this to get a plain-English warning if another pending task already owns that time slot. Returns `None` if the slot is free.
- **`detect_conflicts()`** — full schedule audit. Scans all pending tasks and returns a dict of every time slot where two or more tasks overlap. Completed tasks are excluded, so finishing a task clears it from the conflict report.

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
