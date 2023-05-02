from typing import Callable
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Awaitable, Dict
from src.task_queue import TaskQueue


class GenerateMiddleware(BaseMiddleware):
    def __init__(self, task_queue: TaskQueue, tasks: Dict[str, Any]) -> None:
        self.task_queue = task_queue
        self.tasks = tasks

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data['task_queue'] = self.task_queue
        data['tasks'] = self.tasks

        return await handler(event, data)
