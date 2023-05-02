"""Bot command set up functions."""
import os
import gettext

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from src.config import Settings

translation = gettext.translation('controlnetbot', os.path.join(os.path.dirname(__file__), "..", "..", "..", "locale"), fallback=True)
_ = translation.gettext


async def set_commands(bot: Bot, settings: Settings):
    """Set up main user commands."""
    commands = [
        BotCommand(
            command="start",
            description=_("Начало работы"),
        ),
        BotCommand(
            command="generate",
            description=_("Сгенерировать изображение по текстовому описанию"),
        ),
        BotCommand(
            command="sketch",
            description=_("Сгенерировать изображение по наброску"),
        ),
        BotCommand(
            command="update_prompt",
            description=_("Перерисовать с новой затравкой"),
        ),
        BotCommand(
            command="update_sketch",
            description=_("Перерисовать скетч"),
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

    admin_commands = commands.copy()

    for admin_id in settings.tg_bot.admin_ids:
        await bot.set_my_commands(
            commands=admin_commands,
            scope=BotCommandScopeChat(
                chat_id=admin_id,
            ),
        )