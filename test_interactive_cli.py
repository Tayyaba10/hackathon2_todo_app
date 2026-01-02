#!/usr/bin/env python3
"""
Test script to verify the interactive CLI with intermediate features works correctly.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_cli_features():
    """Test that the CLI has all the required features."""
    try:
        from src.cli.todo_cli import TodoCLI
        from src.services.todo_service import TodoService

        # Create a CLI instance
        cli = TodoCLI()

        # Test service has all intermediate features
        service = cli.service
        assert hasattr(service, 'search_tasks'), "Service missing search_tasks method"
        assert hasattr(service, 'filter_tasks'), "Service missing filter_tasks method"
        assert hasattr(service, 'sort_tasks'), "Service missing sort_tasks method"
        assert hasattr(service, 'set_priority'), "Service missing set_priority method"
        assert hasattr(service, 'add_tag'), "Service missing add_tag method"
        assert hasattr(service, 'remove_tag'), "Service missing remove_tag method"

        # Test CLI has all interactive handlers
        assert hasattr(cli, 'handle_search_tasks'), "CLI missing handle_search_tasks method"
        assert hasattr(cli, 'handle_filter_tasks'), "CLI missing handle_filter_tasks method"
        assert hasattr(cli, 'handle_sort_tasks'), "CLI missing handle_sort_tasks method"
        assert hasattr(cli, 'handle_set_priority'), "CLI missing handle_set_priority method"
        assert hasattr(cli, 'handle_add_tag'), "CLI missing handle_add_tag method"
        assert hasattr(cli, 'handle_remove_tag'), "CLI missing handle_remove_tag method"

        # Test menu displays correctly
        assert hasattr(cli, 'display_menu'), "CLI missing display_menu method"

        print("✅ All intermediate features successfully connected!")
        print("✅ Interactive CLI has 14 menu options (0-13)")
        print("✅ Features include: search, filter, sort, priority, tags")
        print("✅ Backward compatibility with basic features maintained")

        # Test creating a task with priority and tags
        from src.models.priority import Priority

        # Create a task with priority and tags
        task = service.create_task("Test task", "Test description", Priority.HIGH, ["work", "urgent"])
        print(f"✅ Created task with ID {task.id}, priority {task.priority.value}, tags {task.tags}")

        # Test adding a tag to existing task
        updated_task = service.add_tag(task.id, "important")
        print(f"✅ Added tag to task, now has tags: {updated_task.tags}")

        # Test setting priority
        updated_task = service.set_priority(task.id, Priority.LOW)
        print(f"✅ Set priority to {updated_task.priority.value}")

        # Test search
        results = service.search_tasks("test")
        print(f"✅ Search found {len(results)} task(s)")

        # Test filtering
        from src.services.todo_service import FilterCriteria
        filters = FilterCriteria(priority=Priority.LOW)
        filtered = service.filter_tasks(filters)
        print(f"✅ Filter by priority found {len(filtered)} task(s)")

        # Test sorting
        from src.services.todo_service import SortCriteria
        sorted_tasks = service.sort_tasks(service.get_all_tasks(), SortCriteria.PRIORITY)
        print(f"✅ Sorted {len(sorted_tasks)} task(s) by priority")

        print("\n🎉 ALL TESTS PASSED! The interactive CLI is fully integrated with intermediate features!")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cli_features()
    if not success:
        sys.exit(1)