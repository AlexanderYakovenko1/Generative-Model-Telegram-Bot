from aiogram import Dispatcher

from .bot_state import register_start, register_shutdown


def register_admin_handlers(dp: Dispatcher):
    register_start(dp)
    register_shutdown(dp)
