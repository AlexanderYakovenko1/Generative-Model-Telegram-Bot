"""Bot configuration file."""

from pydantic import BaseSettings


class TgBot(BaseSettings):
    """Telegram API settings."""

    token: str
    admin_ids: list[int]
    chief_id: int


class ModelServing(BaseSettings):
    """Model inference settings."""

    model_path: str
    bg_file_id: str
    num_inference_steps: int


class TaskStorage(BaseSettings):
    """Result storing settings."""

    assets_path: str


class SettingExtractor(BaseSettings):
    """Default settings structure."""

    TG_BOT__TOKEN: str = "6064193934:AAGh7DXzdMq1f8HLakE39C3BNWa--G3XmdU"
    TG_BOT__ADMIN_IDS: list[int] = [254582124, 135116752]  # @Shvet5
    TG_BOT__CHIEF_ID: int = 254582124  # @Shvet5

    MS__MODEL_PATH: str = "./assets/"
    MS__BG_FILE_ID: str = "AgACAgIAAxkBAAIBDmRQaD7y8uejBFHGWm1OYXXOYj-jAAI7zDEbWpqBSjr92JS1EVa3AQADAgADeAADLwQ"
    MS__NUM_INFERENCE_STEPS: int = 20

    TS__ASSETS_PATH: str = "./assets/"


class Settings(BaseSettings):
    """App settings."""

    tg_bot: TgBot
    ms: ModelServing
    ts: TaskStorage


def load_config() -> Settings:
    """Create Settings instance with default parameters."""
    settings = SettingExtractor()

    return Settings(
        tg_bot=TgBot(
            token=settings.TG_BOT__TOKEN,
            admin_ids=settings.TG_BOT__ADMIN_IDS,
            chief_id=settings.TG_BOT__CHIEF_ID,
        ),
        ms=ModelServing(
            model_path=settings.MS__MODEL_PATH,
            bg_file_id=settings.MS__BG_FILE_ID,
            num_inference_steps=settings.MS__NUM_INFERENCE_STEPS,
        ),
        ts=TaskStorage(
            assets_path=settings.TS__ASSETS_PATH,
        )
    )
