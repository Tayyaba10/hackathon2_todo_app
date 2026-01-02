# Quickstart Guide: Interactive CLI for Todo Application

## Getting Started

This guide will help you use the interactive todo application with its menu-driven interface.

### Prerequisites

- Python 3.13+ installed on your system
- Basic command-line knowledge

### Running the Application

To start the interactive todo application, run:

```bash
python -m src.cli.todo_cli
```

### Interactive Menu Usage

Once the application starts, you'll see a numbered menu with emoji indicators:

```
📝 Welcome to Todo App!

1️⃣  ➕ Add a new task
2️⃣  📋 View all tasks
3️⃣  ✏️ Update a task
4️⃣  ✅ Mark task as complete
5️⃣  🔄 Mark task as incomplete
6️⃣  🗑️ Delete a task
7️⃣  ❓ Help
0️⃣  🚪 Exit
```

### Available Operations

#### Adding a Task
1. Select option "1" or "1️⃣"
2. Enter the task title when prompted
3. Enter the task description when prompted (optional)
4. The system will confirm the task was added and return to the main menu

#### Viewing All Tasks
1. Select option "2" or "2️⃣"
2. The system will display all tasks with their ID, title, description, and status
3. Each task will show its status with emojis: ⬜ for incomplete, ✅ for complete
4. The system will return to the main menu automatically

#### Updating a Task
1. Select option "3" or "3️⃣"
2. Enter the task ID when prompted
3. Enter the new title when prompted
4. Enter the new description when prompted (optional)
5. The system will confirm the task was updated and return to the main menu

#### Marking Task as Complete
1. Select option "4" or "4️⃣"
2. Enter the task ID when prompted
3. The system will confirm the task was marked as complete and return to the main menu

#### Marking Task as Incomplete
1. Select option "5" or "5️⃣"
2. Enter the task ID when prompted
3. The system will confirm the task was marked as incomplete and return to the main menu

#### Deleting a Task
1. Select option "6" or "6️⃣"
2. Enter the task ID when prompted
3. The system will confirm the task was deleted and return to the main menu

#### Getting Help
1. Select option "7" or "7️⃣"
2. The system will display help information and return to the main menu

#### Exiting the Application
1. Select option "0" or "0️⃣"
2. The application will close

### Example Workflow

1. Start the application
2. Add a few tasks using option 1
3. View your tasks using option 2
4. Mark a task as complete using option 4
5. Exit using option 0

### Error Handling

- Invalid menu choices will show a friendly error message and return to the main menu
- Invalid task IDs will show a friendly error message and return to the main menu
- Empty titles during task creation will show a friendly error message and return to the main menu
- The application will not crash on invalid inputs

### Notes

- All data is stored in-memory only and will be lost when the application exits
- Task IDs are automatically assigned and are unique during the session
- The application supports all five core features through the interactive menu system
- No command-line syntax knowledge required - just select numbered options