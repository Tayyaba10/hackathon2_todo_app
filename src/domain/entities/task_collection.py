"""
TaskCollection entity for the todo application.

This module contains the TaskCollection entity that manages a collection of tasks.
"""
from typing import Dict, List
from src.domain.entities.task import Task


class TaskCollection:
    """
    Represents a collection of tasks managed by the application.

    Attributes:
        tasks (dict): Dictionary mapping task IDs to Task objects
        next_id (int): Counter for generating unique task IDs
    """

    def __init__(self):
        """Initialize an empty task collection with ID counter."""
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def add_task(self, task: Task) -> int:
        """
        Add a task to the collection.

        Args:
            task: Task object to add

        Returns:
            Integer ID of the added task

        Raises:
            ValueError: If task ID already exists in the collection
        """
        if task.id in self.tasks:
            raise ValueError(f"Task with ID {task.id} already exists in collection")

        # If task ID is 0 or negative, assign a new ID
        if task.id <= 0:
            task.id = self.next_id
            self.next_id += 1

        self.tasks[task.id] = task
        return task.id

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task from the collection by ID.

        Args:
            task_id: Integer ID of the task to retrieve

        Returns:
            Task object if found

        Raises:
            KeyError: If task with given ID doesn't exist
        """
        if task_id not in self.tasks:
            raise KeyError(f"Task with ID {task_id} not found")
        return self.tasks[task_id]

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the collection.

        Returns:
            List of all Task objects in the collection
        """
        return list(self.tasks.values())

    def update_task(self, task_id: int, updated_task: Task) -> bool:
        """
        Update a task in the collection.

        Args:
            task_id: Integer ID of the task to update
            updated_task: Updated Task object

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        if task_id not in self.tasks:
            return False

        # Preserve the original ID
        updated_task.id = task_id
        self.tasks[task_id] = updated_task
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the collection.

        Args:
            task_id: Integer ID of the task to delete

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        if task_id not in self.tasks:
            return False

        del self.tasks[task_id]
        return True

    def validate_unique_id(self, task_id: int) -> bool:
        """
        Check if a task ID is unique in the collection.

        Args:
            task_id: Integer ID to check

        Returns:
            Boolean indicating if ID is unique (True) or exists (False)
        """
        return task_id not in self.tasks