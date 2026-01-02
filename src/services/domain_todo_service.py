"""
Domain service for handling todo operations using the domain layer.

This service works with the domain Task entity and storage interface.
"""
from datetime import datetime
from typing import List, Optional
from src.domain.entities.task import Task
from src.domain.entities.task_collection import TaskCollection
from src.infrastructure.storage.in_memory_storage import InMemoryStorage


class DomainTodoService:
    """
    Service for handling todo operations using the domain layer.

    This service works with the domain Task entity and storage interface.
    """

    def __init__(self, storage=None):
        """
        Initialize the DomainTodoService.

        Args:
            storage: Storage interface for task persistence. If None, uses InMemoryStorage.
        """
        self.storage = storage if storage is not None else InMemoryStorage()

    def create_task(
        self,
        title: str,
        description: str = "",
        is_recurring: bool = False,
        recurrence_pattern: Optional[str] = None,
        recurrence_interval: Optional[int] = None
    ) -> Task:
        """
        Create a new task.

        Args:
            title: Title of the task
            description: Description of the task
            is_recurring: Whether the task is recurring
            recurrence_pattern: Pattern for recurrence ("daily", "weekly", "monthly")
            recurrence_interval: Interval for recurrence (number of units)

        Returns:
            Created Task instance
        """
        task = Task(
            id=0,  # Will be assigned by storage
            title=title,
            description=description,
            is_recurring=is_recurring,
            recurrence_pattern=recurrence_pattern,
            recurrence_interval=recurrence_interval
        )

        # Calculate next due date if recurring
        if is_recurring and recurrence_pattern and recurrence_interval:
            from src.lib.utils import calculate_next_due_date
            task.next_due_date = calculate_next_due_date(
                datetime.now(),
                recurrence_pattern,
                recurrence_interval
            )

        task_id = self.storage.save_task(task)
        task.id = task_id

        # Update the original_task_id for recurring tasks
        if is_recurring:
            task.original_task_id = task_id
            self.storage.update_task(task_id, task)

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task instance if found, None otherwise
        """
        return self.storage.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks
        """
        return self.storage.get_all_tasks()

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Task]:
        """
        Update a task's basic properties.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            Updated Task instance if found, None otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        success = self.storage.update_task(task_id, task)
        return task if success else None

    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as completed and handle recurring task logic.

        Args:
            task_id: ID of the task to complete

        Returns:
            Completed task if found, None otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Mark as completed
        task.completed = True

        # Handle recurring task logic
        if task.is_recurring and task.is_active:
            # Import here to avoid circular imports
            from src.services.recurring_service import RecurringTaskService
            recurring_service = RecurringTaskService(self.storage)
            # This will generate the next instance if needed
            next_instance = recurring_service.handle_task_completion(task)

        success = self.storage.update_task(task_id, task)
        return task if success else None

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        return self.storage.delete_task(task_id)

    def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks.

        Returns:
            List of completed tasks
        """
        all_tasks = self.get_all_tasks()
        return [task for task in all_tasks if task.completed]

    def get_pending_tasks(self) -> List[Task]:
        """
        Get all pending (not completed) tasks.

        Returns:
            List of pending tasks
        """
        all_tasks = self.get_all_tasks()
        return [task for task in all_tasks if not task.completed]

    def get_task_display_info(self, task: Task) -> str:
        """
        Get a display string for a task with recurrence information if applicable.

        Args:
            task: Task to get display information for

        Returns:
            Formatted string with task information and recurrence indicators
        """
        status = "✓" if task.completed else "○"

        # Basic task info
        display_str = f"{status} {task.title}"

        # Add recurrence indicator if it's a recurring task
        if task.is_recurring:
            recurrence_info = f" [RECURRING: {task.recurrence_pattern}"
            if task.recurrence_interval and task.recurrence_interval > 1:
                recurrence_info += f" x{task.recurrence_interval}"
            recurrence_info += f", ACTIVE: {task.is_active}]"
            display_str += recurrence_info

        # Add due date if available
        if task.next_due_date:
            display_str += f" (due: {task.next_due_date.strftime('%Y-%m-%d')})"
        elif hasattr(task, 'due_date') and task.due_date:
            display_str += f" (due: {task.due_date.strftime('%Y-%m-%d')})"

        return display_str

    def create_recurring_task(
        self,
        title: str,
        description: str = "",
        recurrence_pattern: str = "daily",
        recurrence_interval: int = 1
    ) -> Task:
        """
        Create a new recurring task.

        Args:
            title: Title of the task
            description: Description of the task
            recurrence_pattern: Pattern for recurrence ("daily", "weekly", "monthly")
            recurrence_interval: Interval for recurrence (number of units)

        Returns:
            Created recurring Task instance
        """
        from src.services.recurring_service import RecurringTaskService
        recurring_service = RecurringTaskService(self.storage)
        return recurring_service.create_recurring_task(
            title=title,
            description=description,
            recurrence_pattern=recurrence_pattern,
            recurrence_interval=recurrence_interval
        )

    def update_recurrence_settings(
        self,
        task_id: int,
        recurrence_pattern: Optional[str] = None,
        recurrence_interval: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> bool:
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
        from src.services.recurring_service import RecurringTaskService
        recurring_service = RecurringTaskService(self.storage)
        return recurring_service.update_recurrence_settings(
            task_id,
            recurrence_pattern,
            recurrence_interval,
            is_active
        )

    def cancel_recurrence(self, task_id: int) -> bool:
        """
        Cancel recurrence for a recurring task.

        Args:
            task_id: ID of the task to cancel recurrence for

        Returns:
            Boolean indicating success
        """
        from src.services.recurring_service import RecurringTaskService
        recurring_service = RecurringTaskService(self.storage)
        return recurring_service.cancel_recurrence(task_id)