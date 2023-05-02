from aiogram import Bot, Dispatcher

from src.config import load_config


async def bot_start(bot: Bot) -> None:
    config = load_config()
    for admin_id in config.tg_bot.admin_ids:
        await bot.send_message(admin_id, "Bot started")


async def bot_shutdown(bot: Bot) -> None:
    config = load_config()
    for admin_id in config.tg_bot.admin_ids:
        await bot.send_message(admin_id, "Bot stoped")


def register_start(dp: Dispatcher):
    dp.startup.register(bot_start)


def register_shutdown(dp: Dispatcher):
    dp.shutdown.register(bot_shutdown)
