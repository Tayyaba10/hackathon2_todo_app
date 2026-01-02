from typing import List
from src.models.task import Task


class SearchService:
    """
    Dedicated service for search functionality.

    Provides methods to search tasks by keywords in title and description.
    """

    def search_by_keyword(self, tasks: List[Task], keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title and description.

        Args:
            tasks: List of tasks to search through
            keyword: Keyword to search for

        Returns:
            List of tasks that match the keyword
        """
        if not keyword or not keyword.strip():
            return []

        keyword = keyword.lower().strip()
        matching_tasks = []

        for task in tasks:
            # Check if keyword appears in title or description
            if (keyword in task.title.lower() or
                keyword in task.description.lower()):
                matching_tasks.append(task)

        return matching_tasks

    def search_by_keyword_safe(self, tasks: List[Task], keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title and description with additional safety checks.

        Args:
            tasks: List of tasks to search through
            keyword: Keyword to search for

        Returns:
            List of tasks that match the keyword
        """
        if not keyword or not isinstance(keyword, str) or not keyword.strip():
            return []

        if not tasks:
            return []

        keyword = keyword.lower().strip()
        matching_tasks = []

        for task in tasks:
            # Safety check in case task attributes are None
            title = task.title or ""
            description = task.description or ""

            # Check if keyword appears in title or description
            if (keyword in title.lower() or
                keyword in description.lower()):
                matching_tasks.append(task)

        return matching_tasks

    def search_by_multiple_keywords(self, tasks: List[Task], keywords: List[str]) -> List[Task]:
        """
        Search with multiple keywords (OR logic - task matches if it contains any of the keywords).

        Args:
            tasks: List of tasks to search through
            keywords: List of keywords to search for

        Returns:
            List of tasks that match any of the keywords
        """
        if not keywords:
            return []

        # Filter out empty keywords
        valid_keywords = [kw.lower().strip() for kw in keywords if kw and kw.strip()]

        if not valid_keywords:
            return []

        matching_tasks = []

        for task in tasks:
            # Check if any keyword appears in title or description
            for keyword in valid_keywords:
                if (keyword in task.title.lower() or
                    keyword in task.description.lower()):
                    matching_tasks.append(task)
                    break  # Once we find a match, no need to check other keywords

        return matching_tasks

    def search_by_exact_match(self, tasks: List[Task], keyword: str) -> List[Task]:
        """
        Search tasks where title or description exactly matches the keyword.

        Args:
            tasks: List of tasks to search through
            keyword: Keyword to search for (exact match)

        Returns:
            List of tasks that exactly match the keyword
        """
        if not keyword or not keyword.strip():
            return []

        keyword = keyword.lower().strip()
        matching_tasks = []

        for task in tasks:
            # Check if title or description exactly matches the keyword
            if (task.title.lower() == keyword or
                task.description.lower() == keyword):
                matching_tasks.append(task)

        return matching_tasks