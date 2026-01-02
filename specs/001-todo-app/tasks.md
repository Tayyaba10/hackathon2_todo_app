---
description: "Task list for todo application implementation"
---

# Tasks: In-Memory Todo Console Application

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/
- [X] T002 [P] Create src/domain/__init__.py
- [X] T003 [P] Create src/domain/entities/__init__.py
- [X] T004 [P] Create src/domain/exceptions/__init__.py
- [X] T005 [P] Create src/services/__init__.py
- [X] T006 [P] Create src/services/interfaces/__init__.py
- [X] T007 [P] Create src/infrastructure/__init__.py
- [X] T008 [P] Create src/infrastructure/storage/__init__.py
- [X] T009 [P] Create src/cli/__init__.py
- [X] T010 [P] Create tests/__init__.py
- [X] T011 [P] Create tests/unit/__init__.py
- [X] T012 [P] Create tests/unit/domain/__init__.py
- [X] T013 [P] Create tests/unit/services/__init__.py
- [X] T014 [P] Create tests/unit/infrastructure/__init__.py
- [X] T015 [P] Create tests/integration/__init__.py
- [X] T016 [P] Create tests/integration/cli/__init__.py
- [X] T017 [P] Create tests/contract/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T018 [P] Create Task entity in src/domain/entities/task.py with id, title, description, completed, created_at fields
- [X] T019 [P] Create TodoException base class in src/domain/exceptions/todo_exceptions.py
- [X] T020 [P] Create InvalidTaskError in src/domain/exceptions/todo_exceptions.py
- [X] T021 [P] Create TaskNotFoundError in src/domain/exceptions/todo_exceptions.py
- [X] T022 [P] Create StorageInterface in src/services/interfaces/storage_interface.py
- [X] T023 Create TaskCollection entity in src/domain/entities/task_collection.py with tasks dict and next_id
- [X] T024 Implement in-memory storage in src/infrastructure/storage/in_memory_storage.py
- [X] T025 Create TodoService in src/services/todo_service.py with all required methods

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks with a title and description during their session.

**Independent Test**: Can be fully tested by adding a task and verifying it appears in the task list, delivering the core value of task creation.

### Implementation for User Story 1

- [X] T026 [P] [US1] Add add_task method to TodoService in src/services/todo_service.py
- [X] T027 [P] [US1] Add validation for empty title in add_task method
- [X] T028 [US1] Create CLI command for adding tasks in src/cli/todo_cli.py
- [ ] T029 [US1] Test adding a task with valid title and description
- [ ] T030 [US1] Test adding a task with empty title (should fail)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can see all their tasks with their completion status to manage their work effectively.

**Independent Test**: Can be fully tested by adding tasks and viewing the complete list, delivering the value of task visibility.

### Implementation for User Story 2

- [X] T031 [P] [US2] Add get_all_tasks method to TodoService in src/services/todo_service.py
- [X] T032 [P] [US2] Add get_task method to TodoService in src/services/todo_service.py
- [X] T033 [US2] Create CLI command for viewing all tasks in src/cli/todo_cli.py
- [X] T034 [US2] Format task display with ID, title, description, and completion status
- [ ] T035 [US2] Test viewing all tasks when tasks exist
- [ ] T036 [US2] Test viewing all tasks when no tasks exist

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P2)

**Goal**: Users can modify existing tasks to reflect changes in their requirements or details.

**Independent Test**: Can be fully tested by updating a task and verifying changes are reflected, delivering the value of task modification.

### Implementation for User Story 3

- [X] T037 [P] [US3] Add update_task method to TodoService in src/services/todo_service.py
- [X] T038 [P] [US3] Add validation for updating non-existent task in update_task method
- [X] T039 [US3] Create CLI command for updating tasks in src/cli/todo_cli.py
- [ ] T040 [US3] Test updating an existing task with valid ID and new details
- [ ] T041 [US3] Test updating a non-existent task (should fail)

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Task (Priority: P2)

**Goal**: Users can remove tasks they no longer need to keep their task list manageable.

**Independent Test**: Can be fully tested by deleting a task and verifying it's removed from the list, delivering the value of task cleanup.

### Implementation for User Story 4

- [X] T042 [P] [US4] Add delete_task method to TodoService in src/services/todo_service.py
- [X] T043 [P] [US4] Add validation for deleting non-existent task in delete_task method
- [X] T044 [US4] Create CLI command for deleting tasks in src/cli/todo_cli.py
- [ ] T045 [US4] Test deleting an existing task with valid ID
- [ ] T046 [US4] Test deleting a non-existent task (should fail)

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can track the completion status of their tasks to manage their progress.

**Independent Test**: Can be fully tested by marking tasks as complete/incomplete and verifying status changes, delivering the value of progress tracking.

### Implementation for User Story 5

- [X] T047 [P] [US5] Add mark_task_complete method to TodoService in src/services/todo_service.py
- [X] T048 [P] [US5] Add mark_task_incomplete method to TodoService in src/services/todo_service.py
- [X] T049 [P] [US5] Add validation for marking non-existent task status in both methods
- [X] T050 [US5] Create CLI commands for marking tasks complete/incomplete in src/cli/todo_cli.py
- [ ] T051 [US5] Test marking an incomplete task as complete
- [ ] T052 [US5] Test marking a completed task as incomplete

**Checkpoint**: At this point, User Stories 1, 2, 3, 4 AND 5 should all work independently

---

## Phase 8: User Story 6 - Console Interface Navigation (Priority: P1)

**Goal**: Users can interact with the application through an intuitive command-based interface.

**Independent Test**: Can be fully tested by navigating through all available commands, delivering the value of accessible functionality.

### Implementation for User Story 6

- [X] T053 [P] [US6] Implement main CLI loop in src/cli/todo_cli.py
- [X] T054 [P] [US6] Add command parsing for all required operations in src/cli/todo_cli.py
- [X] T055 [P] [US6] Add help command implementation in src/cli/todo_cli.py
- [X] T056 [P] [US6] Add exit command implementation in src/cli/todo_cli.py
- [X] T057 [US6] Add error handling for invalid commands
- [X] T058 [US6] Add error handling for invalid task IDs

- [ ] T059 [US6] Test all CLI commands work correctly
- [ ] T060 [US6] Test error handling for invalid inputs

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T061 [P] Add proper logging throughout the application
- [ ] T062 [P] Add type hints to all public interfaces
- [ ] T063 [P] Add docstrings to all public methods
- [ ] T064 [P] Add unit tests for all domain entities
- [ ] T065 [P] Add unit tests for all service methods
- [ ] T066 [P] Add integration tests for CLI functionality
- [ ] T067 [P] Add contract tests for service interface
- [X] T068 [P] Create main entry point for the application
- [ ] T069 [P] Add configuration for command-line arguments
- [ ] T070 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable
- **User Story 6 (P1)**: Can start after Foundational (Phase 2) - Integrates all other stories but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 6 - Core Functionality)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View All Tasks)
5. Complete Phase 8: User Story 6 (Console Interface Navigation)
6. **STOP and VALIDATE**: Test core functionality independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Stories 1, 2, 6 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 → Test independently → Deploy/Demo
4. Add User Story 4 → Test independently → Deploy/Demo
5. Add User Story 5 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 & 2
   - Developer B: User Story 3 & 4
   - Developer C: User Story 5 & 6
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence