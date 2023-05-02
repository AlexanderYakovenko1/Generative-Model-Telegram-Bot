"""Load Stable Diffusion weights before start."""

from src.load_models import load_model
from src.config import load_config


def verify():
    """Verifies that model can be loaded, download weights if not."""
    config = load_config()
    load_model(config.ms.model_path)


if __name__ == "__main__":
    verify()
