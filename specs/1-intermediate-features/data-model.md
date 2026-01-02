# Data Model: Intermediate Level Organization & Usability Features

## Extended Task Model

### Task Entity
**Purpose**: Represents a user task with additional organizational features

**Fields**:
- `id: int` - Unique identifier (maintains existing approach)
- `title: str` - Task title (maintains existing approach)
- `description: str` - Task description (maintains existing approach)
- `completed: bool` - Completion status (maintains existing approach)
- `priority: Priority` - Task priority level (new field)
- `tags: List[str]` - List of tags associated with the task (new field)
- `created_at: datetime` - Creation timestamp (maintains existing approach)
- `updated_at: datetime` - Last update timestamp (maintains existing approach)
- `due_date: Optional[datetime]` - Optional due date (if exists from basic level)

### Priority Enum
**Purpose**: Defines the priority levels for tasks

**Values**:
- `HIGH = "high"` - High priority tasks
- `MEDIUM = "medium"` - Medium priority tasks
- `LOW = "low"` - Low priority tasks

### Validation Rules
- Priority must be one of the defined enum values
- Tags must be non-empty strings
- Tags list must not contain duplicates
- Task must maintain all existing validation rules from Basic Level

## Service Layer Extensions

### TodoService Extensions
**Purpose**: Extended service to handle new organizational features

**New Methods**:
- `set_priority(task_id: int, priority: Priority) -> Task` - Set priority for a task
- `add_tag(task_id: int, tag: str) -> Task` - Add a tag to a task
- `remove_tag(task_id: int, tag: str) -> Task` - Remove a tag from a task
- `search_tasks(query: str) -> List[Task]` - Search tasks by title/description
- `filter_tasks(filters: TaskFilters) -> List[Task]` - Filter tasks by criteria
- `sort_tasks(tasks: List[Task], sort_by: SortCriteria) -> List[Task]` - Sort tasks

### SearchService
**Purpose**: Dedicated service for search functionality

**Methods**:
- `search_by_keyword(tasks: List[Task], keyword: str) -> List[Task]` - Search tasks by keyword in title and description
- `search_by_multiple_keywords(tasks: List[Task], keywords: List[str]) -> List[Task]` - Search with multiple keywords

### Filter Criteria
**Purpose**: Defines filter parameters for task filtering

**Fields**:
- `status: Optional[bool]` - Filter by completion status
- `priority: Optional[Priority]` - Filter by priority level
- `tag: Optional[str]` - Filter by specific tag
- `due_date: Optional[datetime]` - Filter by due date

### Sort Criteria
**Purpose**: Defines sorting parameters for task sorting

**Options**:
- `TITLE_ALPHABETICAL` - Sort by title alphabetically
- `PRIORITY` - Sort by priority (high to low)
- `DUE_DATE` - Sort by due date (earliest first)
- `CREATION_DATE` - Sort by creation date (newest first)