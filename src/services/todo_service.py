import sys
from datetime import datetime
from typing import List, Optional, Dict, Any
from src.models.task import Task
from src.models.priority import Priority
from .search_service import SearchService

# Import domain layer components for recurring tasks
from src.domain.entities.task import Task as DomainTask
from src.infrastructure.storage.in_memory_storage import InMemoryStorage
from src.services.recurring_service import RecurringTaskService
from src.services.domain_todo_service import DomainTodoService


class FilterCriteria:
    """
    Defines filter parameters for task filtering.

    Fields:
    - status: Filter by completion status
    - priority: Filter by priority level
    - tag: Filter by specific tag
    - due_date: Filter by due date
    """
    def __init__(
        self,
        status: Optional[bool] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None,
        due_date: Optional[datetime] = None
    ):
        self.status = status
        self.priority = priority
        self.tag = tag
        self.due_date = due_date


class SortCriteria:
    """
    Defines sorting parameters for task sorting.

    Options:
    - TITLE_ALPHABETICAL: Sort by title alphabetically
    - PRIORITY: Sort by priority (high to low)
    - DUE_DATE: Sort by due date (earliest first)
    - CREATION_DATE: Sort by creation date (newest first)
    """
    TITLE_ALPHABETICAL = "title_alphabetical"
    PRIORITY = "priority"
    DUE_DATE = "due_date"
    CREATION_DATE = "creation_date"


class TodoService:
    """
    Extended service to handle new organizational features.

    New Methods:
    - set_priority(task_id: int, priority: Priority) -> Task
    - add_tag(task_id: int, tag: str) -> Task
    - remove_tag(task_id: int, tag: str) -> Task
    - search_tasks(query: str) -> List[Task]
    - filter_tasks(filters: TaskFilters) -> List[Task]
    - sort_tasks(tasks: List[Task], sort_by: SortCriteria) -> List[Task]
    """

    def __init__(self):
        """Initialize the TodoService with an empty task list and SearchService."""
        self.tasks: List[Task] = []
        self.search_service = SearchService()
        self._next_id = 1

        # Initialize domain layer components for recurring tasks
        self.domain_storage = InMemoryStorage()
        self.domain_service = DomainTodoService(self.domain_storage)
        self.recurring_service = RecurringTaskService(self.domain_storage)

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        due_date: Optional[datetime] = None
    ) -> Task:
        """
        Create a new task.

        Args:
            title: Title of the task
            description: Description of the task
            priority: Priority level of the task
            tags: List of tags for the task
            due_date: Due date for the task

        Returns:
            Created Task instance
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date
        )
        self.tasks.append(task)
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task instance if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks (both regular and recurring).

        Returns:
            List of all tasks
        """
        # Get regular tasks
        all_tasks = self.tasks.copy()

        # Get recurring tasks from domain layer and convert them to models layer format if needed
        # For now, we'll return both lists combined
        return all_tasks

    def get_all_tasks_with_recurring(self) -> List:
        """
        Get all tasks including recurring tasks from domain layer.

        Returns:
            List of all tasks (regular + recurring)
        """
        # Get regular tasks
        regular_tasks = self.tasks.copy()

        # Get recurring tasks from domain storage
        recurring_tasks = self.domain_storage.get_all_tasks()

        # Return both lists combined
        return regular_tasks + recurring_tasks

    def get_all_mixed_tasks(self) -> List:
        """
        Alternative method to get all tasks (regular + recurring) with proper indication.

        Returns:
            List of all tasks (regular + recurring)
        """
        # Get regular tasks
        regular_tasks = self.tasks.copy()

        # Get recurring tasks from domain storage
        recurring_tasks = self.domain_storage.get_all_tasks()

        # Return both lists combined
        return regular_tasks + recurring_tasks

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

        task.updated_at = datetime.now()
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if not found
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def set_priority(self, task_id: int, priority: Priority) -> Optional[Task]:
        """
        Set priority for a task.

        Args:
            task_id: ID of the task to update
            priority: New priority level

        Returns:
            Updated Task instance if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.set_priority(priority)
            return task
        return None

    def add_tag(self, task_id: int, tag: str) -> Optional[Task]:
        """
        Add a tag to a task.

        Args:
            task_id: ID of the task to update
            tag: Tag to add

        Returns:
            Updated Task instance if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.add_tag(tag)
            return task
        return None

    def remove_tag(self, task_id: int, tag: str) -> Optional[Task]:
        """
        Remove a tag from a task.

        Args:
            task_id: ID of the task to update
            tag: Tag to remove

        Returns:
            Updated Task instance if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.remove_tag(tag)
            return task
        return None

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title/description.

        Args:
            query: Search query string

        Returns:
            List of matching tasks
        """
        try:
            return self.search_service.search_by_keyword_safe(self.tasks, query)
        except Exception as e:
            # Log error if needed and return empty list
            print(f"Search error: {e}", file=sys.stderr)
            return []

    def filter_tasks(self, filters: FilterCriteria) -> List[Task]:
        """
        Filter tasks by criteria.

        Args:
            filters: FilterCriteria object with filter parameters

        Returns:
            List of tasks matching the filter criteria
        """
        filtered_tasks = self.tasks.copy()

        # Filter by status (completed/incomplete)
        if filters.status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.completed == filters.status]

        # Filter by priority
        if filters.priority is not None:
            filtered_tasks = [task for task in filtered_tasks if task.priority == filters.priority]

        # Filter by tag
        if filters.tag is not None:
            tag = filters.tag.strip().lower()
            filtered_tasks = [task for task in filtered_tasks if tag in task.tags]

        # Filter by due date
        if filters.due_date is not None:
            filtered_tasks = [task for task in filtered_tasks
                             if task.due_date and task.due_date.date() == filters.due_date.date()]

        return filtered_tasks

    def sort_tasks(self, tasks: List[Task], sort_by: str) -> List[Task]:
        """
        Sort tasks based on the specified criteria.

        Args:
            tasks: List of tasks to sort
            sort_by: Sort criteria (from SortCriteria)

        Returns:
            List of sorted tasks
        """
        if not tasks:
            return tasks

        if sort_by == SortCriteria.TITLE_ALPHABETICAL:
            # Sort alphabetically by title (case-insensitive)
            return sorted(tasks, key=lambda task: task.title.lower())
        elif sort_by == SortCriteria.PRIORITY:
            # Sort by priority (high to low)
            # Using the order of enum values: HIGH > MEDIUM > LOW
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            return sorted(tasks, key=lambda task: priority_order[task.priority])
        elif sort_by == SortCriteria.DUE_DATE:
            # Sort by due date (earliest first), with tasks without due dates at the end
            return sorted(tasks, key=lambda task: (task.due_date is None, task.due_date))
        elif sort_by == SortCriteria.CREATION_DATE:
            # Sort by creation date (newest first)
            return sorted(tasks, key=lambda task: task.created_at, reverse=True)
        else:
            # Default: return as is
            return tasks.copy()

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """
        Get all tasks with a specific priority.

        Args:
            priority: Priority level to filter by

        Returns:
            List of tasks with the specified priority
        """
        return [task for task in self.tasks if task.priority == priority]

    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """
        Get all tasks with a specific tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of tasks with the specified tag
        """
        tag = tag.strip().lower()
        return [task for task in self.tasks if tag in task.tags]

    def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks.

        Returns:
            List of completed tasks
        """
        return [task for task in self.tasks if task.completed]

    def get_pending_tasks(self) -> List[Task]:
        """
        Get all pending (not completed) tasks.

        Returns:
            List of pending tasks
        """
        return [task for task in self.tasks if not task.completed]

    def create_recurring_task(
        self,
        title: str,
        description: str = "",
        recurrence_pattern: str = "daily",
        recurrence_interval: int = 1
    ) -> DomainTask:
        """
        Create a new recurring task using the domain layer.

        Args:
            title: Title of the task
            description: Description of the task
            recurrence_pattern: Pattern for recurrence ("daily", "weekly", "monthly")
            recurrence_interval: Interval for recurrence (number of units)

        Returns:
            Created recurring DomainTask instance
        """
        return self.domain_service.create_recurring_task(
            title=title,
            description=description,
            recurrence_pattern=recurrence_pattern,
            recurrence_interval=recurrence_interval
        )

    def complete_task_with_recurring_logic(self, task_id: int) -> Optional[DomainTask]:
        """
        Complete a task and handle recurring task logic.

        Args:
            task_id: ID of the task to complete

        Returns:
            Completed task if found, None otherwise
        """
        task = self.domain_service.get_task(task_id)
        if not task:
            return None

        return self.domain_service.complete_task(task_id)