import pytest
from src.services.todo_service import TodoService
from src.models.priority import Priority


class TestIntegrationFeatures:
    """Integration tests covering combined usage of features."""

    def setup_method(self):
        """Set up a fresh TodoService instance for each test."""
        self.service = TodoService()

    def test_create_task_with_all_features(self):
        """Test creating a task with priority, tags, and due date."""
        task = self.service.create_task(
            title="Complete project",
            description="Finish the project documentation",
            priority=Priority.HIGH,
            tags=["work", "urgent"],
        )

        assert task.title == "Complete project"
        assert task.description == "Finish the project documentation"
        assert task.priority == Priority.HIGH
        assert "work" in task.tags
        assert "urgent" in task.tags

    def test_priority_and_tag_workflow(self):
        """Test a workflow using priorities and tags together."""
        # Create tasks with different priorities and tags
        high_work_task = self.service.create_task("Urgent work task", priority=Priority.HIGH)
        self.service.add_tag(high_work_task.id, "work")

        low_personal_task = self.service.create_task("Low priority task", priority=Priority.LOW)
        self.service.add_tag(low_personal_task.id, "personal")

        # Test filtering by both priority and tag
        high_priority_tasks = self.service.get_tasks_by_priority(Priority.HIGH)
        work_tasks = self.service.get_tasks_by_tag("work")

        assert high_work_task in high_priority_tasks
        assert high_work_task in work_tasks
        assert low_personal_task not in high_priority_tasks
        assert low_personal_task not in work_tasks

    def test_search_filter_sort_workflow(self):
        """Test a workflow combining search, filter, and sort."""
        # Create multiple tasks
        task1 = self.service.create_task("Write report", priority=Priority.HIGH)
        self.service.add_tag(task1.id, "work")

        task2 = self.service.create_task("Buy groceries", priority=Priority.MEDIUM)
        self.service.add_tag(task2.id, "personal")

        task3 = self.service.create_task("Code review", priority=Priority.HIGH)
        self.service.add_tag(task3.id, "work")

        # Search for tasks containing "work" (in title)
        search_results = self.service.search_tasks("work")
        assert len(search_results) == 2  # task1 and task3

        # Filter high priority tasks
        high_priority_tasks = self.service.get_tasks_by_priority(Priority.HIGH)
        assert len(high_priority_tasks) == 2  # task1 and task3

        # Sort the high priority tasks by title
        sorted_tasks = self.service.sort_tasks(high_priority_tasks, "title_alphabetical")
        assert sorted_tasks[0].title == "Code review"
        assert sorted_tasks[1].title == "Write report"

    def test_complete_task_workflow(self):
        """Test a complete workflow: create, prioritize, tag, filter, update, complete."""
        # Create a task with priority and tags
        task = self.service.create_task("Setup meeting", priority=Priority.HIGH)
        self.service.add_tag(task.id, "work")
        self.service.add_tag(task.id, "urgent")

        # Verify the task was created correctly
        assert task.priority == Priority.HIGH
        assert "work" in task.tags
        assert "urgent" in task.tags
        assert not task.completed

        # Filter by priority and tag
        high_priority_tasks = self.service.get_tasks_by_priority(Priority.HIGH)
        assert task in high_priority_tasks

        work_tasks = self.service.get_tasks_by_tag("work")
        assert task in work_tasks

        # Complete the task
        updated_task = self.service.update_task(task.id, completed=True)
        assert updated_task.completed

        # Verify it's now in completed tasks
        completed_tasks = self.service.get_completed_tasks()
        assert updated_task in completed_tasks

        pending_tasks = self.service.get_pending_tasks()
        assert updated_task not in pending_tasks

    def test_multiple_filters(self):
        """Test applying multiple filters in sequence."""
        # Create tasks with different attributes
        task1 = self.service.create_task("High priority work", priority=Priority.HIGH)
        self.service.add_tag(task1.id, "work")

        task2 = self.service.create_task("Low priority personal", priority=Priority.LOW)
        self.service.add_tag(task2.id, "personal")

        task3 = self.service.create_task("High priority personal", priority=Priority.HIGH)
        self.service.add_tag(task3.id, "personal")

        # Filter by high priority
        high_tasks = self.service.get_tasks_by_priority(Priority.HIGH)
        assert len(high_tasks) == 2
        assert task1 in high_tasks
        assert task3 in high_tasks
        assert task2 not in high_tasks

        # Then filter high priority tasks by personal tag
        personal_high_tasks = [t for t in high_tasks if "personal" in t.tags]
        assert len(personal_high_tasks) == 1
        assert task3 in personal_high_tasks

    def test_search_then_filter_workflow(self):
        """Test searching first, then applying filters to the results."""
        # Create tasks
        important_task = self.service.create_task("Important meeting notes", priority=Priority.HIGH)
        self.service.add_tag(important_task.id, "work")

        regular_task = self.service.create_task("Regular task", priority=Priority.MEDIUM)
        self.service.add_tag(regular_task.id, "personal")

        another_task = self.service.create_task("Meeting preparation", priority=Priority.LOW)
        self.service.add_tag(another_task.id, "work")

        # Search for tasks containing "meeting"
        search_results = self.service.search_tasks("meeting")
        assert len(search_results) == 2  # important_task and another_task

        # Filter these search results by high priority
        high_priority_from_search = [t for t in search_results if t.priority == Priority.HIGH]
        assert len(high_priority_from_search) == 1
        assert important_task in high_priority_from_search

        # Filter by work tag
        work_tasks_from_search = [t for t in search_results if "work" in t.tags]
        assert len(work_tasks_from_search) == 2
        assert important_task in work_tasks_from_search
        assert another_task in work_tasks_from_search

    def test_sort_after_filter(self):
        """Test sorting filtered results."""
        # Create tasks with different priorities
        low_task = self.service.create_task("Low priority task", priority=Priority.LOW)
        high_task = self.service.create_task("High priority task", priority=Priority.HIGH)
        medium_task = self.service.create_task("Medium priority task", priority=Priority.MEDIUM)

        # Get all tasks and sort by priority (high to low)
        all_tasks = self.service.get_all_tasks()
        sorted_tasks = self.service.sort_tasks(all_tasks, "priority")

        # Verify order: High, Medium, Low
        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[1].priority == Priority.MEDIUM
        assert sorted_tasks[2].priority == Priority.LOW

        # Now filter only medium and low priority tasks and sort them
        medium_low_tasks = [t for t in all_tasks if t.priority in [Priority.MEDIUM, Priority.LOW]]
        sorted_medium_low = self.service.sort_tasks(medium_low_tasks, "priority")

        # Verify order: Medium, Low
        assert sorted_medium_low[0].priority == Priority.MEDIUM
        assert sorted_medium_low[1].priority == Priority.LOW