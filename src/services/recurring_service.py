"""
Service for managing recurring tasks in the todo application.

This module contains the RecurringTaskService that handles the logic for creating,
managing, and generating recurring tasks.
"""
from datetime import datetime
from typing import List, Optional
from src.domain.entities.task import Task
from src.lib.utils import calculate_next_due_date


class RecurringTaskService:
    """
    Service for handling recurring task operations.

    This service manages the creation, modification, and generation of recurring tasks.
    """

    def __init__(self, storage):
        """
        Initialize the RecurringTaskService.

        Args:
            storage: Storage interface for task persistence
        """
        self.storage = storage

    def create_recurring_task(self, title: str, description: str = "",
                            recurrence_pattern: str = "daily",
                            recurrence_interval: int = 1) -> Task:
        """
        Create a new recurring task.

        Args:
            title: Title of the task
            description: Description of the task
            recurrence_pattern: Pattern for recurrence ("daily", "weekly", "monthly")
            recurrence_interval: Interval for recurrence (number of units)

        Returns:
            Created Task object with recurring properties set

        Raises:
            ValueError: If recurrence pattern is invalid
        """
        if recurrence_pattern not in ["daily", "weekly", "monthly"]:
            raise ValueError("Recurrence pattern must be 'daily', 'weekly', or 'monthly'")

        if recurrence_interval <= 0:
            raise ValueError("Recurrence interval must be a positive integer")

        # Create a new task with recurring properties
        task = Task(
            id=0,  # Will be assigned by storage
            title=title,
            description=description,
            is_recurring=True,
            recurrence_pattern=recurrence_pattern,
            recurrence_interval=recurrence_interval,
            is_active=True,
            original_task_id=None  # This is the original
        )

        # Calculate next due date based on pattern
        task.next_due_date = self._calculate_next_due_date(
            datetime.now(),
            recurrence_pattern,
            recurrence_interval
        )

        # Set original_task_id to the ID that will be assigned
        task_id = self.storage.save_task(task)
        task.id = task_id
        task.original_task_id = task_id

        # Update the task in storage with the correct original_task_id
        self.storage.update_task(task_id, task)

        return task

    def generate_next_instance(self, recurring_task: Task) -> Optional[Task]:
        """
        Generate the next instance of a recurring task.

        Args:
            recurring_task: The recurring task to generate next instance for

        Returns:
            New Task instance or None if recurrence is not active
        """
        if not recurring_task.is_recurring or not recurring_task.is_active:
            return None

        # Calculate the next due date
        current_due_date = recurring_task.next_due_date or datetime.now()
        next_due_date = self._calculate_next_due_date(
            current_due_date,
            recurring_task.recurrence_pattern,
            recurring_task.recurrence_interval
        )

        # Check for duplicates before generating
        original_task_id = recurring_task.original_task_id or recurring_task.id
        if self.prevent_duplicate_generation(original_task_id, next_due_date):
            return None  # Duplicate already exists, don't generate

        # Create a new task instance with the same properties
        next_task = Task(
            id=0,  # Will be assigned by storage
            title=recurring_task.title,
            description=recurring_task.description,
            is_recurring=True,
            recurrence_pattern=recurring_task.recurrence_pattern,
            recurrence_interval=recurring_task.recurrence_interval,
            is_active=True,
            parent_id=recurring_task.id,
            original_task_id=original_task_id
        )

        next_task.next_due_date = next_due_date

        # Save the new instance
        task_id = self.storage.save_task(next_task)
        next_task.id = task_id

        return next_task

    def update_recurrence_settings(self, task_id: int, recurrence_pattern: Optional[str] = None,
                                 recurrence_interval: Optional[int] = None,
                                 is_active: Optional[bool] = None) -> bool:
        """
        Update recurrence settings for a recurring task.

        Args:
            task_id: ID of the task to update
            recurrence_pattern: New recurrence pattern (optional)
            recurrence_interval: New recurrence interval (optional)
            is_active: New active status (optional)

        Returns:
            Boolean indicating success
        """
        task = self.storage.get_task(task_id)
        if not task or not task.is_recurring:
            return False

        # Update fields if provided
        if recurrence_pattern is not None:
            if recurrence_pattern not in ["daily", "weekly", "monthly"]:
                raise ValueError("Recurrence pattern must be 'daily', 'weekly', or 'monthly'")
            task.recurrence_pattern = recurrence_pattern

        if recurrence_interval is not None:
            if recurrence_interval <= 0:
                raise ValueError("Recurrence interval must be a positive integer")
            task.recurrence_interval = recurrence_interval

        if is_active is not None:
            task.is_active = is_active

        return self.storage.update_task(task_id, task)

    def cancel_recurrence(self, task_id: int) -> bool:
        """
        Cancel recurrence for a recurring task.

        Args:
            task_id: ID of the task to cancel recurrence for

        Returns:
            Boolean indicating success
        """
        task = self.storage.get_task(task_id)
        if not task or not task.is_recurring:
            return False

        task.is_active = False
        return self.storage.update_task(task_id, task)

    def _calculate_next_due_date(self, start_date: datetime, pattern: str, interval: int) -> datetime:
        """
        Calculate the next due date based on the recurrence pattern and interval.

        Args:
            start_date: Starting date for calculation
            pattern: Recurrence pattern ("daily", "weekly", "monthly")
            interval: Recurrence interval (number of units)

        Returns:
            Calculated next due date
        """
        return calculate_next_due_date(start_date, pattern, interval)

    def get_recurring_tasks(self) -> List[Task]:
        """
        Get all recurring tasks.

        Returns:
            List of all recurring tasks
        """
        all_tasks = self.storage.get_all_tasks()
        return [task for task in all_tasks if task.is_recurring]

    def handle_overdue_recurring_tasks(self) -> List[Task]:
        """
        Identify and handle overdue recurring tasks.

        Returns:
            List of overdue recurring tasks
        """
        from datetime import datetime
        all_tasks = self.storage.get_all_tasks()
        overdue_tasks = []

        for task in all_tasks:
            if (task.is_recurring and
                task.is_active and
                task.next_due_date and
                task.next_due_date < datetime.now() and
                not task.completed):
                overdue_tasks.append(task)

        return overdue_tasks

    def handle_mid_cycle_changes(self, task_id: int, recurrence_pattern: Optional[str] = None,
                                recurrence_interval: Optional[int] = None,
                                is_active: Optional[bool] = None) -> bool:
        """
        Handle changes to recurrence settings mid-cycle.

        Args:
            task_id: ID of the task to update
            recurrence_pattern: New recurrence pattern (optional)
            recurrence_interval: New recurrence interval (optional)
            is_active: New active status (optional)

        Returns:
            Boolean indicating success
        """
        task = self.storage.get_task(task_id)
        if not task or not task.is_recurring:
            return False

        # Update fields if provided
        if recurrence_pattern is not None:
            if recurrence_pattern not in ["daily", "weekly", "monthly"]:
                raise ValueError("Recurrence pattern must be 'daily', 'weekly', or 'monthly'")
            task.recurrence_pattern = recurrence_pattern

        if recurrence_interval is not None:
            if recurrence_interval <= 0:
                raise ValueError("Recurrence interval must be a positive integer")
            task.recurrence_interval = recurrence_interval

        if is_active is not None:
            task.is_active = is_active

        # Validate the updated task
        try:
            task.validate()
        except ValueError as e:
            raise ValueError(f"Invalid task data after update: {e}")

        # Update the task in storage
        return self.storage.update_task(task_id, task)

    def handle_task_completion(self, task: Task) -> Optional[Task]:
        """
        Handle the completion of a task, generating a new instance if it's recurring.

        Args:
            task: The task being completed

        Returns:
            New task instance if generated, None otherwise
        """
        if not task.is_recurring or not task.is_active:
            return None

        # Mark the current task as completed
        task.completed = True
        self.storage.update_task(task.id, task)

        # Generate the next instance
        return self.generate_next_instance(task)

    def perform_data_integrity_check(self) -> dict:
        """
        Perform data integrity checks on recurring tasks.

        Returns:
            Dictionary with integrity check results
        """
        all_tasks = self.storage.get_all_tasks()
        issues = []
        valid_count = 0

        for task in all_tasks:
            # Check if recurring task has valid recurrence settings
            if task.is_recurring:
                if task.recurrence_pattern not in ["daily", "weekly", "monthly"]:
                    issues.append(f"Task {task.id}: Invalid recurrence pattern '{task.recurrence_pattern}'")

                if task.recurrence_interval is not None and task.recurrence_interval <= 0:
                    issues.append(f"Task {task.id}: Invalid recurrence interval '{task.recurrence_interval}'")

                # Check for circular references in parent/child relationships
                if task.parent_id and task.id == task.parent_id:
                    issues.append(f"Task {task.id}: Circular reference - task is its own parent")

                # Check if original_task_id is valid
                if task.original_task_id and task.original_task_id != task.id:
                    original_task = self.storage.get_task(task.original_task_id)
                    if original_task and not original_task.is_recurring:
                        issues.append(f"Task {task.id}: Original task {task.original_task_id} is not recurring")

                valid_count += 1
            else:
                # Non-recurring tasks should not have recurrence-related fields set incorrectly
                if (task.recurrence_pattern or task.recurrence_interval or
                    task.next_due_date or task.parent_id or task.original_task_id):
                    # This might be okay if the fields are set but is_recurring is False
                    # We'll just note this as informational
                    pass

        return {
            "total_recurring_tasks": len([t for t in all_tasks if t.is_recurring]),
            "valid_recurring_tasks": valid_count,
            "integrity_issues": issues,
            "has_issues": len(issues) > 0
        }

    def prevent_duplicate_generation(self, original_task_id: int, next_due_date: datetime) -> bool:
        """
        Check if a duplicate task already exists for the same original task and due date.

        Args:
            original_task_id: ID of the original recurring task
            next_due_date: The next due date to check

        Returns:
            Boolean indicating if a duplicate exists (True) or not (False)
        """
        all_tasks = self.storage.get_all_tasks()

        for task in all_tasks:
            # Check if this is a recurring task instance with the same original_task_id
            # and similar next_due_date (within a small time window to account for timing differences)
            if (task.original_task_id == original_task_id and
                task.next_due_date and
                abs((task.next_due_date - next_due_date).total_seconds()) < 60):  # Within 1 minute
                return True

        return False