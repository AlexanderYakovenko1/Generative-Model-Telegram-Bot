"""Queue querying function."""
from aiogram import Bot
from aiogram.types import FSInputFile
from src.task_queue import TaskQueue
from src.config import load_config


async def send_generated(bot: Bot, task_queue: TaskQueue, tasks: dict):
    """Get generation result from the queue and send to user."""
    config = load_config()
    for task_id, sent_to in tasks.items():
        found, result = task_queue.get_result(task_id)
        if found:
            path = config.ts.assets_path + task_id + '.png'
            result.save(path, format='PNG')
            photo = FSInputFile(path)
            await bot.send_photo(sent_to, photo=photo)
