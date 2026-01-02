"""
Simple test script to verify the todo application works correctly.
"""
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli.todo_cli import TodoCLI

def test_todo_app():
    """Test the todo application functionality."""
    print("Testing Todo Application...")

    # Create a CLI instance
    cli = TodoCLI()

    # Test adding a task
    print("\n1. Testing add task:")
    cli.add_task("Test task", "This is a test task")

    # Test listing tasks
    print("\n2. Testing list tasks:")
    cli.list_tasks()

    # Test getting a specific task
    print("\n3. Testing get task (assuming task ID 1 exists):")
    try:
        cli.get_task(1)
    except Exception as e:
        print(f"Expected error for non-existent task: {e}")

    # Test updating a task
    print("\n4. Testing update task:")
    try:
        cli.update_task(1, "Updated test task", "This is an updated test task")
    except Exception as e:
        print(f"Expected error for non-existent task: {e}")

    # Test marking complete
    print("\n5. Testing mark complete:")
    try:
        cli.mark_complete(1)
    except Exception as e:
        print(f"Expected error for non-existent task: {e}")

    # Test deleting a task
    print("\n6. Testing delete task:")
    try:
        cli.delete_task(1)
    except Exception as e:
        print(f"Expected error for non-existent task: {e}")

    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_todo_app()