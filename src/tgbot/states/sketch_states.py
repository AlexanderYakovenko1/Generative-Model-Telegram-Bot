from aiogram.fsm.state import State, StatesGroup


class SketchStates(StatesGroup):
    prompt = State()
    task_id = State()
    sketch = State()
