"""Image generation middleware."""
from typing import Callable
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Awaitable, Dict
from src.task_queue import TaskQueue


class GenerateMiddleware(BaseMiddleware):
    """/generate command middleware."""

    def __init__(self, task_queue: TaskQueue, tasks: Dict[str, Any]) -> None:
        """Initialize GenerateMiddleware.

        :param task_queue: task queue to put requests into
        :param tasks: pending tasks
        """
        self.task_queue = task_queue
        self.tasks = tasks

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        """Fill data and pass to handler."""
        data['task_queue'] = self.task_queue
        data['tasks'] = self.tasks

        return await handler(event, data)
