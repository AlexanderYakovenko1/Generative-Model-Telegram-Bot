"""SketchState class."""
from aiogram.fsm.state import State, StatesGroup


class SketchStates(StatesGroup):
    """Stores image and text prompts along with queue task id for retrieval."""

    prompt = State()
    task_id = State()
    sketch = State()
