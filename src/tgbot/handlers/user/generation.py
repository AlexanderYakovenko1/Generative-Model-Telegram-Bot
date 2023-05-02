import os
from typing import Dict, Any
from uuid import uuid4

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from PIL import Image
from googletrans import Translator

from src.task_queue import TaskQueue
from src.tgbot.states.sketch_states import SketchStates
from src.config import load_config


translator = Translator()


def generate_image(controlnet, prompt, control_image=None):
    image = controlnet.generate_image(prompt, control_image)
    return image


async def generate(m: Message, task_queue: TaskQueue, tasks: Dict[str, Any]):
    global translator
    try:
        raw_prompt = m.text.split(' ', 1)[1]
        prompt = translator.translate(raw_prompt, dest="en").text
        
        task_id = str(uuid4())
        
        if task_queue.put_task(task_id, generate_image, prompt):
            tasks[task_id] = m.chat.id
            await m.reply(f"Ваш запрос на генерацию по затравке {raw_prompt} поставлен в очередь")
        else:
            await m.reply("Попробуйте позже, очередь переполнена")

    except IndexError:
        await m.reply("Неверный формат ввода затраки. Попробуйте ещё раз /generate [затравка]")


def register_generate(dp: Dispatcher):
    dp.message.register(generate, Command(commands=["generate"]))


async def sketch(m: Message, state: FSMContext):
    global translator
    await state.clear()

    try:
        raw_prompt = m.text.split(' ', 1)[1]
        prompt = translator.translate(raw_prompt, dest="en").text
        task_id = str(uuid4())
        config = load_config()

        await m.reply(
            f"Для генерации будет использована затравка: {raw_prompt}. "
            "Ниже вам предложен холст для рисования. "
            "Следущим сообщением отправьте ваш набросок."
        )
        await m.reply_photo(photo=config.ms.white_file_id)
        await state.update_data(prompt=prompt)
        await state.update_data(task_id=task_id)
        await state.set_state(SketchStates.sketch)
    
    except IndexError:
        await m.reply("Неверный формат ввода затраки. Попробуйте ещё раз /sketch [затравка]")


def register_sketch(dp: Dispatcher):
    dp.message.register(sketch, Command(commands=["sketch"]))


async def sketch_prompted(m: Message, bot: Bot, state: FSMContext, task_queue: TaskQueue, tasks: Dict[str, Any]):
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
        await m.reply(f"Ваш запрос на генерацию по наброску поставлен в очередь")
    else:
        await m.reply("Попробуйте позже, очередь переполнена")


def register_sketch_prompted(dp: Dispatcher):
    dp.message.register(sketch_prompted, SketchStates.sketch)

async def update_prompt(m: Message):
    await m.reply("Not Implemented Yet")

def register_update_prompt(dp: Dispatcher):
    dp.message.register(update_prompt, Command(commands=["update_prompt"]))

async def update_sketch(m: Message):
    await m.reply("Not Implemented Yet")

def register_update_sketch(dp: Dispatcher):
    dp.message.register(update_sketch, Command(commands=["update_sketch"]))
