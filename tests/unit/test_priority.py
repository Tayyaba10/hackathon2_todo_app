import pytest
from src.models.priority import Priority


class TestPriority:
    """Unit tests for the Priority enum."""

    def test_priority_enum_values(self):
        """Test that Priority enum has the correct values."""
        assert Priority.HIGH.value == "high"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.LOW.value == "low"

    def test_priority_enum_str_representation(self):
        """Test string representation of Priority enum."""
        assert str(Priority.HIGH) == "high"
        assert str(Priority.MEDIUM) == "medium"
        assert str(Priority.LOW) == "low"

    def test_priority_from_string_valid(self):
        """Test creating Priority from valid string values."""
        assert Priority.from_string("high") == Priority.HIGH
        assert Priority.from_string("HIGH") == Priority.HIGH  # Case insensitive
        assert Priority.from_string("High") == Priority.HIGH  # Case insensitive
        assert Priority.from_string("medium") == Priority.MEDIUM
        assert Priority.from_string("low") == Priority.LOW

    def test_priority_from_string_invalid(self):
        """Test creating Priority from invalid string values raises ValueError."""
        with pytest.raises(ValueError):
            Priority.from_string("invalid")

        with pytest.raises(ValueError):
            Priority.from_string("HIGH_PRIORITY")

        with pytest.raises(ValueError):
            Priority.from_string("")

    def test_priority_equality(self):
        """Test Priority enum equality."""
        assert Priority.HIGH == Priority.HIGH
        assert Priority.MEDIUM == Priority.MEDIUM
        assert Priority.LOW == Priority.LOW
        assert Priority.HIGH != Priority.MEDIUM
        assert Priority.MEDIUM != Priority.LOW
        assert Priority.LOW != Priority.HIGH

    def test_priority_membership(self):
        """Test that all expected priority values are in the enum."""
        expected_values = {"high", "medium", "low"}
        actual_values = {p.value for p in Priority}
        assert actual_values == expected_values