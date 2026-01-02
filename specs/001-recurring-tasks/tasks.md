---
description: "Task list for Advanced Level Recurring Tasks feature implementation"
---

# Tasks: Advanced Level Recurring Tasks

**Input**: Design documents from `/specs/001-recurring-tasks/`
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

- [ ] T001 Create project structure per implementation plan in src/models/, src/services/, src/cli/
- [ ] T002 Initialize Python 3.11 project with appropriate dependencies
- [ ] T003 [P] Configure linting and formatting tools for Python project

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Extend existing Task model with recurring task properties in src/domain/entities/task.py
- [X] T005 [P] Create RecurringTask model in src/services/recurring_service.py
- [X] T006 [P] Setup storage framework to handle recurring task data
- [X] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Setting up a recurring task (Priority: P1) 🎯 MVP

**Goal**: Allow users to create tasks that automatically repeat at specified intervals (daily, weekly, monthly)

**Independent Test**: User can create a recurring task with a specific interval and see it marked as recurring in the interface

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for recurring task creation endpoint in tests/contract/test_recurring_tasks.py
- [ ] T011 [P] [US1] Integration test for creating recurring task in tests/integration/test_recurring_tasks.py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Extend Task model with recurrence properties in src/models/task.py
- [ ] T013 [P] [US1] Create RecurringTask model with validation in src/models/recurring_task.py
- [ ] T014 [US1] Implement RecurringTaskService in src/services/recurring_service.py
- [ ] T015 [US1] Add recurring task creation to CLI commands in src/cli/commands.py
- [ ] T016 [US1] Add validation and error handling for recurrence settings
- [ ] T017 [US1] Add logging for recurring task creation operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Completing a recurring task (Priority: P2)

**Goal**: When a recurring task is marked as complete, automatically generate the next instance based on the recurrence interval

**Independent Test**: When user marks a recurring task as complete, a new instance appears in the task list with the correct due date

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for task completion with recurrence logic in tests/contract/test_task_completion.py
- [ ] T019 [P] [US2] Integration test for recurring task completion and generation in tests/integration/test_task_completion.py

### Implementation for User Story 2

- [X] T020 [P] [US2] Implement recurring task generation logic in src/services/recurring_service.py
- [X] T021 [US2] Update TaskService to handle recurring task completion in src/services/domain_todo_service.py
- [X] T022 [US2] Modify complete command to handle recurring tasks in src/cli/cli.py
- [X] T023 [US2] Add date calculation utilities for recurrence intervals in src/lib/utils.py
- [X] T024 [US2] Implement duplicate prevention for recurring task generation

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Managing recurring task settings (Priority: P3)

**Goal**: Allow users to modify or cancel recurrence settings for existing recurring tasks

**Independent Test**: User can access recurrence settings and change the interval or cancel recurrence without affecting existing instances

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US3] Contract test for recurrence settings modification in tests/contract/test_recurrence_management.py
- [ ] T026 [P] [US3] Integration test for recurrence management in tests/integration/test_recurrence_management.py

### Implementation for User Story 3

- [X] T027 [P] [US3] Add recurrence management methods to RecurringTaskService in src/services/recurring_service.py
- [X] T028 [US3] Create CLI commands for recurrence management in src/cli/cli.py
- [X] T029 [US3] Add recurrence editing functionality to task update in src/services/domain_todo_service.py
- [X] T030 [US3] Implement recurrence cancellation logic in src/services/recurring_service.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Viewing recurring tasks (Priority: P4)

**Goal**: Clearly indicate which tasks are recurring in the task list and provide quick access to recurrence settings

**Independent Test**: User can view their task list and clearly identify which tasks are recurring and their intervals

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US4] Contract test for recurring task display in tests/contract/test_task_display.py
- [ ] T032 [P] [US4] Integration test for recurring task visualization in tests/integration/test_task_display.py

### Implementation for User Story 4

- [X] T033 [P] [US4] Update CLI display functions to show recurrence indicators in src/cli/cli.py
- [X] T034 [US4] Add recurrence information to task listing in src/services/domain_todo_service.py
- [X] T035 [US4] Implement quick access to recurrence settings in CLI in src/cli/cli.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Handle recurrence exceptions (Priority: P5)

**Goal**: Handle edge cases for recurring tasks appropriately (no duplicates, mid-cycle changes, overdue tasks)

**Independent Test**: System handles edge cases gracefully without data corruption

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T036 [P] [US5] Contract test for edge case handling in tests/contract/test_edge_cases.py
- [ ] T037 [P] [US5] Integration test for recurrence exception handling in tests/integration/test_edge_cases.py

### Implementation for User Story 5

- [X] T038 [P] [US5] Implement duplicate prevention logic in src/services/recurring_service.py
- [X] T039 [US5] Add overdue recurring task handling in src/services/recurring_service.py
- [X] T040 [US5] Handle mid-cycle recurrence changes in src/services/recurring_service.py
- [X] T041 [US5] Add data integrity checks in src/services/recurring_service.py

**Checkpoint**: All user stories should now be fully functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T042 [P] Documentation updates in docs/
- [X] T043 Code cleanup and refactoring
- [X] T044 Performance optimization across all stories
- [ ] T045 [P] Additional unit tests (if requested) in tests/unit/
- [X] T046 Security hardening
- [X] T047 Run quickstart.md validation

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (needs recurring tasks to complete)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 (needs recurring tasks to manage)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US1 (needs recurring tasks to display)
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Depends on US1, US2 (needs recurring tasks to test edge cases)

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for recurring task creation endpoint in tests/contract/test_recurring_tasks.py"
Task: "Integration test for creating recurring task in tests/integration/test_recurring_tasks.py"

# Launch all models for User Story 1 together:
Task: "Extend Task model with recurrence properties in src/models/task.py"
Task: "Create RecurringTask model with validation in src/models/recurring_task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2 (depends on US1 completion)
   - Developer C: User Story 3 (depends on US1 completion)
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