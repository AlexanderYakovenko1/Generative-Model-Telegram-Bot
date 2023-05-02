from aiogram import Dispatcher

from .start import register_start
from .generation import register_generate, register_sketch, register_sketch_prompted, \
    register_update_prompt, register_update_sketch


def register_user_handlers(dp: Dispatcher):
    register_start(dp)
    register_generate(dp)
    register_sketch(dp)
    register_sketch_prompted(dp)
    register_update_prompt(dp)
    register_update_sketch(dp)