"""Controlnet implementation."""
import PIL
import torch
import random
import numpy as np
from typing import Union, List

from src.load_models import load_model
from src.config import load_config


class Controlnet:
    """The network for text to image generation."""

    def __init__(self, config=load_config()):
        """
        Create Stable Diffusion and load weights.

        :param config: configuration for Stable Diffusion
        """
        self.model_dir = config.ms.model_path
        self.num_inference_steps = config.ms.num_inference_steps
        self.pipeline_sd, self.pipeline_sketch = load_model(self.model_dir)

    def generate_image(
            self,
            prompt: Union[str, List[str]] = None,
            control_image: Union[
                torch.FloatTensor, PIL.Image.Image, List[torch.FloatTensor], List[PIL.Image.Image]] = None,
            seed: int = None,
    ) -> PIL.Image.Image:
        """
        Text to image generation.

        :param prompt: text for conditional image generation
        :param control_image: sketch for image restoration,
                if control_image is None then plain text to image generation works
        :param seed: if seed is None, then seed isn't setting up
        """
        if seed is not None:
            set_seed(seed)
        if control_image is None:
            image = self.pipeline_sd(
                prompt,
                num_inference_steps=self.num_inference_steps,
            ).images[0]
        else:
            image = self.pipeline_sketch(
                prompt,
                num_inference_steps=20,
                image=control_image
            ).images[0]
        return image


def set_seed(seed: int = 0) -> None:
    """Set up seed."""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
