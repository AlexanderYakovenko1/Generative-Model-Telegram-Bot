"""Test for queue module."""

from src.task_queue import nothing


class TestQueue:
    """A suite of tests for Queue class."""

    def test_nothing(self):
        """Test sample function."""
        assert nothing() == "I do nothing"
