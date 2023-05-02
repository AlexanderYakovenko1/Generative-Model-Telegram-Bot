"""Bot startup and shutdown helpers."""
from aiogram import Bot, Dispatcher

from src.config import load_config

import os
import gettext

translation = gettext.translation('controlnetbot', os.path.join(os.path.dirname(__file__),
                                                                "..", "..", "..", "..", "locale"), fallback=True)
_ = translation.gettext


async def bot_start(bot: Bot) -> None:
    """Send bot start msg to admins."""
    config = load_config()
    for admin_id in config.tg_bot.admin_ids:
        await bot.send_message(admin_id, _("Бот запущен"))


async def bot_shutdown(bot: Bot) -> None:
    """Send bot shutdown msg to admins."""
    config = load_config()
    for admin_id in config.tg_bot.admin_ids:
        await bot.send_message(admin_id, _("Бот остановлен"))


def register_start(dp: Dispatcher):
    """Register startup msg function."""
    dp.startup.register(bot_start)


def register_shutdown(dp: Dispatcher):
    """Register shutdown msg function."""
    dp.shutdown.register(bot_shutdown)
