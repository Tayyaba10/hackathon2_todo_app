"""
Task entity for the todo application.

This module contains the Task entity that represents a user task in the todo application.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a user task in the todo application.

    Attributes:
        id (int): Unique identifier for the task, automatically assigned
        title (str): Required title of the task
        description (str): Optional description of the task
        completed (bool): Status indicating whether the task is completed (default: False)
        created_at (datetime): Timestamp when the task was created
        is_recurring (bool): Indicates if the task is part of a recurring series (default: False)
        recurrence_pattern (Optional[str]): Interval type ("daily", "weekly", "monthly") for recurring tasks
        recurrence_interval (Optional[int]): Number of units for the interval (default: 1)
        next_due_date (Optional[datetime]): When the next instance is due (for recurring tasks)
        is_active (bool): Whether recurrence is currently active (default: True for recurring tasks)
        parent_id (Optional[int]): For child instances, identifies the original recurring task
        original_task_id (Optional[int]): For any instance, identifies the original recurring task template
    """
    id: int
    title: str
    description: Optional[str] = ""
    completed: bool = False
    created_at: datetime = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    next_due_date: Optional[datetime] = None
    is_active: bool = True
    parent_id: Optional[int] = None
    original_task_id: Optional[int] = None

    def __post_init__(self):
        """Initialize the created_at field if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()

        # Set default recurrence interval to 1 if recurring and not specified
        if self.is_recurring and self.recurrence_interval is None:
            self.recurrence_interval = 1

    def validate(self) -> None:
        """
        Validate the task fields.

        Raises:
            ValueError: If title is empty or None, or if recurring task has invalid pattern
        """
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty or None")

        # Validate recurrence fields if task is recurring
        if self.is_recurring:
            if self.recurrence_pattern not in ["daily", "weekly", "monthly"]:
                raise ValueError("Recurrence pattern must be 'daily', 'weekly', or 'monthly'")

            if self.recurrence_interval is not None and self.recurrence_interval <= 0:
                raise ValueError("Recurrence interval must be a positive integer")