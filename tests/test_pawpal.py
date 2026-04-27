import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pawpal_system import Task, TaskType, Frequency, Pet


# -----------------------------------------------------------------------------
# Test Suite: TestTaskCompletion
#
# Purpose:
#   Verifies that calling complete() on a Task correctly updates its status.
#
# Why it matters:
#   The entire scheduling system depends on is_completed being accurate.
#   If complete() silently fails or doesn't persist the change, completed tasks
#   would keep appearing in pending lists and could be scheduled again by error.
#
# Setup:
#   A fresh Task is created before each test via setUp(). It represents a
#   daily 30-minute walk with priority 1. is_completed defaults to False.
# -----------------------------------------------------------------------------
class TestTaskCompletion(unittest.TestCase):
    def setUp(self):
        # A new Task instance is built before every test method runs,
        # so each test starts from the same clean state (is_completed = False).
        self.task = Task(
            taskID=1,
            taskType=TaskType.WALK,
            description="Morning walk",
            duration=30.0,
            frequency=Frequency.DAILY,
            priority=1,
        )

    def test_mark_complete_changes_status(self):
        # Step 1 — Precondition:
        #   Confirm the task starts as incomplete. Expected: is_completed == False.
        #   If this fails, setUp() is broken or the Task dataclass has a bad default.
        self.assertFalse(self.task.is_completed)

        # Step 2 — Action:
        #   Call complete(), the method that marks a task as done.
        self.task.complete()

        # Step 3 — Postcondition:
        #   is_completed must now be True. Expected: is_completed == True.
        #   If this fails, complete() is not setting the flag correctly.
        self.assertTrue(self.task.is_completed)


# -----------------------------------------------------------------------------
# Test Suite: TestTaskAddition
#
# Purpose:
#   Verifies that calling addTask() on a Pet actually appends the task to
#   that pet's task list, increasing its length by exactly 1.
#
# Why it matters:
#   A pet's task list is the single source of truth for everything the
#   Scheduler reads. If addTask() doesn't append (e.g. returns early, stores
#   elsewhere, or silently drops the task), the task will never be scheduled
#   and no error would be raised to alert the caller.
#
# Setup:
#   A Pet ("Buddy") with an empty task list and a single FEED Task are created
#   fresh before each test via setUp().
# -----------------------------------------------------------------------------
class TestTaskAddition(unittest.TestCase):
    def setUp(self):
        # Pet starts with no tasks (default_factory=list gives an empty list).
        self.pet = Pet(petID=1, species="Dog", petName="Buddy", ownerID=10)

        # A daily feeding task with priority 1 to be added to Buddy.
        self.task = Task(
            taskID=2,
            taskType=TaskType.FEED,
            description="Evening meal",
            duration=10.0,
            frequency=Frequency.DAILY,
            priority=1,
        )

    def test_add_task_increases_count(self):
        # Step 1 — Precondition:
        #   Confirm the pet has zero tasks. Expected: len(pet.tasks) == 0.
        #   If this fails, the Pet dataclass is not initializing tasks as empty.
        self.assertEqual(len(self.pet.tasks), 0)

        # Step 2 — Action:
        #   Add the task to the pet's task list via addTask().
        self.pet.addTask(self.task)

        # Step 3 — Postcondition:
        #   The list must now contain exactly 1 task. Expected: len(pet.tasks) == 1.
        #   If this fails, addTask() did not append the task to self.tasks.
        self.assertEqual(len(self.pet.tasks), 1)


if __name__ == "__main__":
    unittest.main()
