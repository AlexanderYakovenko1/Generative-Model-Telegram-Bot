"""Bot introduction handler."""
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.text_decorations import html_decoration as fmt


async def user_start(m: Message):
    """Handle first interaction with bot."""
    await m.reply(
        f"Приветствую, {fmt.italic(m.from_user.full_name)}. "
        "Этот бот может генерировать изображние по запросу, а так же наброску. "
        "Для генерации по запросу воспользуйся командой /generate [затравка], по наброску /sketch [затравка]"
    )


def register_start(dp: Dispatcher):
    """Register first user interaction."""
    dp.message.register(user_start, CommandStart())
