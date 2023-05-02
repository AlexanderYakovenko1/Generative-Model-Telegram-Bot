"""Set up handlers."""
from aiogram import Dispatcher

from src.tgbot.handlers.admin import register_admin_handlers
from src.tgbot.handlers.user import register_user_handlers


def register_handlers(dp: Dispatcher):
    """Register handlers with dispatcher."""
    register_admin_handlers(dp)
    register_user_handlers(dp)
