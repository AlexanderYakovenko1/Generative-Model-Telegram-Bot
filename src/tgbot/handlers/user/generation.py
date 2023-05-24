"""Prompted image generation functions."""
import os
from typing import Dict, Any
from uuid import uuid4
import gettext

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from PIL import Image, ImageOps
from googletrans import Translator

from src.task_queue import TaskQueue
from src.tgbot.states.sketch_states import SketchStates
from src.config import load_config

translator = Translator()

translation = gettext.translation('controlnetbot', os.path.join(os.path.dirname(__file__),
                                                                "..", "..", "..", "..", "locale"))
_ = translation.gettext


def generate_image(controlnet, prompt, control_image=None):
    """Worker function for generating image."""
    if control_image is not None:
        control_image = ImageOps.invert(control_image)
    image = controlnet.generate_image(prompt, control_image)
    return image


async def generate(m: Message, task_queue: TaskQueue, tasks: Dict[str, Any]):
    """Handle /generate call."""
    global translator
    try:
        raw_prompt = m.text.split(' ', 1)[1]
        for i in range(5): # retry
            try:
                prompt = translator.translate(raw_prompt, dest="en").text
                break
            except TypeError:
                pass
        else:
            await m.reply(_("Внутренняя ошибка Google Translate"))
            return

        task_id = str(uuid4())

        if task_queue.put_task(task_id, generate_image, prompt):
            tasks[task_id] = m.chat.id
            await m.reply(
                _("Ваш запрос на генерацию по затравке {raw_prompt} поставлен в очередь").format(raw_prompt=raw_prompt))
        else:
            await m.reply(_("Попробуйте позже, очередь переполнена"))

    except IndexError:
        await m.reply(_("Неверный формат ввода затраки. Попробуйте ещё раз /generate [затравка]"))


def register_generate(dp: Dispatcher):
    """Register /generate bot call."""
    dp.message.register(generate, Command(commands=["generate"]))


async def sketch(m: Message, state: FSMContext):
    """Handle /sketch call."""
    global translator
    await state.clear()

    try:
        raw_prompt = m.text.split(' ', 1)[1]
        
        for i in range(5): # retry
            try:
                prompt = translator.translate(raw_prompt, dest="en").text
                break
            except TypeError:
                pass
        else:
            await m.reply(_("Внутренняя ошибка Google Translate"))
            return

        task_id = str(uuid4())
        config = load_config()

        await m.reply(
            _("Для генерации будет использована затравка: {raw_prompt}. "
              "Ниже вам предложен холст для рисования. "
              "Следущим сообщением отправьте ваш набросок.").format(raw_prompt=raw_prompt)
        )
        await m.reply_photo(photo=config.ms.bg_file_id)
        await state.update_data(prompt=prompt)
        await state.update_data(task_id=task_id)
        await state.set_state(SketchStates.sketch)

    except IndexError:
        await m.reply(_("Неверный формат ввода затраки. Попробуйте ещё раз /sketch [затравка]"))


def register_sketch(dp: Dispatcher):
    """Register /sketch bot call."""
    dp.message.register(sketch, Command(commands=["sketch"]))


async def sketch_prompted(m: Message, bot: Bot, state: FSMContext, task_queue: TaskQueue, tasks: Dict[str, Any]):
    """Handle /sketch call."""
    config = load_config()

    data = await state.get_data()
    task_id = data["task_id"]
    prompt = data["prompt"]

    path_to_sketch = os.path.join(config.ts.assets_path, f"{task_id}-sketch.png")

    file_id = m.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, path_to_sketch)
    sketch = Image.open(path_to_sketch)

    if task_queue.put_task(task_id, generate_image, prompt, sketch):
        tasks[task_id] = m.chat.id
        await m.reply(_("Ваш запрос на генерацию по наброску поставлен в очередь"))
    else:
        await m.reply(_("Попробуйте позже, очередь переполнена"))


def register_sketch_prompted(dp: Dispatcher):
    """Register /sketch bot call."""
    dp.message.register(sketch_prompted, SketchStates.sketch)


async def update_prompt(m: Message):
    """Handle /update_prompt call."""
    await m.reply("Not Implemented Yet")


def register_update_prompt(dp: Dispatcher):
    """Register /update_prompt bot call."""
    dp.message.register(update_prompt, Command(commands=["update_prompt"]))


async def update_sketch(m: Message):
    """Handle /update_sketch call."""
    await m.reply("Not Implemented Yet")


def register_update_sketch(dp: Dispatcher):
    """Register /update_sketch bot call."""
    dp.message.register(update_sketch, Command(commands=["update_sketch"]))
