"""Test for queue module."""
import random
from time import sleep

from src.task_queue import TaskQueue


def slow_func(inp):
    """Sample function that takes a while to finish."""
    sleep(2)
    return inp


def fast_func(inp):
    """Sample function that finishes *almost* instantly."""
    return inp


class TestQueue:
    """A suite of tests for Queue class."""

    def test_one_task_at_a_time(self):
        """Test that tasks complete and return the expected results."""
        tq = TaskQueue(num_workers=1)

        random.seed(1337)
        for i in range(100):
            arg = random.randint(1, 622)

            tq.put_task(f"{i}", fast_func, arg)
            sleep(0.01)
            available, result = tq.get_result(f"{i}")
            assert available is True and result == fast_func(arg)

    def test_one_long_task_many_fast(self):
        """Test running one slow task alongside many fast ones."""
        tq = TaskQueue(num_workers=2, queue_size=100)

        tq.put_task("slow", slow_func, "SLOW RESULT")
        put_results = []
        for i in range(100):
            put_results.append(tq.put_task(f"{i}", fast_func, f"FAST RESULT {i}"))

        assert all(put_results) is True

        sleep(0.01)
        available, result = tq.get_result("slow")

        assert available is False and result is None

        get_results = []
        for i in range(100):
            get_results.append(tq.get_result(f"{i}")[0])

        assert all(get_results) is True

        sleep(3)
        tq.close()
        assert tq.get_result("slow")[0] is True

    def test_many_tasks_few_executors(self):
        """Test small worker pool and spam it with many tasks."""
        tq = TaskQueue(queue_size=4)

        put_results = []
        for i in range(10):
            put_results.append(tq.put_task(f"{i}", slow_func, i ** 3))

        assert all(put_results) is False and any(put_results) is True

        initial_get_results = []
        for i in range(10):
            initial_get_results.append(tq.get_result(f"{i}")[0])

        assert any(initial_get_results) is False

        sleep(3)
        tq.close()

        final_get_results = []
        for i in range(10):
            final_get_results.append(tq.get_result(f"{i}"))

        assert any(final_get_results) is True
