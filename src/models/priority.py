from enum import Enum
from typing import Union


class Priority(str, Enum):
    """
    Enum representing the priority levels for tasks.

    Values:
    - HIGH: High priority tasks
    - MEDIUM: Medium priority tasks
    - LOW: Low priority tasks
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    def __str__(self) -> str:
        """Return the string representation of the priority."""
        return self.value

    @classmethod
    def from_string(cls, value: str) -> 'Priority':
        """
        Create a Priority instance from a string value.

        Args:
            value: String representation of the priority

        Returns:
            Priority: The corresponding Priority enum value

        Raises:
            ValueError: If the value is not a valid priority
        """
        try:
            return cls(value.lower())
        except ValueError:
            valid_values = [p.value for p in cls]
            raise ValueError(f"Invalid priority: {value}. Valid values are: {valid_values}")