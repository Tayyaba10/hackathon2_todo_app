import pytest
from datetime import datetime
from src.services.todo_service import TodoService, FilterCriteria
from src.models.task import Task
from src.models.priority import Priority


class TestTodoServicePriorityOperations:
    """Unit tests for priority operations in TodoService."""

    def test_set_priority_success(self):
        """Test setting priority for a task."""
        service = TodoService()
        task = service.create_task("Test Task")

        updated_task = service.set_priority(task.id, Priority.HIGH)

        assert updated_task is not None
        assert updated_task.priority == Priority.HIGH

    def test_set_priority_task_not_found(self):
        """Test setting priority for a non-existent task."""
        service = TodoService()

        result = service.set_priority(999, Priority.HIGH)

        assert result is None

    def test_set_priority_multiple_tasks(self):
        """Test setting priority for multiple tasks."""
        service = TodoService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")

        service.set_priority(task1.id, Priority.LOW)
        service.set_priority(task2.id, Priority.HIGH)

        assert service.get_task(task1.id).priority == Priority.LOW
        assert service.get_task(task2.id).priority == Priority.HIGH

    def test_get_tasks_by_priority(self):
        """Test getting all tasks with a specific priority."""
        service = TodoService()
        task1 = service.create_task("Task 1", priority=Priority.HIGH)
        task2 = service.create_task("Task 2", priority=Priority.LOW)
        task3 = service.create_task("Task 3", priority=Priority.HIGH)

        high_priority_tasks = service.get_tasks_by_priority(Priority.HIGH)

        assert len(high_priority_tasks) == 2
        assert task1 in high_priority_tasks
        assert task3 in high_priority_tasks
        assert task2 not in high_priority_tasks

    def test_get_tasks_by_priority_empty_result(self):
        """Test getting tasks by priority when none match."""
        service = TodoService()
        service.create_task("Task 1", priority=Priority.LOW)

        high_priority_tasks = service.get_tasks_by_priority(Priority.HIGH)

        assert len(high_priority_tasks) == 0


class TestTodoServiceTagOperations:
    """Unit tests for tag operations in TodoService."""

    def test_add_tag_success(self):
        """Test adding a tag to a task."""
        service = TodoService()
        task = service.create_task("Test Task")

        updated_task = service.add_tag(task.id, "work")

        assert updated_task is not None
        assert "work" in updated_task.tags

    def test_add_tag_task_not_found(self):
        """Test adding a tag to a non-existent task."""
        service = TodoService()

        result = service.add_tag(999, "work")

        assert result is None

    def test_remove_tag_success(self):
        """Test removing a tag from a task."""
        service = TodoService()
        task = service.create_task("Test Task")
        service.add_tag(task.id, "work")

        updated_task = service.remove_tag(task.id, "work")

        assert updated_task is not None
        assert "work" not in updated_task.tags

    def test_remove_tag_task_not_found(self):
        """Test removing a tag from a non-existent task."""
        service = TodoService()

        result = service.remove_tag(999, "work")

        assert result is None

    def test_remove_nonexistent_tag(self):
        """Test removing a tag that doesn't exist on the task."""
        service = TodoService()
        task = service.create_task("Test Task")

        # This should raise an error in the Task model, but we're testing the service method
        # which calls the task method and should propagate the exception
        with pytest.raises(ValueError):
            service.remove_tag(task.id, "work")

    def test_get_tasks_by_tag(self):
        """Test getting all tasks with a specific tag."""
        service = TodoService()
        task1 = service.create_task("Task 1")
        service.add_tag(task1.id, "work")
        task2 = service.create_task("Task 2")
        service.add_tag(task2.id, "personal")
        task3 = service.create_task("Task 3")
        service.add_tag(task3.id, "work")

        work_tasks = service.get_tasks_by_tag("work")

        assert len(work_tasks) == 2
        assert task1 in work_tasks
        assert task3 in work_tasks
        assert task2 not in work_tasks

    def test_get_tasks_by_tag_case_insensitive(self):
        """Test getting tasks by tag is case-insensitive."""
        service = TodoService()
        task = service.create_task("Task 1")
        service.add_tag(task.id, "WORK")

        work_tasks = service.get_tasks_by_tag("work")

        assert len(work_tasks) == 1
        assert task in work_tasks

    def test_get_tasks_by_tag_empty_result(self):
        """Test getting tasks by tag when none match."""
        service = TodoService()
        service.create_task("Task 1")
        service.add_tag(1, "work")

        personal_tasks = service.get_tasks_by_tag("personal")

        assert len(personal_tasks) == 0


class TestTodoServiceFilterOperations:
    """Unit tests for filter operations in TodoService."""

    def test_filter_by_status_completed(self):
        """Test filtering tasks by completion status."""
        service = TodoService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        service.update_task(task2.id, completed=True)

        completed_tasks = service.filter_tasks(FilterCriteria(status=True))

        assert len(completed_tasks) == 1
        assert task2 in completed_tasks
        assert task1 not in completed_tasks

    def test_filter_by_status_pending(self):
        """Test filtering tasks by pending status."""
        service = TodoService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        service.update_task(task2.id, completed=True)

        pending_tasks = service.filter_tasks(FilterCriteria(status=False))

        assert len(pending_tasks) == 1
        assert task1 in pending_tasks
        assert task2 not in pending_tasks

    def test_filter_by_priority(self):
        """Test filtering tasks by priority."""
        service = TodoService()
        task1 = service.create_task("Task 1", priority=Priority.HIGH)
        task2 = service.create_task("Task 2", priority=Priority.LOW)
        task3 = service.create_task("Task 3", priority=Priority.HIGH)

        high_tasks = service.filter_tasks(FilterCriteria(priority=Priority.HIGH))

        assert len(high_tasks) == 2
        assert task1 in high_tasks
        assert task3 in high_tasks
        assert task2 not in high_tasks

    def test_filter_by_tag(self):
        """Test filtering tasks by tag."""
        service = TodoService()
        task1 = service.create_task("Task 1")
        service.add_tag(task1.id, "work")
        task2 = service.create_task("Task 2")
        service.add_tag(task2.id, "personal")
        task3 = service.create_task("Task 3")
        service.add_tag(task3.id, "work")

        work_tasks = service.filter_tasks(FilterCriteria(tag="work"))

        assert len(work_tasks) == 2
        assert task1 in work_tasks
        assert task3 in work_tasks
        assert task2 not in work_tasks

    def test_filter_by_tag_case_insensitive(self):
        """Test filtering tasks by tag is case-insensitive."""
        service = TodoService()
        task = service.create_task("Task 1")
        service.add_tag(task.id, "WORK")

        work_tasks = service.filter_tasks(FilterCriteria(tag="work"))

        assert len(work_tasks) == 1
        assert task in work_tasks

    def test_filter_by_multiple_criteria(self):
        """Test filtering tasks by multiple criteria."""
        service = TodoService()
        task1 = service.create_task("Task 1", priority=Priority.HIGH)
        service.add_tag(task1.id, "work")
        task2 = service.create_task("Task 2", priority=Priority.LOW)
        service.add_tag(task2.id, "work")
        service.update_task(task2.id, completed=True)
        task3 = service.create_task("Task 3", priority=Priority.HIGH)
        service.add_tag(task3.id, "work")

        # Filter for high priority AND work tag, but only pending tasks
        filters = FilterCriteria(priority=Priority.HIGH, tag="work", status=False)
        result = service.filter_tasks(filters)

        assert len(result) == 2  # task1 and task3 are high priority and have "work" tag, and are not completed
        assert task1 in result
        assert task3 in result
        assert task2 not in result  # task2 is completed


class TestTodoServiceSortOperations:
    """Unit tests for sort operations in TodoService."""

    def test_sort_by_title_alphabetical(self):
        """Test sorting tasks alphabetically by title."""
        from src.services.todo_service import SortCriteria

        service = TodoService()
        task_c = service.create_task("Zebra Task")
        task_a = service.create_task("Apple Task")
        task_b = service.create_task("Banana Task")

        sorted_tasks = service.sort_tasks(service.get_all_tasks(), SortCriteria.TITLE_ALPHABETICAL)

        assert sorted_tasks[0].title == "Apple Task"
        assert sorted_tasks[1].title == "Banana Task"
        assert sorted_tasks[2].title == "Zebra Task"

    def test_sort_by_priority(self):
        """Test sorting tasks by priority (high to low)."""
        from src.services.todo_service import SortCriteria

        service = TodoService()
        task_low = service.create_task("Low Task", priority=Priority.LOW)
        task_high = service.create_task("High Task", priority=Priority.HIGH)
        task_medium = service.create_task("Medium Task", priority=Priority.MEDIUM)

        sorted_tasks = service.sort_tasks(service.get_all_tasks(), SortCriteria.PRIORITY)

        # High priority should come first, then medium, then low
        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[1].priority == Priority.MEDIUM
        assert sorted_tasks[2].priority == Priority.LOW

    def test_sort_by_creation_date(self):
        """Test sorting tasks by creation date (newest first)."""
        from src.services.todo_service import SortCriteria

        service = TodoService()
        task1 = service.create_task("First Task")
        task2 = service.create_task("Second Task")
        task3 = service.create_task("Third Task")

        sorted_tasks = service.sort_tasks(service.get_all_tasks(), SortCriteria.CREATION_DATE)

        # Third task should be first (newest), then second, then first
        assert sorted_tasks[0].title == "Third Task"
        assert sorted_tasks[1].title == "Second Task"
        assert sorted_tasks[2].title == "First Task"

    def test_sort_empty_list(self):
        """Test sorting an empty list of tasks."""
        from src.services.todo_service import SortCriteria

        service = TodoService()

        sorted_tasks = service.sort_tasks([], SortCriteria.TITLE_ALPHABETICAL)

        assert sorted_tasks == []


class TestTodoServiceSearchOperations:
    """Unit tests for search operations in TodoService."""

    def test_search_by_title(self):
        """Test searching tasks by title."""
        service = TodoService()
        task1 = service.create_task("Work on project", "Detailed description")
        task2 = service.create_task("Buy groceries", "Shopping list")
        task3 = service.create_task("Work meeting", "Team discussion")

        results = service.search_tasks("Work")

        assert len(results) == 2
        assert task1 in results
        assert task3 in results
        assert task2 not in results

    def test_search_by_description(self):
        """Test searching tasks by description."""
        service = TodoService()
        task1 = service.create_task("Task 1", "Work related details")
        task2 = service.create_task("Task 2", "Personal notes")
        task3 = service.create_task("Task 3", "Work and personal")

        results = service.search_tasks("Work")

        assert len(results) == 2
        assert task1 in results
        assert task3 in results
        assert task2 not in results

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        service = TodoService()
        task = service.create_task("WORK TASK", "important details")

        results = service.search_tasks("work")

        assert len(results) == 1
        assert task in results

    def test_search_no_matches(self):
        """Test searching when no tasks match."""
        service = TodoService()
        service.create_task("Work Task", "Work details")

        results = service.search_tasks("nonexistent")

        assert len(results) == 0

    def test_search_empty_query(self):
        """Test searching with empty query."""
        service = TodoService()
        task = service.create_task("Work Task", "Work details")

        results = service.search_tasks("")

        assert len(results) == 0