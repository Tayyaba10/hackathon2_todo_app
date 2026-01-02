#!/usr/bin/env python3
"""
CLI interface for the Todo application with organizational features.

This module provides a command-line interface for managing tasks with
priority, tags, search, filter, and sort capabilities.
"""

import argparse
import sys
from datetime import datetime
from typing import List, Optional
from src.services.todo_service import TodoService, FilterCriteria, SortCriteria
from src.models.priority import Priority


class TodoCLI:
    """
    Command-line interface for the Todo application.
    """

    def __init__(self):
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()

    def run(self):
        """Run the main CLI loop."""
        parser = argparse.ArgumentParser(
            description="Todo application with organizational features"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add task command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("title", help="Title of the task")
        add_parser.add_argument("--description", "-d", help="Description of the task")
        add_parser.add_argument(
            "--priority", "-p",
            choices=["high", "medium", "low"],
            help="Priority level of the task"
        )
        add_parser.add_argument(
            "--tags", "-t",
            nargs="*",
            help="Tags for the task (space-separated)"
        )
        add_parser.add_argument(
            "--due-date",
            help="Due date for the task (format: YYYY-MM-DD)"
        )

        # Add recurring task command
        add_recurring_parser = subparsers.add_parser("add-recurring", help="Add a new recurring task")
        add_recurring_parser.add_argument("title", help="Title of the recurring task")
        add_recurring_parser.add_argument("--description", "-d", help="Description of the task")
        add_recurring_parser.add_argument(
            "--pattern", "-p",
            required=True,
            choices=["daily", "weekly", "monthly"],
            help="Recurrence pattern for the task (required)"
        )
        add_recurring_parser.add_argument(
            "--interval", "-i",
            type=int,
            default=1,
            help="Recurrence interval (number of units, default: 1)"
        )

        # List tasks command
        list_parser = subparsers.add_parser("list", help="List all tasks")
        list_parser.add_argument(
            "--status",
            choices=["completed", "pending"],
            help="Filter tasks by completion status"
        )
        list_parser.add_argument(
            "--priority",
            choices=["high", "medium", "low"],
            help="Filter tasks by priority"
        )
        list_parser.add_argument(
            "--tag",
            help="Filter tasks by tag"
        )
        list_parser.add_argument(
            "--sort",
            choices=["title", "priority", "date", "creation"],
            help="Sort tasks by specified criteria"
        )
        list_parser.add_argument(
            "--search",
            help="Search tasks by keyword"
        )

        # Update task command
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("id", type=int, help="ID of the task to update")
        update_parser.add_argument("--title", help="New title for the task")
        update_parser.add_argument("--description", "-d", help="New description for the task")
        update_parser.add_argument("--completed", action="store_true", help="Mark task as completed")
        update_parser.add_argument("--not-completed", action="store_true", help="Mark task as not completed")

        # Set priority command
        priority_parser = subparsers.add_parser("priority", help="Set priority for a task")
        priority_parser.add_argument("id", type=int, help="ID of the task")
        priority_parser.add_argument(
            "priority",
            choices=["high", "medium", "low"],
            help="Priority level to set"
        )

        # Add tag command
        add_tag_parser = subparsers.add_parser("add-tag", help="Add a tag to a task")
        add_tag_parser.add_argument("id", type=int, help="ID of the task")
        add_tag_parser.add_argument("tag", help="Tag to add to the task")

        # Remove tag command
        remove_tag_parser = subparsers.add_parser("remove-tag", help="Remove a tag from a task")
        remove_tag_parser.add_argument("id", type=int, help="ID of the task")
        remove_tag_parser.add_argument("tag", help="Tag to remove from the task")

        # Complete task command
        complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
        complete_parser.add_argument("id", type=int, help="ID of the task to complete")

        # Delete task command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("id", type=int, help="ID of the task to delete")

        # Update recurrence settings command
        update_recurrence_parser = subparsers.add_parser("update-recurrence", help="Update recurrence settings")
        update_recurrence_parser.add_argument("id", type=int, help="ID of the recurring task")
        update_recurrence_parser.add_argument(
            "--pattern", "-p",
            choices=["daily", "weekly", "monthly"],
            help="New recurrence pattern"
        )
        update_recurrence_parser.add_argument(
            "--interval", "-i",
            type=int,
            help="New recurrence interval"
        )
        update_recurrence_parser.add_argument(
            "--active", "-a",
            choices=["true", "false"],
            help="Set active status (true/false)"
        )

        # Cancel recurrence command
        cancel_recurrence_parser = subparsers.add_parser("cancel-recurrence", help="Cancel recurrence for a task")
        cancel_recurrence_parser.add_argument("id", type=int, help="ID of the recurring task to cancel")

        # Show recurrence settings command
        show_recurrence_parser = subparsers.add_parser("show-recurrence", help="Show recurrence settings for a task")
        show_recurrence_parser.add_argument("id", type=int, help="ID of the task to show recurrence settings for")

        # Parse arguments
        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        # Execute the appropriate command
        try:
            if args.command == "add":
                self.add_task(args)
            elif args.command == "add-recurring":
                self.add_recurring_task(args)
            elif args.command == "list":
                self.list_tasks(args)
            elif args.command == "update":
                self.update_task(args)
            elif args.command == "priority":
                self.set_priority(args)
            elif args.command == "add-tag":
                self.add_tag(args)
            elif args.command == "remove-tag":
                self.remove_tag(args)
            elif args.command == "complete":
                self.complete_task(args)
            elif args.command == "delete":
                self.delete_task(args)
            elif args.command == "update-recurrence":
                self.update_recurrence_settings(args)
            elif args.command == "cancel-recurrence":
                self.cancel_recurrence(args)
            elif args.command == "show-recurrence":
                self.show_recurrence_settings(args)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def add_task(self, args):
        """Add a new task."""
        # Parse priority if provided
        priority = None
        if args.priority:
            priority = Priority(args.priority)

        # Parse due date if provided
        due_date = None
        if args.due_date:
            try:
                due_date = datetime.strptime(args.due_date, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD", file=sys.stderr)
                return

        # Create task
        task = self.service.create_task(
            title=args.title,
            description=args.description or "",
            priority=priority,
            tags=args.tags,
            due_date=due_date
        )
        print(f"Task added with ID {task.id}: {task.title}")

    def add_recurring_task(self, args):
        """Add a new recurring task."""
        # Use the domain service from the TodoService to ensure shared storage
        domain_service = self.service.domain_service

        task = domain_service.create_recurring_task(
            title=args.title,
            description=args.description or "",
            recurrence_pattern=args.pattern,
            recurrence_interval=args.interval
        )
        print(f"Recurring task added with ID {task.id}: {task.title}")
        print(f"Recurrence pattern: {task.recurrence_pattern}, interval: {task.recurrence_interval}")

    def list_tasks(self, args):
        """List tasks with optional filtering and sorting."""
        # Get all tasks (regular and recurring) using the unified service method
        all_tasks = self.service.get_all_tasks_with_recurring()

        # Apply search if provided
        if args.search:
            # Filter tasks based on search query
            search_results = []
            for task in all_tasks:
                # Check if the task title or description contains the search term
                task_title = getattr(task, 'title', '')
                task_description = getattr(task, 'description', '')
                if (args.search.lower() in task_title.lower() or
                    args.search.lower() in task_description.lower()):
                    search_results.append(task)
            all_tasks = search_results

        # Apply filters if provided
        filtered_tasks = []
        for task in all_tasks:
            include_task = True

            # Apply status filter
            if args.status:
                if args.status == "completed" and not task.completed:
                    include_task = False
                elif args.status == "pending" and task.completed:
                    include_task = False

            # Apply priority filter (only for models layer tasks that have priority)
            if args.priority and hasattr(task, 'priority'):
                priority_enum = Priority(args.priority)
                if task.priority != priority_enum:
                    include_task = False

            # Apply tag filter (only for models layer tasks that have tags)
            if args.tag and hasattr(task, 'tags'):
                tag_lower = args.tag.strip().lower()
                if tag_lower not in task.tags:
                    include_task = False

            if include_task:
                filtered_tasks.append(task)

        all_tasks = filtered_tasks

        # Apply sorting if specified
        if args.sort:
            sort_by = self._get_sort_criteria(args.sort)
            # For now, we'll just use basic sorting based on attributes
            if sort_by == "title_alphabetical":
                all_tasks = sorted(all_tasks, key=lambda t: getattr(t, 'title', '').lower())
            elif sort_by == "creation_date":
                all_tasks = sorted(all_tasks, key=lambda t: getattr(t, 'created_at', datetime.min), reverse=True)

        # Display tasks
        if not all_tasks:
            print("No tasks found.")
        else:
            # Use the domain service from the TodoService to ensure shared storage
            domain_service = self.service.domain_service

            for task in all_tasks:
                # Check if this is a domain task (has is_recurring attribute) or a model task
                if hasattr(task, 'is_recurring') and task.is_recurring:
                    # This is a recurring task from the domain layer
                    display_info = domain_service.get_task_display_info(task)
                    print(display_info)
                else:
                    # This is a regular task from the models layer
                    print(task)

    def _get_sort_criteria(self, sort_arg: str) -> str:
        """Convert CLI sort argument to SortCriteria."""
        if sort_arg == "title":
            return SortCriteria.TITLE_ALPHABETICAL
        elif sort_arg == "priority":
            return SortCriteria.PRIORITY
        elif sort_arg == "date":
            return SortCriteria.DUE_DATE
        elif sort_arg == "creation":
            return SortCriteria.CREATION_DATE
        else:
            return SortCriteria.TITLE_ALPHABETICAL  # Default

    def update_task(self, args):
        """Update a task."""
        completed = None
        if args.completed:
            completed = True
        elif args.not_completed:
            completed = False

        task = self.service.update_task(
            task_id=args.id,
            title=args.title,
            description=args.description,
            completed=completed
        )
        if task:
            print(f"Task {args.id} updated: {task.title}")
        else:
            print(f"Task {args.id} not found.")

    def set_priority(self, args):
        """Set priority for a task."""
        priority = Priority(args.priority)
        task = self.service.set_priority(args.id, priority)
        if task:
            print(f"Priority set to {task.priority.value} for task {args.id}: {task.title}")
        else:
            print(f"Task {args.id} not found.")

    def add_tag(self, args):
        """Add a tag to a task."""
        task = self.service.add_tag(args.id, args.tag)
        if task:
            print(f"Tag '{args.tag}' added to task {args.id}: {task.title}")
        else:
            print(f"Task {args.id} not found.")

    def remove_tag(self, args):
        """Remove a tag from a task."""
        task = self.service.remove_tag(args.id, args.tag)
        if task:
            print(f"Tag '{args.tag}' removed from task {args.id}: {task.title}")
        else:
            print(f"Task {args.id} not found.")

    def complete_task(self, args):
        """Mark a task as completed, with special handling for recurring tasks."""
        # First try to complete as a regular task
        task = self.service.update_task(args.id, completed=True)

        if task:
            print(f"Task {args.id} marked as completed: {task.title}")
        else:
            # If not found in regular tasks, check if it's a recurring task
            # Use the domain service from the TodoService to ensure shared storage
            domain_service = self.service.domain_service

            # Try to complete the task via the domain service
            completed_task = domain_service.complete_task(args.id)

            if completed_task:
                print(f"Recurring task {args.id} marked as completed: {completed_task.title}")

                # Check if this was a recurring task and if a new instance was generated
                if completed_task.is_recurring and completed_task.is_active:
                    # The recurring service would have already generated the next instance
                    # Find the next instance from storage
                    all_tasks = self.service.domain_storage.get_all_tasks()
                    next_instance = None
                    for task in all_tasks:
                        if (hasattr(task, 'parent_id') and task.parent_id == args.id and
                            not task.completed and task.is_recurring):
                            next_instance = task
                            break
                    if next_instance:
                        print(f"Next instance of recurring task has been scheduled for {next_instance.next_due_date}.")
                    else:
                        print(f"Next instance of recurring task has been scheduled.")
            else:
                print(f"Task {args.id} not found in regular or recurring tasks.")

    def delete_task(self, args):
        """Delete a task."""
        success = self.service.delete_task(args.id)
        if success:
            print(f"Task {args.id} deleted.")
        else:
            print(f"Task {args.id} not found.")

    def update_recurrence_settings(self, args):
        """Update recurrence settings for a recurring task."""
        # Use the domain service from the TodoService to ensure shared storage
        domain_service = self.service.domain_service

        # Convert active argument to boolean
        is_active = None
        if args.active:
            is_active = args.active.lower() == "true"

        success = domain_service.update_recurrence_settings(
            task_id=args.id,
            recurrence_pattern=args.pattern,
            recurrence_interval=args.interval,
            is_active=is_active
        )

        if success:
            print(f"Recurrence settings updated for task {args.id}")
            # Get and display the updated task
            updated_task = domain_service.get_task(args.id)
            if updated_task and updated_task.is_recurring:
                print(f"Pattern: {updated_task.recurrence_pattern}, Interval: {updated_task.recurrence_interval}, Active: {updated_task.is_active}")
        else:
            print(f"Failed to update recurrence settings for task {args.id}")

    def cancel_recurrence(self, args):
        """Cancel recurrence for a recurring task."""
        # Use the domain service from the TodoService to ensure shared storage
        domain_service = self.service.domain_service

        success = domain_service.cancel_recurrence(args.id)

        if success:
            print(f"Recurrence canceled for task {args.id}")
        else:
            print(f"Failed to cancel recurrence for task {args.id} (not a recurring task or already canceled)")

    def show_recurrence_settings(self, args):
        """Show recurrence settings for a task."""
        # Use the domain service from the TodoService to ensure shared storage
        domain_service = self.service.domain_service

        task = domain_service.get_task(args.id)

        if not task:
            print(f"Task {args.id} not found.")
            return

        if not task.is_recurring:
            print(f"Task {args.id} is not a recurring task.")
            return

        print(f"Recurrence settings for task {args.id}:")
        print(f"  Title: {task.title}")
        print(f"  Pattern: {task.recurrence_pattern}")
        print(f"  Interval: {task.recurrence_interval}")
        print(f"  Active: {task.is_active}")
        if task.next_due_date:
            print(f"  Next due date: {task.next_due_date.strftime('%Y-%m-%d %H:%M:%S')}")
        if task.parent_id:
            print(f"  Parent task ID: {task.parent_id}")
        if task.original_task_id and task.original_task_id != task.id:
            print(f"  Original task ID: {task.original_task_id}")


def main():
    """Main entry point for the CLI."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()