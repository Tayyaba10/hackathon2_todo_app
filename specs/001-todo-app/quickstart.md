# Quickstart Guide: In-Memory Todo Console Application

## Getting Started

This guide will help you get up and running with the todo console application.

### Prerequisites

- Python 3.13+ installed on your system
- Basic command-line knowledge

### Installation

1. Clone or download the project repository
2. Navigate to the project root directory
3. Ensure Python 3.13+ is available in your environment

### Running the Application

To start the todo application, run:

```bash
python -m src.cli.todo_cli
```

### Basic Usage

Once the application starts, you'll see a command prompt where you can enter commands:

#### Adding a Task
```
add "Task Title" "Task Description"
```

#### Viewing All Tasks
```
list
```

#### Updating a Task
```
update 1 "New Title" "New Description"
```

#### Deleting a Task
```
delete 1
```

#### Marking Task as Complete
```
complete 1
```

#### Marking Task as Incomplete
```
incomplete 1
```

#### Getting Help
```
help
```

#### Exiting the Application
```
exit
```

### Example Workflow

1. Start the application
2. Add a few tasks:
   ```
   add "Buy groceries" "Milk, bread, eggs"
   add "Finish report" "Complete the quarterly report"
   ```
3. View your tasks:
   ```
   list
   ```
4. Mark a task as complete:
   ```
   complete 1
   ```
5. Exit when done:
   ```
   exit
   ```

### Error Handling

- Invalid commands will show an error message and return to the prompt
- Invalid task IDs will show an appropriate error message
- Empty titles will be rejected during task creation
- The application will not crash on invalid inputs

### Notes

- All data is stored in-memory only and will be lost when the application exits
- Task IDs are automatically assigned and are unique during the session
- The application supports all five core features: add, list, update, delete, complete/incomplete