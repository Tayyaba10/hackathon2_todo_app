---
id: 001
title: Update Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user:
command: sp.constitution
labels: [constitution, todo-app, spec-driven-development]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

# Evolution of Todo (Phase I)

## Role & Authority
You are an expert Product Engineer and Python Architect operating under a spec-driven development workflow.
You must strictly follow specifications written using Spec-Kit Plus.
You are not allowed to make assumptions beyond what is explicitly defined in the spec.

## Development Philosophy
- No manual coding by the user
- All implementation must originate from approved specifications
- Clean architecture is mandatory, even for small CLI systems
- The system must be designed to evolve into cloud-native and distributed architectures in later phases

## Scope — Phase I Only
You are currently implementing **Phase I: In-Memory Python Console Todo Application**.
You must not introduce features from later phases unless explicitly specified.

## Functional Requirements (Mandatory)
Implement exactly the following core features:
1. Add a task (title + description)
2. Update a task
3. Delete a task by ID
4. View all tasks with completion status
5. Mark tasks as complete or incomplete

## Technical Constraints
- Language: Python 3.13+
- Storage: In-memory only (no files, no databases)
- Interface: Console / CLI
- Project structure must follow clean separation of concerns
- Code must be readable, testable, and modular

## Architectural Rules
- Business logic must not live in the CLI layer
- Data storage must be abstracted, even if in-memory
- Each responsibility should have a single, clear owner
- IDs must be deterministic and managed centrally

## Tooling & Workflow
- Use Spec-Kit Plus for all specs and planning
- Use Qwen / Claude Code only after specs are finalized
- Follow the sequence:
  Spec → Plan → Tasks → Implementation
- Do not skip or merge steps

## Code Quality Rules

## Response snapshot

# Todo Application Constitution

## Core Principles

### I. Spec-Driven Development
All implementation must originate from approved specifications written using Spec-Kit Plus; No manual coding without prior specification; Strict adherence to specifications without assumptions beyond what is explicitly defined.

### II. Clean Architecture
Business logic must not live in the CLI layer; Data storage must be abstracted, even if in-memory; Each responsibility should have a single, clear owner; Follow separation of concerns with clear boundaries between layers.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced; All features must have corresponding tests before implementation.

### IV. In-Memory Storage Abstraction
Storage must be abstracted and managed centrally; Even in-memory storage requires proper abstraction layer; IDs must be deterministic and managed centrally; Prepare for future persistence implementations.

### V. Console Interface Design
CLI interface must be intuitive and user-friendly; Follow standard CLI patterns and conventions; Support both human-readable and structured output formats; Clear error messaging and help documentation.

### VI. Python 3.13+ Standards
Use modern Python 3.13+ features and syntax; Follow PEP 8 style guidelines; Type hints mandatory for all public interfaces; Maintain compatibility with specified Python version.

## Technical Constraints
- Language: Python 3.13+
- Storage: In-memory only (no files, no databases for Phase I)
- Interface: Console / CLI
- Project structure must follow clean separation of concerns
- Code must be readable, testable, and modular
- No external dependencies beyond standard library for core functionality

## Architectural Rules
- Business logic must not live in the CLI layer
- Data storage must be abstracted, even if in-memory
- Each responsibility should have a single, clear owner
- IDs must be deterministic and managed centrally
- Follow clean architecture principles with clear separation between entities, use cases, interface adapters, and frameworks

## Development Workflow
- Use Spec-Kit Plus for all specs and planning
- Follow the sequence: Spec → Plan → Tasks → Implementation
- Do not skip or merge steps
- All implementation must be traceable to approved specifications
- Code reviews must verify compliance with architectural principles

## Governance
This constitution supersedes all other practices; Amendments require documentation, approval, and migration plan; All PRs/reviews must verify compliance; Complexity must be justified; Use specification documents for development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30

## Outcome

- ✅ Impact: Updated project constitution with specific principles for todo application development
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Implementation can now proceed according to spec-driven workflow
- 🧠 Reflection: Constitution now properly reflects the requirements for the todo application project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable):
- Next experiment (smallest change to try): Begin spec creation for the todo application