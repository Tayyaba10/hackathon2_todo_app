import pytest
import sys
from io import StringIO
from unittest.mock import patch, Mock
from src.cli.cli import TodoCLI
from src.models.priority import Priority


class TestTodoCLI:
    """Unit tests for the Todo CLI interface."""

    def setup_method(self):
        """Set up a fresh CLI instance for each test."""
        self.cli = TodoCLI()
        # Clear any existing tasks to ensure test isolation
        self.cli.service.tasks = []
        self.cli.service._next_id = 1

    def test_add_task_with_priority(self):
        """Test adding a task with priority."""
        # Mock sys.argv to simulate command line arguments
        test_args = ["todo", "add", "Test task", "--priority", "high"]

        with patch.object(sys, 'argv', test_args):
            # Capture stdout
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass  # Expected behavior after command execution

            output = captured_output.getvalue()
            assert "Task added" in output

        # Verify the task was added with the correct priority
        tasks = self.cli.service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].priority == Priority.HIGH

    def test_add_task_with_tags(self):
        """Test adding a task with tags."""
        test_args = ["todo", "add", "Test task", "--tags", "work", "urgent"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            assert "Task added" in output

        # Verify the task was added with the correct tags
        tasks = self.cli.service.get_all_tasks()
        assert len(tasks) == 1
        assert "work" in tasks[0].tags
        assert "urgent" in tasks[0].tags

    def test_set_priority_command(self):
        """Test the priority command to set task priority."""
        # First add a task
        task = self.cli.service.create_task("Test task")
        initial_priority = task.priority

        test_args = ["todo", "priority", str(task.id), "high"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            assert f"Priority set to high for task {task.id}" in output

        # Verify the priority was updated
        updated_task = self.cli.service.get_task(task.id)
        assert updated_task.priority == Priority.HIGH
        assert updated_task.priority != initial_priority

    def test_add_tag_command(self):
        """Test the add-tag command."""
        # First add a task
        task = self.cli.service.create_task("Test task")

        test_args = ["todo", "add-tag", str(task.id), "work"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            assert f"Tag 'work' added to task {task.id}" in output

        # Verify the tag was added
        updated_task = self.cli.service.get_task(task.id)
        assert "work" in updated_task.tags

    def test_remove_tag_command(self):
        """Test the remove-tag command."""
        # First add a task and tag
        task = self.cli.service.create_task("Test task")
        self.cli.service.add_tag(task.id, "work")

        test_args = ["todo", "remove-tag", str(task.id), "work"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            assert f"Tag 'work' removed from task {task.id}" in output

        # Verify the tag was removed
        updated_task = self.cli.service.get_task(task.id)
        assert "work" not in updated_task.tags

    def test_list_command_with_priority_filter(self):
        """Test the list command with priority filter."""
        # Add tasks with different priorities
        high_task = self.cli.service.create_task("High priority task", priority=Priority.HIGH)
        low_task = self.cli.service.create_task("Low priority task", priority=Priority.LOW)

        test_args = ["todo", "list", "--priority", "high"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            # Should show only the high priority task
            assert "High priority task" in output
            assert "Low priority task" not in output

    def test_list_command_with_tag_filter(self):
        """Test the list command with tag filter."""
        # Add tasks with different tags
        work_task = self.cli.service.create_task("Work task")
        self.cli.service.add_tag(work_task.id, "work")

        personal_task = self.cli.service.create_task("Personal task")
        self.cli.service.add_tag(personal_task.id, "personal")

        test_args = ["todo", "list", "--tag", "work"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            # Should show only the work task
            assert "Work task" in output
            assert "Personal task" not in output

    def test_list_command_with_sort_priority(self):
        """Test the list command with priority sort."""
        # Add tasks with different priorities
        low_task = self.cli.service.create_task("Low priority task", priority=Priority.LOW)
        high_task = self.cli.service.create_task("High priority task", priority=Priority.HIGH)
        medium_task = self.cli.service.create_task("Medium priority task", priority=Priority.MEDIUM)

        test_args = ["todo", "list", "--sort", "priority"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            # High priority should appear first in the output
            lines = [line for line in output.split('\n') if line.strip()]
            # Find the lines that contain our task titles
            task_lines = [line for line in lines if 'priority task' in line]

            # The high priority task should be first
            assert "High priority task" in task_lines[0]
            assert "Low priority task" in task_lines[-1]  # Last in the filtered list

    def test_list_command_with_search(self):
        """Test the list command with search functionality."""
        # Add tasks with different content
        work_task = self.cli.service.create_task("Work on project", "Need to complete this week")
        personal_task = self.cli.service.create_task("Buy groceries", "Milk and bread")

        test_args = ["todo", "list", "--search", "project"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            # Should show only the project task
            assert "Work on project" in output
            assert "Buy groceries" not in output

    def test_complete_command(self):
        """Test the complete command."""
        task = self.cli.service.create_task("Test task")
        assert not task.completed  # Initially not completed

        test_args = ["todo", "complete", str(task.id)]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            assert f"Task {task.id} marked as completed" in output

        # Verify the task was marked as completed
        completed_task = self.cli.service.get_task(task.id)
        assert completed_task.completed

    def test_update_command(self):
        """Test the update command."""
        task = self.cli.service.create_task("Old title", description="Old description")

        test_args = ["todo", "update", str(task.id), "--title", "New title", "--description", "New description"]

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            assert f"Task {task.id} updated" in output

        # Verify the task was updated
        updated_task = self.cli.service.get_task(task.id)
        assert updated_task.title == "New title"
        assert updated_task.description == "New description"

    def test_help_command(self):
        """Test that CLI shows help when no command is provided."""
        test_args = ["todo"]  # No command specified

        with patch.object(sys, 'argv', test_args):
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    self.cli.run()
                except SystemExit:
                    pass

            output = captured_output.getvalue()
            # Should show help information
            assert "usage:" in output.lower()
            assert "help" in output.lower()