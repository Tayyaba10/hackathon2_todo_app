"""
Storage interface for the todo application.

This module defines the interface for storage implementations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.task import Task


class StorageInterface(ABC):
    """
    Interface for storage implementations in the todo application.

    This interface defines the contract that all storage implementations must follow.
    """

    @abstractmethod
    def save_task(self, task: Task) -> int:
        """
        Save a task to storage.

        Args:
            task: Task object to save

        Returns:
            Integer ID of the saved task
        """
        pass

    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task from storage by ID.

        Args:
            task_id: Integer ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from storage.

        Returns:
            List of all Task objects in storage
        """
        pass

    @abstractmethod
    def update_task(self, task_id: int, updated_task: Task) -> bool:
        """
        Update a task in storage.

        Args:
            task_id: Integer ID of the task to update
            updated_task: Updated Task object

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from storage.

        Args:
            task_id: Integer ID of the task to delete

        Returns:
            Boolean indicating success (True) or failure (False)
        """
        pass