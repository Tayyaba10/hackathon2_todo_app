"""
Interactive CLI for the todo application.

This module contains the interactive, menu-driven command-line interface for the todo application.
Users interact through numbered menu options with emoji indicators.
"""
from typing import List
from src.services.todo_service import TodoService


class TodoCLI:
    """
    Command-line interface for the todo application.

    This class handles user interaction through command-line interface.
    """

    def __init__(self):
        """Initialize the CLI with a todo service."""
        self.service = TodoService()

    def add_task(self, title: str, description: str = "") -> None:
        """
        Add a new task to the system.

        Args:
            title: Title of the task
            description: Description of the task
        """
        try:
            task = self.service.create_task(title, description)
            print(f"Task added successfully with ID: {task.id}")
        except Exception as e:
            print(f"Error adding task: {str(e)}")

    def list_tasks(self) -> None:
        """List all tasks in the system with emoji indicators."""
        try:
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("📭 No tasks found.")
                return

            print("📋 All Tasks:")
            for task in tasks:
                status_emoji = "✅" if task.completed else "⬜"
                print(f"{status_emoji} ID: {task.id} | {task.title}")
                if task.description:
                    print(f"   Description: {task.description}")
                if task.priority:
                    print(f"   Priority: {task.priority.value}")
                if task.tags:
                    print(f"   Tags: {', '.join(task.tags)}")
                print(f"   Status: {'Completed' if task.completed else 'Pending'}")
        except Exception as e:
            print(f"Error listing tasks: {str(e)}")

    def get_task(self, task_id: int) -> None:
        """
        Get a specific task by ID with emoji indicators.

        Args:
            task_id: ID of the task to retrieve
        """
        try:
            task = self.service.get_task(task_id)
            if not task:
                print(f"❌ Task with ID {task_id} not found.")
                return

            status_emoji = "✅" if task.completed else "⬜"
            print(f"{status_emoji} ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            if task.priority:
                print(f"Priority: {task.priority.value}")
            if task.tags:
                print(f"Tags: {', '.join(task.tags)}")
            print(f"Status: {'Completed' if task.completed else 'Pending'}")
            print(f"Created: {task.created_at}")
        except Exception as e:
            print(f"Error getting task: {str(e)}")

    def update_task(self, task_id: int, title: str = None, description: str = None) -> None:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
        """
        try:
            success = self.service.update_task(task_id, title, description)
            if success:
                print(f"Task {task_id} updated successfully")
            else:
                print(f"Failed to update task {task_id}")
        except Exception as e:
            print(f"Error updating task: {str(e)}")

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete
        """
        try:
            success = self.service.delete_task(task_id)
            if success:
                print(f"Task {task_id} deleted successfully")
            else:
                print(f"Failed to delete task {task_id}")
        except Exception as e:
            print(f"Error deleting task: {str(e)}")

    def mark_complete(self, task_id: int) -> None:
        """
        Mark a task as complete.

        Args:
            task_id: ID of the task to mark complete
        """
        try:
            task = self.service.update_task(task_id, completed=True)
            if task:
                print(f"Task {task_id} marked as complete")
            else:
                print(f"Failed to mark task {task_id} as complete")
        except Exception as e:
            print(f"Error marking task as complete: {str(e)}")

    def mark_incomplete(self, task_id: int) -> None:
        """
        Mark a task as incomplete.

        Args:
            task_id: ID of the task to mark incomplete
        """
        try:
            task = self.service.update_task(task_id, completed=False)
            if task:
                print(f"Task {task_id} marked as incomplete")
            else:
                print(f"Failed to mark task {task_id} as incomplete")
        except Exception as e:
            print(f"Error marking task as incomplete: {str(e)}")

    def display_menu(self) -> None:
        """Display the main menu with emoji indicators."""
        print("\n📝 Welcome to Todo App!")
        print("\n1.  ➕ Add a new task")
        print("2. 📋 View all tasks")
        print("3. 🔍 Search tasks")
        print("4. 🎯 Filter tasks")
        print("5. 📊 Sort tasks")
        print("6. ⚡ Set task priority")
        print("7. 🏷️ Add task tag")
        print("8. ❌ Remove task tag")
        print("9. ✏️ Update a task")
        print("10. ✅ Mark task as complete")
        print("11.🔄 Mark task as incomplete")
        print("12. 🗑️ Delete a task")
        print("13. 🔁 Set recurring task")
        print("14. ⏰ update task due date")
        print("15. 🔔 View upcoming recurring tasks")
        print("16. ❓ Help")
        print("0.  🚪 Exit")

    def run_interactive(self) -> None:
        """Run the interactive CLI loop with menu system."""
        while True:
            try:
                self.display_menu()
                choice = input("\nSelect an option (0-16): ").strip()

                if not choice.isdigit():
                    print("❌ Please enter a number between 0 and 16.")
                    continue

                choice_num = int(choice)

                if choice_num == 0:
                    self.handle_exit()
                    break
                elif choice_num == 1:
                    self.handle_add_task()
                elif choice_num == 2:
                    self.handle_view_tasks()
                elif choice_num == 3:
                    self.handle_search_tasks()
                elif choice_num == 4:
                    self.handle_filter_tasks()
                elif choice_num == 5:
                    self.handle_sort_tasks()
                elif choice_num == 6:
                    self.handle_set_priority()
                elif choice_num == 7:
                    self.handle_add_tag()
                elif choice_num == 8:
                    self.handle_remove_tag()
                elif choice_num == 9:
                    self.handle_update_task()
                elif choice_num == 10:
                    self.handle_mark_complete()
                elif choice_num == 11:
                    self.handle_mark_incomplete()
                elif choice_num == 12:
                    self.handle_delete_task()
                elif choice_num == 13:
                    self.handle_set_recurring_task()
                elif choice_num == 14:
                    self.handle_set_update_due_date()
                elif choice_num == 15:
                    self.handle_view_upcoming_recurring_tasks()
                elif choice_num == 16:
                    self.handle_help()
                else:
                    print("❌ Invalid option. Please select a number between 0 and 16.")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break

    def handle_exit(self) -> None:
        """Handle the exit functionality."""
        print("👋 Goodbye!")

    def handle_add_task(self) -> None:
        """Handle adding a new task with guided prompts."""
        try:
            title = input("Enter task title: ").strip()

            if not title:
                print("❌ Task title cannot be empty. Please try again.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            description = input("Enter task description (optional): ").strip()

            # Ask for priority
            priority_input = input("Enter priority (high/medium/low, or press Enter to skip): ").strip().lower()
            priority = None
            if priority_input:
                if priority_input in ['high', 'h']:
                    from src.models.priority import Priority
                    priority = Priority.HIGH
                elif priority_input in ['medium', 'm']:
                    from src.models.priority import Priority
                    priority = Priority.MEDIUM
                elif priority_input in ['low', 'l']:
                    from src.models.priority import Priority
                    priority = Priority.LOW
                else:
                    print("❌ Invalid priority. Use 'high', 'medium', or 'low'.")
                    print("Press Enter to return to main menu...", end="")
                    input()
                    return

            # Ask for tags
            tags_input = input("Enter tags (comma-separated, or press Enter to skip): ").strip()
            tags = None
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

            # Use the create_task method from the service
            task = self.service.create_task(title, description, priority, tags)
            print(f"✅ Task added successfully with ID: {task.id}")
            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error adding task: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_view_tasks(self) -> None:
        """Handle viewing all tasks with emoji indicators."""
        try:
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("\n📭 No tasks found.")
            else:
                print("\n📋 All Tasks:")
                for task in tasks:
                    status_emoji = "✅" if task.completed else "⬜"
                    print(f"\n{status_emoji} ID: {task.id} | {task.title}")
                    if task.description:
                        print(f"   Description: {task.description}")
                    if task.priority:
                        print(f"   Priority: {task.priority.value}")
                    if task.tags:
                        print(f"   Tags: {', '.join(task.tags)}")
                    print(f"   Status: {'Completed' if task.completed else 'Pending'}")

            print("\nPress Enter to return to main menu...", end="")
            input()

        except Exception as e:
            print(f"❌ Error viewing tasks: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_update_task(self) -> None:
        """Handle updating a task with guided prompts."""
        try:
            task_id_input = input("Enter task ID to update: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            try:
                task = self.service.get_task(task_id)
            except Exception:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            print(f"Current task: {task.title}")
            if task.description:
                print(f"Current description: {task.description}")

            new_title = input(f"Enter new title (or press Enter to keep '{task.title}'): ").strip()
            if new_title == "":
                new_title = task.title  # Keep original title if empty input

            if not new_title:
                print("❌ Task title cannot be empty. Please try again.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            new_description = input(f"Enter new description (or press Enter to keep current): ").strip()
            if new_description == "":
                new_description = task.description  # Keep original description if empty input

            success = self.service.update_task(task_id, new_title, new_description)
            if success:
                print(f"✅ Task {task_id} updated successfully")
            else:
                print(f"❌ Failed to update task {task_id}")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error updating task: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_delete_task(self) -> None:
        """Handle deleting a task with guided prompts."""
        try:
            task_id_input = input("Enter task ID to delete: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            try:
                task = self.service.get_task(task_id)
                print(f"You are about to delete: {task.title}")
                if task.description:
                    print(f"Description: {task.description}")
            except Exception:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            confirm = input(f"Are you sure you want to delete task {task_id}? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ Task deletion cancelled.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            success = self.service.delete_task(task_id)
            if success:
                print(f"✅ Task {task_id} deleted successfully")
            else:
                print(f"❌ Failed to delete task {task_id}")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error deleting task: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_mark_complete(self) -> None:
        """Handle marking a task as complete with guided prompts."""
        try:
            task_id_input = input("Enter task ID to mark as complete: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            task = self.service.get_task(task_id)
            if not task:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            if task.completed:
                print(f"⚠️  Task {task_id} is already marked as complete.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            updated_task = self.service.update_task(task_id, completed=True)
            if updated_task:
                print(f"✅ Task {task_id} marked as complete")
            else:
                print(f"❌ Failed to mark task {task_id} as complete")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error marking task as complete: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_mark_incomplete(self) -> None:
        """Handle marking a task as incomplete with guided prompts."""
        try:
            task_id_input = input("Enter task ID to mark as incomplete: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            task = self.service.get_task(task_id)
            if not task:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            if not task.completed:
                print(f"⚠️  Task {task_id} is already marked as incomplete.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            updated_task = self.service.update_task(task_id, completed=False)
            if updated_task:
                print(f"✅ Task {task_id} marked as incomplete")
            else:
                print(f"❌ Failed to mark task {task_id} as incomplete")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error marking task as incomplete: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_help(self) -> None:
        """Show help information for the interactive menu."""
        help_text = """
📋 Interactive Todo App Help

This application uses a menu-driven interface with numbered options.
Select an option by entering the corresponding number.

Menu Options:
1️⃣  ➕ Add a new task - Create a new todo item
2️⃣  📋 View all tasks - See all your tasks with status
3️⃣  🔍 Search tasks - Find tasks by keywords
4️⃣  🎯 Filter tasks - Show tasks by criteria (status, priority, tag)
5️⃣  📊 Sort tasks - Order tasks (by title, priority, date)
6️⃣  ⚡ Set task priority - Assign priority (high, medium, low)
7️⃣  🏷️ Add task tag - Add a category to a task
8️⃣  ❌ Remove task tag - Remove a category from a task
9️⃣  ✏️ Update a task - Modify an existing task
1️⃣0️⃣ ✅ Mark task as complete - Change task status to completed
1️⃣1️⃣ 🔄 Mark task as incomplete - Change task status to pending
1️⃣2️⃣ 🗑️ Delete a task - Remove a task permanently
1️⃣3️⃣ ❓ Help - Show this help message
0️⃣  🚪 Exit - Quit the application

Emoji Guide:
⬜ - Incomplete task
✅ - Completed task
➕ - Add operation
🔍 - Search operation
🎯 - Filter operation
📊 - Sort operation
⚡ - Priority operation
🏷️ - Tag operation
❌ - Remove operation
✏️ - Update operation
✅ - Complete operation
🔄 - Incomplete operation
🗑️ - Delete operation
❓ - Help operation
🚪 - Exit operation

After each operation, you'll be returned to the main menu automatically.
        """
        print(help_text)
        print("Press Enter to return to main menu...", end="")
        input()

    def handle_search_tasks(self) -> None:
        """Handle searching tasks with guided prompts."""
        try:
            query = input("Enter search query: ").strip()
            if not query:
                print("❌ Search query cannot be empty.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            results = self.service.search_tasks(query)
            if not results:
                print(f"\n📭 No tasks found matching '{query}'.")
            else:
                print(f"\n🔍 Found {len(results)} task(s) matching '{query}':")
                for task in results:
                    status_emoji = "✅" if task.completed else "⬜"
                    print(f"\n{status_emoji} ID: {task.id} | {task.title}")
                    if task.description:
                        print(f"   Description: {task.description}")
                    if task.priority:
                        print(f"   Priority: {task.priority.value}")
                    if task.tags:
                        print(f"   Tags: {', '.join(task.tags)}")
                    print(f"   Status: {'Completed' if task.completed else 'Pending'}")

            print("\nPress Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error searching tasks: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_filter_tasks(self) -> None:
        """Handle filtering tasks with guided prompts."""
        try:
            print("\nFilter options:")
            print("1. Filter by status (completed/pending)")
            print("2. Filter by priority (high/medium/low)")
            print("3. Filter by tag")
            print("4. Combine filters")

            filter_choice = input("\nSelect filter type (1-4): ").strip()

            from src.services.todo_service import FilterCriteria
            filters = FilterCriteria()

            if filter_choice == "1":
                status_choice = input("Filter by status (completed/pending): ").strip().lower()
                if status_choice in ['completed', 'c']:
                    filters.status = True
                elif status_choice in ['pending', 'p']:
                    filters.status = False
                else:
                    print("❌ Invalid status. Use 'completed' or 'pending'.")
                    print("Press Enter to return to main menu...", end="")
                    input()
                    return
            elif filter_choice == "2":
                priority_choice = input("Filter by priority (high/medium/low): ").strip().lower()
                if priority_choice in ['high', 'h']:
                    from src.models.priority import Priority
                    filters.priority = Priority.HIGH
                elif priority_choice in ['medium', 'm']:
                    from src.models.priority import Priority
                    filters.priority = Priority.MEDIUM
                elif priority_choice in ['low', 'l']:
                    from src.models.priority import Priority
                    filters.priority = Priority.LOW
                else:
                    print("❌ Invalid priority. Use 'high', 'medium', or 'low'.")
                    print("Press Enter to return to main menu...", end="")
                    input()
                    return
            elif filter_choice == "3":
                tag = input("Filter by tag: ").strip()
                if not tag:
                    print("❌ Tag cannot be empty.")
                    print("Press Enter to return to main menu...", end="")
                    input()
                    return
                filters.tag = tag
            elif filter_choice == "4":
                # Ask for each filter type
                status_input = input("Filter by status (completed/pending, or press Enter to skip): ").strip().lower()
                if status_input:
                    if status_input in ['completed', 'c']:
                        filters.status = True
                    elif status_input in ['pending', 'p']:
                        filters.status = False
                    else:
                        print("❌ Invalid status. Use 'completed' or 'pending'.")
                        print("Press Enter to return to main menu...", end="")
                        input()
                        return

                priority_input = input("Filter by priority (high/medium/low, or press Enter to skip): ").strip().lower()
                if priority_input:
                    if priority_input in ['high', 'h']:
                        from src.models.priority import Priority
                        filters.priority = Priority.HIGH
                    elif priority_input in ['medium', 'm']:
                        from src.models.priority import Priority
                        filters.priority = Priority.MEDIUM
                    elif priority_input in ['low', 'l']:
                        from src.models.priority import Priority
                        filters.priority = Priority.LOW
                    else:
                        print("❌ Invalid priority. Use 'high', 'medium', or 'low'.")
                        print("Press Enter to return to main menu...", end="")
                        input()
                        return

                tag_input = input("Filter by tag (or press Enter to skip): ").strip()
                if tag_input:
                    filters.tag = tag_input
            else:
                print("❌ Invalid filter option.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            results = self.service.filter_tasks(filters)
            if not results:
                print(f"\n📭 No tasks found matching the filters.")
            else:
                print(f"\n🎯 Found {len(results)} task(s) matching the filters:")
                for task in results:
                    status_emoji = "✅" if task.completed else "⬜"
                    print(f"\n{status_emoji} ID: {task.id} | {task.title}")
                    if task.description:
                        print(f"   Description: {task.description}")
                    if task.priority:
                        print(f"   Priority: {task.priority.value}")
                    if task.tags:
                        print(f"   Tags: {', '.join(task.tags)}")
                    print(f"   Status: {'Completed' if task.completed else 'Pending'}")

            print("\nPress Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error filtering tasks: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_sort_tasks(self) -> None:
        """Handle sorting tasks with guided prompts."""
        try:
            print("\nSort options:")
            print("1. Sort by title (alphabetically)")
            print("2. Sort by priority (high to low)")
            print("3. Sort by due date (earliest first)")
            print("4. Sort by creation date (newest first)")

            sort_choice = input("\nSelect sort option (1-4): ").strip()

            from src.services.todo_service import SortCriteria
            sort_by = SortCriteria.TITLE_ALPHABETICAL  # default

            if sort_choice == "1":
                sort_by = SortCriteria.TITLE_ALPHABETICAL
            elif sort_choice == "2":
                sort_by = SortCriteria.PRIORITY
            elif sort_choice == "3":
                sort_by = SortCriteria.DUE_DATE
            elif sort_choice == "4":
                sort_by = SortCriteria.CREATION_DATE
            else:
                print("❌ Invalid sort option. Use 1-4.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            # Get all tasks and sort them
            all_tasks = self.service.get_all_tasks()
            sorted_tasks = self.service.sort_tasks(all_tasks, sort_by)

            if not sorted_tasks:
                print("\n📭 No tasks to sort.")
            else:
                print(f"\n📊 Tasks sorted by {sort_choice}:")
                sort_name = {
                    SortCriteria.TITLE_ALPHABETICAL: "title (alphabetically)",
                    SortCriteria.PRIORITY: "priority (high to low)",
                    SortCriteria.DUE_DATE: "due date (earliest first)",
                    SortCriteria.CREATION_DATE: "creation date (newest first)"
                }.get(sort_by, "title (alphabetically)")

                print(f"\nSorted by: {sort_name}")
                for task in sorted_tasks:
                    status_emoji = "✅" if task.completed else "⬜"
                    print(f"\n{status_emoji} ID: {task.id} | {task.title}")
                    if task.description:
                        print(f"   Description: {task.description}")
                    if task.priority:
                        print(f"   Priority: {task.priority.value}")
                    if task.tags:
                        print(f"   Tags: {', '.join(task.tags)}")
                    print(f"   Status: {'Completed' if task.completed else 'Pending'}")

            print("\nPress Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error sorting tasks: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_set_priority(self) -> None:
        """Handle setting task priority with guided prompts."""
        try:
            task_id_input = input("Enter task ID to set priority: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            try:
                task = self.service.get_task(task_id)
            except Exception:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            print(f"Current task: {task.title}")
            print(f"Current priority: {task.priority.value if task.priority else 'None'}")

            priority_choice = input("Enter new priority (high/medium/low): ").strip().lower()
            if priority_choice not in ['high', 'medium', 'low', 'h', 'm', 'l']:
                print("❌ Invalid priority. Use 'high', 'medium', or 'low'.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            # Normalize priority input
            if priority_choice in ['high', 'h']:
                from src.models.priority import Priority
                priority = Priority.HIGH
            elif priority_choice in ['medium', 'm']:
                from src.models.priority import Priority
                priority = Priority.MEDIUM
            else:  # low or l
                from src.models.priority import Priority
                priority = Priority.LOW

            updated_task = self.service.set_priority(task_id, priority)
            if updated_task:
                print(f"✅ Priority set to {updated_task.priority.value} for task {task_id}: {updated_task.title}")
            else:
                print(f"❌ Failed to set priority for task {task_id}")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error setting task priority: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_add_tag(self) -> None:
        """Handle adding a tag to a task with guided prompts."""
        try:
            task_id_input = input("Enter task ID to add tag: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            try:
                task = self.service.get_task(task_id)
            except Exception:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            print(f"Current task: {task.title}")
            print(f"Current tags: {', '.join(task.tags) if task.tags else 'None'}")

            tag = input("Enter tag to add: ").strip()
            if not tag:
                print("❌ Tag cannot be empty.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            updated_task = self.service.add_tag(task_id, tag)
            if updated_task:
                print(f"✅ Tag '{tag}' added to task {task_id}: {updated_task.title}")
                print(f"Updated tags: {', '.join(updated_task.tags)}")
            else:
                print(f"❌ Failed to add tag to task {task_id}")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error adding tag to task: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_remove_tag(self) -> None:
        """Handle removing a tag from a task with guided prompts."""
        try:
            task_id_input = input("Enter task ID to remove tag: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            try:
                task = self.service.get_task(task_id)
            except Exception:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            print(f"Current task: {task.title}")
            if not task.tags:
                print("❌ Task has no tags to remove.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            print(f"Current tags: {', '.join(task.tags)}")

            tag = input("Enter tag to remove: ").strip()
            if not tag:
                print("❌ Tag cannot be empty.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            updated_task = self.service.remove_tag(task_id, tag)
            if updated_task:
                print(f"✅ Tag '{tag}' removed from task {task_id}: {updated_task.title}")
                if updated_task.tags:
                    print(f"Remaining tags: {', '.join(updated_task.tags)}")
                else:
                    print("No tags remaining.")
            else:
                print(f"❌ Failed to remove tag from task {task_id}")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error removing tag from task: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_set_recurring_task(self) -> None:
        """Handle setting a task as recurring with guided prompts."""
        try:
            task_id_input = input("Enter task ID to set as recurring: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            try:
                task = self.service.get_task(task_id)
                if not task:
                    print(f"❌ Task with ID {task_id} not found.")
                    print("Press Enter to return to main menu...", end="")
                    input()
                    return
            except Exception:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            print(f"Current task: {task.title}")
            if task.description:
                print(f"Description: {task.description}")

            # Ask for recurrence pattern
            print("\nSelect recurrence pattern:")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")

            pattern_choice = input("Enter choice (1-3): ").strip()
            pattern_map = {"1": "daily", "2": "weekly", "3": "monthly"}

            if pattern_choice not in pattern_map:
                print("❌ Invalid choice. Please select 1, 2, or 3.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            recurrence_pattern = pattern_map[pattern_choice]

            # Ask for recurrence interval
            interval_input = input("Enter recurrence interval (default 1): ").strip()
            if interval_input and interval_input.isdigit():
                recurrence_interval = int(interval_input)
                if recurrence_interval <= 0:
                    print("❌ Interval must be a positive number.")
                    print("Press Enter to return to main menu...", end="")
                    input()
                    return
            else:
                recurrence_interval = 1  # default

            # Use the domain service to create recurring task
            recurring_task = self.service.create_recurring_task(
                title=task.title,
                description=task.description,
                recurrence_pattern=recurrence_pattern,
                recurrence_interval=recurrence_interval
            )

            if recurring_task:
                print(f"✅ Task {task_id} set as recurring:")
                print(f"   Pattern: {recurring_task.recurrence_pattern}")
                print(f"   Interval: {recurring_task.recurrence_interval}")
                print(f"   Next due date: {recurring_task.next_due_date}")
            else:
                print(f"❌ Failed to set task {task_id} as recurring")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error setting task as recurring: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_set_update_due_date(self) -> None:
        """Handle setting or updating a task's due date with guided prompts."""
        try:
            task_id_input = input("Enter task ID to set/update due date: ").strip()
            if not task_id_input.isdigit():
                print("❌ Task ID must be a number.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            task_id = int(task_id_input)

            # Check if task exists
            try:
                task = self.service.get_task(task_id)
                if not task:
                    print(f"❌ Task with ID {task_id} not found.")
                    print("Press Enter to return to main menu...", end="")
                    input()
                    return
            except Exception:
                print(f"❌ Task with ID {task_id} not found.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            print(f"Current task: {task.title}")
            if task.description:
                print(f"Description: {task.description}")

            # Ask for due date in YYYY-MM-DD format
            due_date_input = input("Enter due date (YYYY-MM-DD format): ").strip()
            if not due_date_input:
                print("❌ Due date cannot be empty.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            # Validate date format
            from datetime import datetime
            try:
                due_date = datetime.strptime(due_date_input, "%Y-%m-%d")
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD format.")
                print("Press Enter to return to main menu...", end="")
                input()
                return

            # For now, we'll update the task with the due date by creating a new recurring task with due date
            # Since the models layer doesn't have due date functionality built-in, we'll update the description
            # or if it's a recurring task, we'll update the next_due_date

            # First, check if this is already a recurring task
            recurring_task = self.service.domain_storage.get_task(task_id)
            if recurring_task and recurring_task.is_recurring:
                # Update the recurring task's next due date
                recurring_task.next_due_date = due_date
                success = self.service.domain_storage.update_task(task_id, recurring_task)
                if success:
                    print(f"✅ Due date updated for recurring task {task_id}: {due_date_input}")
                else:
                    print(f"❌ Failed to update due date for task {task_id}")
            else:
                # For regular tasks, we'll update the description to include the due date
                # or create a recurring task if user wants it recurring
                print("Would you like to make this task recurring? (y/N): ", end="")
                make_recurring = input().strip().lower()

                if make_recurring in ['y', 'yes']:
                    print("\nSelect recurrence pattern:")
                    print("1. Daily")
                    print("2. Weekly")
                    print("3. Monthly")

                    pattern_choice = input("Enter choice (1-3): ").strip()
                    pattern_map = {"1": "daily", "2": "weekly", "3": "monthly"}

                    if pattern_choice not in pattern_map:
                        print("❌ Invalid choice. Please select 1, 2, or 3.")
                        print("Press Enter to return to main menu...", end="")
                        input()
                        return

                    recurrence_pattern = pattern_map[pattern_choice]

                    interval_input = input("Enter recurrence interval (default 1): ").strip()
                    if interval_input and interval_input.isdigit():
                        recurrence_interval = int(interval_input)
                        if recurrence_interval <= 0:
                            print("❌ Interval must be a positive number.")
                            print("Press Enter to return to main menu...", end="")
                            input()
                            return
                    else:
                        recurrence_interval = 1  # default

                    # Create recurring task with due date
                    recurring_task = self.service.create_recurring_task(
                        title=task.title,
                        description=task.description,
                        recurrence_pattern=recurrence_pattern,
                        recurrence_interval=recurrence_interval
                    )

                    # Update the next due date to the specified date
                    recurring_task.next_due_date = due_date
                    success = self.service.domain_storage.update_task(recurring_task.id, recurring_task)

                    if success:
                        print(f"✅ Task {task_id} converted to recurring with due date: {due_date_input}")
                    else:
                        print(f"❌ Failed to update task {task_id} with due date")
                else:
                    # Just update the description to mention the due date
                    if task.description:
                        updated_description = f"{task.description} [Due: {due_date_input}]"
                    else:
                        updated_description = f"[Due: {due_date_input}]"

                    updated_task = self.service.update_task(task_id, description=updated_description)
                    if updated_task:
                        print(f"✅ Due date added to task {task_id} description: {due_date_input}")
                    else:
                        print(f"❌ Failed to update task {task_id} with due date")

            print("Press Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error setting/updating due date: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()

    def handle_view_upcoming_recurring_tasks(self) -> None:
        """Handle viewing upcoming recurring tasks with guided prompts."""
        try:
            # Get recurring tasks from the domain service
            recurring_service = self.service.recurring_service
            all_recurring_tasks = recurring_service.get_recurring_tasks()

            if not all_recurring_tasks:
                print("\n🔔 No recurring tasks found.")
            else:
                print(f"\n🔔 Found {len(all_recurring_tasks)} recurring task(s):")
                for task in all_recurring_tasks:
                    status_emoji = "✅" if task.completed else "⬜"
                    print(f"\n{status_emoji} ID: {task.id} | {task.title}")
                    print(f"   Pattern: {task.recurrence_pattern}")
                    print(f"   Interval: {task.recurrence_interval}")
                    if task.next_due_date:
                        print(f"   Next due: {task.next_due_date}")
                    print(f"   Active: {task.is_active}")
                    if task.description:
                        print(f"   Description: {task.description}")

            print("\nPress Enter to return to main menu...", end="")
            input()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"❌ Error viewing upcoming recurring tasks: {str(e)}")
            print("Press Enter to return to main menu...", end="")
            input()


def main():
    """Main entry point for the interactive todo CLI application."""
    cli = TodoCLI()
    # Run interactive mode only
    cli.run_interactive()


if __name__ == "__main__":
    main()