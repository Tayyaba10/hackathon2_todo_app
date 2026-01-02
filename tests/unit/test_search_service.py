import pytest
from src.services.search_service import SearchService
from src.models.task import Task
from src.models.priority import Priority


class TestSearchService:
    """Unit tests for the SearchService."""

    def setup_method(self):
        """Set up a fresh SearchService instance for each test."""
        self.service = SearchService()

    def test_search_by_keyword_title_match(self):
        """Test searching by keyword in task title."""
        # Create tasks
        task1 = Task(id=1, title="Work on project", description="Complete the project")
        task2 = Task(id=2, title="Buy groceries", description="Milk and bread")
        tasks = [task1, task2]

        results = self.service.search_by_keyword(tasks, "project")

        assert len(results) == 1
        assert task1 in results
        assert task2 not in results

    def test_search_by_keyword_description_match(self):
        """Test searching by keyword in task description."""
        # Create tasks
        task1 = Task(id=1, title="Task 1", description="Work related details")
        task2 = Task(id=2, title="Task 2", description="Personal notes")
        tasks = [task1, task2]

        results = self.service.search_by_keyword(tasks, "Work")

        assert len(results) == 1
        assert task1 in results
        assert task2 not in results

    def test_search_by_keyword_case_insensitive(self):
        """Test that keyword search is case-insensitive."""
        task = Task(id=1, title="WORK TASK", description="IMPORTANT DETAILS")
        tasks = [task]

        results = self.service.search_by_keyword(tasks, "work")

        assert len(results) == 1
        assert task in results

    def test_search_by_keyword_multiple_matches(self):
        """Test searching where multiple tasks match the keyword."""
        task1 = Task(id=1, title="Work on project", description="Important work")
        task2 = Task(id=2, title="More work", description="Additional work details")
        task3 = Task(id=3, title="Personal task", description="Not work related")
        tasks = [task1, task2, task3]

        results = self.service.search_by_keyword(tasks, "work")

        assert len(results) == 2
        assert task1 in results
        assert task2 in results
        assert task3 not in results

    def test_search_by_keyword_no_matches(self):
        """Test searching when no tasks match the keyword."""
        task1 = Task(id=1, title="Work task", description="Work details")
        tasks = [task1]

        results = self.service.search_by_keyword(tasks, "nonexistent")

        assert len(results) == 0

    def test_search_by_keyword_empty_query(self):
        """Test searching with empty query."""
        task = Task(id=1, title="Work task", description="Work details")
        tasks = [task]

        results = self.service.search_by_keyword(tasks, "")

        assert len(results) == 0

    def test_search_by_keyword_whitespace_only_query(self):
        """Test searching with whitespace-only query."""
        task = Task(id=1, title="Work task", description="Work details")
        tasks = [task]

        results = self.service.search_by_keyword(tasks, "   ")

        assert len(results) == 0

    def test_search_by_multiple_keywords_single_match(self):
        """Test searching by multiple keywords where only one matches."""
        task1 = Task(id=1, title="Work on project", description="Complete the project")
        task2 = Task(id=2, title="Buy groceries", description="Milk and bread")
        tasks = [task1, task2]

        results = self.service.search_by_multiple_keywords(tasks, ["project", "nonexistent"])

        assert len(results) == 1
        assert task1 in results
        assert task2 not in results

    def test_search_by_multiple_keywords_multiple_matches(self):
        """Test searching by multiple keywords where multiple tasks match."""
        task1 = Task(id=1, title="Work on project", description="Complete the project")
        task2 = Task(id=2, title="Buy groceries", description="Milk and bread for work")
        task3 = Task(id=3, title="Personal task", description="Not related")
        tasks = [task1, task2, task3]

        results = self.service.search_by_multiple_keywords(tasks, ["project", "work"])

        assert len(results) == 2
        assert task1 in results
        assert task2 in results
        assert task3 not in results

    def test_search_by_multiple_keywords_all_empty(self):
        """Test searching by multiple keywords when all keywords are empty."""
        task = Task(id=1, title="Work task", description="Work details")
        tasks = [task]

        results = self.service.search_by_multiple_keywords(tasks, ["", "   "])

        assert len(results) == 0

    def test_search_by_multiple_keywords_some_empty(self):
        """Test searching by multiple keywords where some are empty."""
        task1 = Task(id=1, title="Work on project", description="Complete the project")
        task2 = Task(id=2, title="Buy groceries", description="Milk and bread")
        tasks = [task1, task2]

        results = self.service.search_by_multiple_keywords(tasks, ["", "project", "   "])

        assert len(results) == 1
        assert task1 in results
        assert task2 not in results

    def test_search_by_multiple_keywords_empty_list(self):
        """Test searching by an empty list of keywords."""
        task = Task(id=1, title="Work task", description="Work details")
        tasks = [task]

        results = self.service.search_by_multiple_keywords(tasks, [])

        assert len(results) == 0

    def test_search_by_exact_match(self):
        """Test searching for exact matches."""
        task1 = Task(id=1, title="exact match", description="description")
        task2 = Task(id=2, title="partial match", description="description")
        task3 = Task(id=3, title="title", description="exact match")
        tasks = [task1, task2, task3]

        results = self.service.search_by_exact_match(tasks, "exact match")

        assert len(results) == 2
        assert task1 in results  # Title matches exactly
        assert task3 in results  # Description matches exactly
        assert task2 not in results  # Only partially matches

    def test_search_by_exact_match_case_insensitive(self):
        """Test that exact match search is case-insensitive."""
        task = Task(id=1, title="EXACT MATCH", description="description")
        tasks = [task]

        results = self.service.search_by_exact_match(tasks, "exact match")

        assert len(results) == 1
        assert task in results

    def test_search_by_exact_match_no_match(self):
        """Test exact match search when no exact matches exist."""
        task = Task(id=1, title="partial matching", description="description")
        tasks = [task]

        results = self.service.search_by_exact_match(tasks, "match")

        assert len(results) == 0

    def test_search_with_special_characters(self):
        """Test searching with special characters."""
        task = Task(id=1, title="Task with special chars: @#$%", description="description")
        tasks = [task]

        results = self.service.search_by_keyword(tasks, "@#$%")

        assert len(results) == 1
        assert task in results