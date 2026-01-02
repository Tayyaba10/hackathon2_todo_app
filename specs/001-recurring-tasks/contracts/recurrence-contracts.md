# API Contracts: Advanced Level Recurring Tasks

## Task Creation with Recurrence

### Endpoint: `POST /tasks`
**Purpose**: Create a new task, optionally with recurring properties

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "priority": "low|medium|high",
  "tags": ["string"],
  "dueDate": "string (ISO 8601)",
  "isRecurring": "boolean (optional)",
  "recurrencePattern": "daily|weekly|monthly (required if isRecurring=true)",
  "recurrenceInterval": "number (optional, default=1)",
  "isActive": "boolean (optional, default=true)"
}
```

**Response**:
```json
{
  "taskId": "string",
  "title": "string",
  "description": "string",
  "status": "pending|completed",
  "priority": "low|medium|high",
  "tags": ["string"],
  "dueDate": "string (ISO 8601)",
  "createdAt": "string (ISO 8601)",
  "completedAt": "string (ISO 8601) or null",
  "isRecurring": "boolean",
  "recurrencePattern": "string or null",
  "recurrenceInterval": "number or null",
  "nextDueDate": "string (ISO 8601) or null",
  "isActive": "boolean",
  "parentId": "string or null",
  "originalTaskId": "string or null"
}
```

## Update Recurrence Settings

### Endpoint: `PUT /tasks/{taskId}/recurrence`
**Purpose**: Update recurrence settings for an existing recurring task

**Request Body**:
```json
{
  "recurrencePattern": "daily|weekly|monthly",
  "recurrenceInterval": "number",
  "isActive": "boolean"
}
```

**Response**: Updated task object with recurrence properties

## Cancel Recurrence

### Endpoint: `DELETE /tasks/{taskId}/recurrence`
**Purpose**: Cancel recurrence for a recurring task (keeps existing instances)

**Response**: Success confirmation with updated task status

## Generate Next Instance

### Endpoint: `POST /tasks/{taskId}/generate-next`
**Purpose**: Manually trigger generation of the next instance for a recurring task

**Response**: New task instance object

## CLI Commands Extension

### Command: `todo add <title> --recurring --pattern <daily|weekly|monthly> [--interval <number>]`
**Purpose**: Add a new recurring task

### Command: `todo cancel-recurrence <taskId>`
**Purpose**: Cancel recurrence for a recurring task

### Command: `todo complete <taskId>` (extended behavior)
**Purpose**: Complete a task; if recurring, generate next instance automatically