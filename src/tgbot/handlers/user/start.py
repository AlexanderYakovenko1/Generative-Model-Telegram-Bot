"""Bot introduction handler."""
import os
import gettext

from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.text_decorations import html_decoration as fmt

translation = gettext.translation('controlnetbot',
                                  os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "locale"))
_ = translation.gettext


async def user_start(m: Message):
    """Handle first interaction with bot."""
    await m.reply(
        _("Приветствую, {user}. "
          "Этот бот может генерировать изображние по запросу, а так же наброску. "
          "Для генерации по запросу воспользуйся командой /generate [затравка], по наброску /sketch [затравка]"
          ).format(user=fmt.italic(m.from_user.full_name))
    )


def register_start(dp: Dispatcher):
    """Register first user interaction."""
    dp.message.register(user_start, CommandStart())
