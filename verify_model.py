"""Load Stable Diffusion weights before start."""

from src.load_models import load_model
from src.config as load_config

if __name__ == "__main__":
    config = load_config()
    load_model(config.ms.model_path)
