# Data Model: Advanced Level Recurring Tasks

## Entity: RecurringTask

### Properties
- **taskId**: string - Unique identifier for the task (inherited from base Task)
- **title**: string - Task description (inherited from base Task)
- **description**: string - Detailed task information (inherited from base Task)
- **status**: string - Task status (e.g., "pending", "completed") (inherited from base Task)
- **priority**: string - Task priority (e.g., "low", "medium", "high") (inherited from base Task if Intermediate Level exists)
- **tags**: array of strings - Task categorization tags (inherited from base Task if Intermediate Level exists)
- **dueDate**: string - Due date in ISO 8601 format (inherited from base Task if due dates exist)
- **createdAt**: string - Creation timestamp in ISO 8601 format (inherited from base Task)
- **completedAt**: string - Completion timestamp in ISO 8601 format (inherited from base Task)
- **recurrencePattern**: string - Interval type ("daily", "weekly", "monthly")
- **recurrenceInterval**: number - Number of units for the interval (default: 1)
- **nextDueDate**: string - When the next instance is due in ISO 8601 format
- **isActive**: boolean - Whether recurrence is currently active (default: true)
- **parentId**: string - For child instances, identifies the original recurring task (null for original)
- **originalTaskId**: string - For any instance, identifies the original recurring task template

### Validation Rules
- **recurrencePattern** must be one of: "daily", "weekly", "monthly"
- **recurrenceInterval** must be a positive integer
- **nextDueDate** must be a valid ISO 8601 date string
- **isActive** must be a boolean
- **parentId** and **originalTaskId** must be valid task IDs or null
- **taskId** must be unique across all tasks

### State Transitions
- When a recurring task is marked as complete:
  - If **isActive** is true, calculate and set **nextDueDate**
  - Generate a new task instance with the same properties (except taskId and dates)
- When recurrence is canceled:
  - Set **isActive** to false
  - Do not generate new instances after completion

## Entity: Task (Extended)

### Additional Properties for Recurring Tasks
- **isRecurring**: boolean - Indicates if the task is part of a recurring series (default: false)
- **recurrenceId**: string - Reference to the recurring task template (for child instances)

### Validation Rules
- If **isRecurring** is true, then **recurrenceId** must be a valid recurring task ID
- If **isRecurring** is false, then **recurrenceId** must be null or undefined

## Relationships

### RecurringTask to Task Instances
- One RecurringTask can generate multiple Task instances
- Each Task instance has a reference back to its RecurringTask template
- The relationship is hierarchical: original RecurringTask -> generated Task instances

### Storage Format
The data will be stored in the existing JSON format with additional fields for recurring tasks:

```json
{
  "tasks": [
    {
      "taskId": "task-123",
      "title": "Daily Exercise",
      "description": "Go for a 30-minute run",
      "status": "pending",
      "priority": "high",
      "tags": ["health", "exercise"],
      "dueDate": "2026-01-02T08:00:00Z",
      "createdAt": "2026-01-01T10:00:00Z",
      "completedAt": null,
      "isRecurring": true,
      "recurrencePattern": "daily",
      "recurrenceInterval": 1,
      "nextDueDate": "2026-01-02T08:00:00Z",
      "isActive": true,
      "parentId": null,
      "originalTaskId": "task-123"
    },
    {
      "taskId": "task-456",
      "title": "Daily Exercise",
      "description": "Go for a 30-minute run",
      "status": "pending",
      "priority": "high",
      "tags": ["health", "exercise"],
      "dueDate": "2026-01-03T08:00:00Z",
      "createdAt": "2026-01-02T08:00:00Z",
      "completedAt": null,
      "isRecurring": true,
      "recurrenceId": "task-123",
      "isChildInstance": true
    }
  ]
}
```

## Backward Compatibility
- All new properties are optional for existing tasks
- Existing task data remains unchanged
- The system maintains full compatibility with Basic and Intermediate Level tasks
- Old task objects without recurrence properties are treated as non-recurring tasks