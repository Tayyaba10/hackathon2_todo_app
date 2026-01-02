import pytest
from datetime import datetime
from src.models.task import Task
from src.models.priority import Priority


class TestTask:
    """Unit tests for the extended Task model."""

    def test_task_initialization_with_defaults(self):
        """Test Task initialization with default values."""
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
        assert task.priority == Priority.MEDIUM  # Default priority
        assert task.tags == []
        assert task.created_at is not None
        assert task.updated_at is not None
        assert task.due_date is None

    def test_task_initialization_with_all_values(self):
        """Test Task initialization with all values provided."""
        from datetime import datetime

        created_time = datetime(2023, 1, 1, 12, 0, 0)
        due_time = datetime(2023, 12, 31, 23, 59, 59)

        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=True,
            priority=Priority.HIGH,
            tags=["work", "urgent"],
            created_at=created_time,
            updated_at=created_time,
            due_date=due_time
        )

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is True
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]
        assert task.created_at == created_time
        assert task.updated_at == created_time
        assert task.due_date == due_time

    def test_add_tag_success(self):
        """Test adding a tag to a task."""
        task = Task(id=1, title="Test Task")

        task.add_tag("work")

        assert "work" in task.tags
        assert len(task.tags) == 1

    def test_add_tag_duplicate_error(self):
        """Test that adding a duplicate tag raises ValueError."""
        task = Task(id=1, title="Test Task")
        task.add_tag("work")

        with pytest.raises(ValueError, match="Tag 'work' already exists on this task"):
            task.add_tag("work")

    def test_add_tag_empty_error(self):
        """Test that adding an empty tag raises ValueError."""
        task = Task(id=1, title="Test Task")

        with pytest.raises(ValueError, match="Tag cannot be empty or whitespace only"):
            task.add_tag("")

        with pytest.raises(ValueError, match="Tag cannot be empty or whitespace only"):
            task.add_tag("   ")

    def test_add_tag_case_normalization(self):
        """Test that tags are normalized to lowercase."""
        task = Task(id=1, title="Test Task")

        task.add_tag("WORK")

        assert "work" in task.tags

    def test_remove_tag_success(self):
        """Test removing a tag from a task."""
        task = Task(id=1, title="Test Task")
        task.add_tag("work")

        task.remove_tag("work")

        assert "work" not in task.tags
        assert len(task.tags) == 0

    def test_remove_tag_not_exists_error(self):
        """Test that removing a non-existent tag raises ValueError."""
        task = Task(id=1, title="Test Task")

        with pytest.raises(ValueError, match="Tag 'work' does not exist on this task"):
            task.remove_tag("work")

    def test_remove_tag_case_insensitive(self):
        """Test that removing tags is case-insensitive."""
        task = Task(id=1, title="Test Task")
        task.add_tag("work")

        task.remove_tag("WORK")

        assert "work" not in task.tags

    def test_set_priority_success(self):
        """Test setting task priority."""
        task = Task(id=1, title="Test Task")

        task.set_priority(Priority.HIGH)

        assert task.priority == Priority.HIGH

    def test_set_priority_type_error(self):
        """Test that setting priority with non-Priority value raises TypeError."""
        task = Task(id=1, title="Test Task")

        with pytest.raises(TypeError, match="Priority must be a Priority enum value"):
            task.set_priority("high")

    def test_to_dict(self):
        """Test converting Task to dictionary."""
        task = Task(id=1, title="Test Task", description="Test Description")
        task.add_tag("work")

        task_dict = task.to_dict()

        assert task_dict["id"] == 1
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["completed"] is False
        assert task_dict["priority"] == "medium"
        assert task_dict["tags"] == ["work"]
        assert "created_at" in task_dict
        assert "updated_at" in task_dict
        assert task_dict["due_date"] is None

    def test_str_representation(self):
        """Test string representation of Task."""
        task = Task(id=1, title="Test Task")
        task.add_tag("work")

        str_repr = str(task)
        assert "[MEDIUM]" in str_repr
        assert "Test Task" in str_repr
        assert "[work]" in str_repr
        assert "○" in str_repr  # Not completed

    def test_str_representation_completed(self):
        """Test string representation of completed Task."""
        task = Task(id=1, title="Test Task", completed=True)

        str_repr = str(task)
        assert "✓" in str_repr  # Completed

    def test_str_representation_with_due_date(self):
        """Test string representation with due date."""
        from datetime import datetime

        due_date = datetime(2023, 12, 31)
        task = Task(id=1, title="Test Task", due_date=due_date)

        str_repr = str(task)
        assert "due: 2023-12-31" in str_repr

    def test_repr_representation(self):
        """Test detailed string representation of Task."""
        task = Task(id=1, title="Test Task")
        task.add_tag("work")

        repr_str = repr(task)
        assert "Task(id=1" in repr_str
        assert "title='Test Task'" in repr_str
        assert "completed=False" in repr_str
        assert "priority=" in repr_str
        assert "work" in repr_str

    def test_equality(self):
        """Test Task equality based on ID."""
        task1 = Task(id=1, title="Test Task 1")
        task2 = Task(id=1, title="Test Task 2")  # Same ID
        task3 = Task(id=2, title="Test Task 3")  # Different ID

        assert task1 == task2
        assert task1 != task3

    def test_equality_with_non_task(self):
        """Test Task equality with non-Task object."""
        task = Task(id=1, title="Test Task")

        assert task != "not a task"
        assert task != 123
        assert task != None

    def test_hash(self):
        """Test Task hashing based on ID."""
        task = Task(id=1, title="Test Task")

        # Hash should be based on ID
        assert hash(task) == hash(1)

    def test_updated_at_changes_on_tag_operations(self):
        """Test that updated_at changes when tags are modified."""
        task = Task(id=1, title="Test Task")
        original_updated_at = task.updated_at

        # Sleep briefly to ensure time difference
        import time
        time.sleep(0.001)  # Sleep for 1 millisecond

        task.add_tag("work")
        assert task.updated_at > original_updated_at

        original_updated_at = task.updated_at
        time.sleep(0.001)  # Sleep for 1 millisecond

        task.remove_tag("work")
        assert task.updated_at > original_updated_at

    def test_updated_at_changes_on_priority_change(self):
        """Test that updated_at changes when priority is modified."""
        task = Task(id=1, title="Test Task")
        original_updated_at = task.updated_at

        # Sleep briefly to ensure time difference
        import time
        time.sleep(0.001)  # Sleep for 1 millisecond

        task.set_priority(Priority.HIGH)
        assert task.updated_at > original_updated_at