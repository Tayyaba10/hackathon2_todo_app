"""
Domain exceptions for the todo application.

This module contains custom exceptions for the domain layer.
"""


class TodoException(Exception):
    """Base exception for todo application domain errors."""
    pass


class InvalidTaskError(TodoException):
    """Raised when a task is invalid (e.g., empty title)."""
    pass


class TaskNotFoundError(TodoException):
    """Raised when a task with a given ID is not found."""
    pass