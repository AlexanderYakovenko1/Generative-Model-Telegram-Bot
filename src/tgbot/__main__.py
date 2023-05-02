import argparse
import asyncio
import logging
import sys
import os


from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation

from apscheduler.schedulers.asyncio import AsyncIOScheduler


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.tgbot.handlers import register_handlers
from src.tgbot.services import set_commands
from src.tgbot.jobs.generate_queue import send_generated
from src.tgbot.middlewares.generate import GenerateMiddleware
from src.controlnet import Controlnet
from src.task_queue import TaskQueue
from src.config import load_config


logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_workers', type=int, default=1, 
        help="Количество воркеров для обработки запросов на генерацию")

    return parser.parse_args()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config()

    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())

    global task_queue
    global tasks

    dp.message.middleware.register(GenerateMiddleware(task_queue, tasks))

    scheduler = AsyncIOScheduler({"apscheduler.timezone": "Europe/Moscow"})
    
    
    scheduler.add_job(send_generated, trigger="interval", seconds=5, kwargs={"bot": bot, "task_queue": task_queue, "tasks": tasks})
    scheduler.start()

    register_handlers(dp=dp)

    try:
        await set_commands(bot)
        await dp.start_polling(bot, config=config)
    finally:
        await dp.fsm.storage.close()
        await bot.session.close()

    scheduler.shutdown()
    task_queue.close()


if __name__ == "__main__":
    args = parse_args()
    try:
        tasks = dict()
        task_queue = TaskQueue(num_workers=args.num_workers, create_state=Controlnet, context='spawn')
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot has killed!")
