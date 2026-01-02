# Data Model: In-Memory Todo Console Application

## Entity: Task

**Description**: Represents a user task in the todo application

**Fields**:
- `id` (int): Unique identifier for the task, automatically assigned
- `title` (str): Required title of the task
- `description` (str): Optional description of the task
- `completed` (bool): Status indicating whether the task is completed (default: False)
- `created_at` (datetime): Timestamp when the task was created

**Validation Rules**:
- `title` must not be empty or None
- `id` must be unique within the application session
- `completed` must be a boolean value

**State Transitions**:
- New task: `completed = False` by default
- Mark complete: `completed = True`
- Mark incomplete: `completed = False`

## Entity: TaskCollection

**Description**: Represents a collection of tasks managed by the application

**Fields**:
- `tasks` (dict): Dictionary mapping task IDs to Task objects
- `next_id` (int): Counter for generating unique task IDs

**Validation Rules**:
- Task IDs must be unique within the collection
- No duplicate IDs allowed
- Maximum efficiency for add, update, delete, and retrieve operations

## Relationships
- TaskCollection contains multiple Task entities
- Each Task has a unique ID within the TaskCollection