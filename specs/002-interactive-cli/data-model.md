# Data Model: Interactive CLI for Todo Application

## Entity: InteractiveMenu

**Description**: Represents the menu system that guides users through operations with numbered options and emojis

**Fields**:
- `options` (dict): Dictionary mapping menu numbers to operation descriptions
- `display_text` (str): Formatted text for menu display with emojis
- `valid_choices` (list): List of valid numeric choices for menu selection

**Validation Rules**:
- All menu options must have corresponding emoji indicators
- All numeric choices must map to valid operations
- Menu must include exit option (0)

## Entity: GuidedOperation

**Description**: Represents the step-by-step prompting system for each task operation

**Fields**:
- `operation_type` (str): Type of operation (add, update, delete, complete, incomplete)
- `prompts` (list): List of prompts to guide user through operation
- `validation_rules` (dict): Rules for validating user input during operation
- `success_message` (str): Message to display upon successful operation
- `error_message` (str): Message to display upon operation failure

**Validation Rules**:
- All operations must return to main menu after completion
- All operations must validate user input before executing
- Error messages must be user-friendly and non-technical

## Relationships
- InteractiveMenu contains multiple GuidedOperation entities
- Each GuidedOperation corresponds to a specific menu option
- Both entities interact with the existing TodoService layer