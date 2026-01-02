"""
In-memory storage implementation for the todo application.

This module contains the in-memory storage implementation that stores tasks during runtime.
"""
from typing import List, Optional
from src.domain.entities.task import Task
from src.domain.entities.task_collection import TaskCollection
from src.services.interfaces.storage_interface import StorageInterface


class InMemoryStorage(StorageInterface):
    """
    In-memory storage implementation for the todo application.

    This class implements the StorageInterface using in-memory storage that persists
    only during the runtime session.
    """

    def __init__(self):
        """Initialize the in-memory storage with an empty task collection."""
        self._task_collection = TaskCollection()

    def save_task(self, task: Task) -> int:
        """
        Save a task to in-memory storage.

        Args:
            task: Task object to save

        Returns:
            Integer ID of the saved task
        """
        # Validate the task before saving
        task.validate()
        return self._task_collection.add_task(task)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task from in-memory storage by ID.

        Args:
            task_id: Integer ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        try:
            return self._task_collection.get_task(task_id)
        except KeyError:
            return None

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from in-memory storage.

        Returns:
            List of all Task objects in storage
        """
        return self._task_collection.get_all_tasks()

    def update_task(self, task_id: int, updated_task: Task) -> bool:
        """
        Update a task in in-memory storage.

        Args:
            task_id: Integer ID of the task to update
            updated_task: Updated Task object

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        # Validate the updated task before saving
        updated_task.validate()
        return self._task_collection.update_task(task_id, updated_task)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from in-memory storage.

        Args:
            task_id: Integer ID of the task to delete

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        return self._task_collection.delete_task(task_id)