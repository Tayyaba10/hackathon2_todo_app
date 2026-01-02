# Todo Application with Organizational Features

This is a command-line todo application that helps you manage tasks with advanced organizational features including priorities, tags, search, filtering, and sorting.

## Features

### Basic Task Management
- Add, update, complete, and delete tasks
- View all tasks with their status

### Organizational Features
- **Priorities**: Assign high, medium, or low priority to tasks
- **Tags**: Categorize tasks with multiple tags
- **Search**: Find tasks by keywords in title or description
- **Filter**: View tasks by status, priority, or tags
- **Sort**: Order tasks alphabetically, by priority, or by due date

## Installation

1. Make sure you have Python 3.13+ installed
2. Clone this repository
3. Navigate to the project directory

## Usage

### Adding a Task
```bash
python -m src.cli add "Task title" --description "Task description" --priority high --tags work urgent --due-date 2025-12-31
```

### Listing Tasks
```bash
python -m src.cli list
```

Filter and sort tasks:
```bash
# Filter by priority
python -m src.cli list --priority high

# Filter by tag
python -m src.cli list --tag work

# Filter by status
python -m src.cli list --status completed

# Sort tasks
python -m src.cli list --sort priority

# Search tasks
python -m src.cli list --search "keyword"

# Combine filters and search
python -m src.cli list --priority high --tag work --sort title --search "project"
```

### Setting Task Priority
```bash
python -m src.cli priority 1 high
```

### Adding Tags to a Task
```bash
python -m src.cli add-tag 1 work
```

### Removing Tags from a Task
```bash
python -m src.cli remove-tag 1 work
```

### Completing a Task
```bash
python -m src.cli complete 1
```

### Updating a Task
```bash
python -m src.cli update 1 --title "New title" --description "New description"
```

### Deleting a Task
```bash
python -m src.cli delete 1
```

## Examples

### Add a high-priority work task with tags
```bash
python -m src.cli add "Complete project proposal" --description "Finish the Q4 project proposal" --priority high --tags work urgent --due-date 2025-01-15
```

### Find and view all urgent tasks
```bash
python -m src.cli list --tag urgent --sort priority
```

### Search for tasks related to a specific project
```bash
python -m src.cli list --search "project" --sort title
```

## Architecture

The application follows clean architecture principles:

- **Models** (`src/models/`): Task and Priority definitions
- **Services** (`src/services/`): Business logic for task management
- **CLI** (`src/cli/`): Command-line interface
- **Tests** (`tests/`): Unit and integration tests

## Running Tests

To run the tests:
```bash
python -m pytest tests/
```

## License

MIT License