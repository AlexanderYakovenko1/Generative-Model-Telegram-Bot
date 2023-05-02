"""Bot command set up functions."""
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    """Set up main user commands."""
    commands = [
        BotCommand(
            command="start",
            description="Начало работы",
        ),
        BotCommand(
            command="generate",
            description="Сгенерировать изображение по текстовому описанию",
        ),
        BotCommand(
            command="sketch",
            description="Сгенерировать изображение по наброску",
        ),
        BotCommand(
            command="update_prompt",
            description="Перерисовать с новой затравкой",
        ),
        BotCommand(
            command="update_sketch",
            description="Перерисовать скетч",
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
