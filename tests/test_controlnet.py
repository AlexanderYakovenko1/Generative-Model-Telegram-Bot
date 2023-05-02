"""Tests for controlnet conditional generation."""
import numpy as np
from PIL import Image

from src.config import load_config
from src.controlnet import Controlnet


def cosine_distance(a, b):
    """Compute cosine distance of two vectors."""
    a = a.reshape(-1)
    b = b.reshape(-1)
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return 1 - cos_sim


def test_prompt_sketch() -> None:
    """Test controlnet generation conditioned on prompt and sketch."""
    prompt = "a blue paradise bird in the jungle"
    control_image = Image.open("assets/bird_edges.png")
    eps = 3e-1

    controlnet = Controlnet(load_config())

    image_pred = controlnet.generate_image(prompt=prompt, control_image=control_image)
    image_real = Image.open('assets/image_test_prompt_scetch.png')

    assert cosine_distance(np.asarray(image_pred, dtype=float), np.asarray(image_real, dtype=float)) < eps


def test_prompt() -> None:
    """Test controlnet generation conditioned on prompt only."""
    prompt = "a blue paradise bird in the jungle"
    eps = 3e-1

    controlnet = Controlnet(load_config())

    image_pred = controlnet.generate_image(prompt=prompt, seed=42)
    image_real = Image.open('assets/image_test_prompt.png')
    assert cosine_distance(np.asarray(image_pred, dtype=float), np.asarray(image_real, dtype=float)) < eps
