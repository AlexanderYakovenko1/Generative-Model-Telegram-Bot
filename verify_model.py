"""Load Stable Diffusion weights before start."""

from src.load_models import load_model
import src.config as config

if __name__ == "__main__":
    load_model(config.MODEL_PATH)
