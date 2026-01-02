# Todo API Contract

## Overview
This contract defines the expected behavior and interfaces for the todo application services.

## Service Interface: TodoService

### Methods

#### `add_task(title: str, description: str = "") -> int`
- **Purpose**: Add a new task to the system
- **Parameters**:
  - `title`: Required string title for the task
  - `description`: Optional string description for the task
- **Returns**: Integer ID of the newly created task
- **Exceptions**: Raises `InvalidTaskError` if title is empty
- **Preconditions**: Title must not be empty
- **Postconditions**: Task is added to the system with unique ID and completion status False

#### `get_all_tasks() -> List[Task]`
- **Purpose**: Retrieve all tasks in the system
- **Parameters**: None
- **Returns**: List of all Task objects in the system
- **Exceptions**: None
- **Preconditions**: None
- **Postconditions**: Returns complete list of tasks

#### `get_task(task_id: int) -> Task`
- **Purpose**: Retrieve a specific task by ID
- **Parameters**:
  - `task_id`: Integer ID of the task to retrieve
- **Returns**: Task object if found
- **Exceptions**: Raises `TaskNotFoundError` if task with given ID doesn't exist
- **Preconditions**: Task with ID must exist
- **Postconditions**: Returns the specific Task object

#### `update_task(task_id: int, title: str = None, description: str = None) -> bool`
- **Purpose**: Update an existing task
- **Parameters**:
  - `task_id`: Integer ID of the task to update
  - `title`: Optional new title for the task
  - `description`: Optional new description for the task
- **Returns**: Boolean indicating success (True) or failure (False)
- **Exceptions**: Raises `TaskNotFoundError` if task with given ID doesn't exist
- **Preconditions**: Task with ID must exist
- **Postconditions**: Task is updated with provided values

#### `delete_task(task_id: int) -> bool`
- **Purpose**: Delete a task from the system
- **Parameters**:
  - `task_id`: Integer ID of the task to delete
- **Returns**: Boolean indicating success (True) or failure (False)
- **Exceptions**: Raises `TaskNotFoundError` if task with given ID doesn't exist
- **Preconditions**: Task with ID must exist
- **Postconditions**: Task is removed from the system

#### `mark_task_complete(task_id: int) -> bool`
- **Purpose**: Mark a task as complete
- **Parameters**:
  - `task_id`: Integer ID of the task to mark complete
- **Returns**: Boolean indicating success (True) or failure (False)
- **Exceptions**: Raises `TaskNotFoundError` if task with given ID doesn't exist
- **Preconditions**: Task with ID must exist
- **Postconditions**: Task completion status is set to True

#### `mark_task_incomplete(task_id: int) -> bool`
- **Purpose**: Mark a task as incomplete
- **Parameters**:
  - `task_id`: Integer ID of the task to mark incomplete
- **Returns**: Boolean indicating success (True) or failure (False)
- **Exceptions**: Raises `TaskNotFoundError` if task with given ID doesn't exist
- **Preconditions**: Task with ID must exist
- **Postconditions**: Task completion status is set to False

## Storage Interface: StorageInterface

### Methods

#### `save_task(task: Task) -> int`
- **Purpose**: Save a task to storage
- **Parameters**:
  - `task`: Task object to save
- **Returns**: Integer ID of the saved task
- **Exceptions**: Raises appropriate storage error if save fails

#### `get_task(task_id: int) -> Task`
- **Purpose**: Retrieve a task from storage
- **Parameters**:
  - `task_id`: Integer ID of the task to retrieve
- **Returns**: Task object if found
- **Exceptions**: Raises appropriate storage error if task not found

#### `get_all_tasks() -> List[Task]`
- **Purpose**: Retrieve all tasks from storage
- **Parameters**: None
- **Returns**: List of all Task objects in storage
- **Exceptions**: None

#### `update_task(task_id: int, updated_task: Task) -> bool`
- **Purpose**: Update a task in storage
- **Parameters**:
  - `task_id`: Integer ID of the task to update
  - `updated_task`: Updated Task object
- **Returns**: Boolean indicating success (True) or failure (False)
- **Exceptions**: Raises appropriate storage error if update fails

#### `delete_task(task_id: int) -> bool`
- **Purpose**: Delete a task from storage
- **Parameters**:
  - `task_id`: Integer ID of the task to delete
- **Returns**: Boolean indicating success (True) or failure (False)
- **Exceptions**: Raises appropriate storage error if delete fails