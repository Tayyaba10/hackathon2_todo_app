from datetime import datetime
from typing import List, Optional
from .priority import Priority


class Task:
    """
    Represents a user task with additional organizational features.

    Attributes:
        id (int): Unique identifier for the task
        title (str): Title of the task
        description (str): Detailed description of the task
        completed (bool): Completion status of the task
        priority (Priority): Task priority level
        tags (List[str]): List of tags associated with the task
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
        due_date (Optional[datetime]): Optional due date
    """

    def __init__(
        self,
        id: int,
        title: str,
        description: str = "",
        completed: bool = False,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        due_date: Optional[datetime] = None
    ):
        """
        Initialize a Task instance.

        Args:
            id: Unique identifier for the task
            title: Title of the task
            description: Detailed description of the task
            completed: Completion status of the task
            priority: Task priority level (defaults to MEDIUM)
            tags: List of tags associated with the task (defaults to empty list)
            created_at: Creation timestamp (defaults to now)
            updated_at: Last update timestamp (defaults to now)
            due_date: Optional due date
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority if priority is not None else Priority.MEDIUM
        self.tags = tags if tags is not None else []
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
        self.due_date = due_date

    def add_tag(self, tag: str) -> None:
        """
        Add a tag to the task.

        Args:
            tag: Tag to add to the task

        Raises:
            ValueError: If tag is empty or already exists
        """
        if not tag or not tag.strip():
            raise ValueError("Tag cannot be empty or whitespace only")

        tag = tag.strip().lower()
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
        else:
            raise ValueError(f"Tag '{tag}' already exists on this task")

    def remove_tag(self, tag: str) -> None:
        """
        Remove a tag from the task.

        Args:
            tag: Tag to remove from the task

        Raises:
            ValueError: If tag does not exist
        """
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
        else:
            raise ValueError(f"Tag '{tag}' does not exist on this task")

    def set_priority(self, priority: Priority) -> None:
        """
        Set the priority of the task.

        Args:
            priority: New priority level for the task
        """
        if not isinstance(priority, Priority):
            raise TypeError("Priority must be a Priority enum value")

        self.priority = priority
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """
        Convert the Task instance to a dictionary.

        Returns:
            dict: Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority.value,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None
        }

    def __str__(self) -> str:
        """Return a string representation of the task."""
        status = "✓" if self.completed else "○"
        priority_str = self.priority.value.upper()
        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        due_str = f" (due: {self.due_date.strftime('%Y-%m-%d')})" if self.due_date else ""

        return f"{status} [{priority_str}] {self.title}{tags_str}{due_str}"

    def __repr__(self) -> str:
        """Return a detailed string representation of the task."""
        return (f"Task(id={self.id}, title='{self.title}', completed={self.completed}, "
                f"priority={self.priority}, tags={self.tags})")

    def __eq__(self, other) -> bool:
        """Check equality with another Task instance."""
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Return hash value for the task."""
        return hash(self.id)