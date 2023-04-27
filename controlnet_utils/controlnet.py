import torch
from typing import Union, List
import PIL

from controlnet_utils.load_models import load_model


class Controlnet:
    def __init__(self):
        self.model_dir = "/home/vmeshchaninov/Education/Generative-Model-Telegram-Bot/models"
        self.pipeline = load_model(self.model_dir)

    def generate_image(
            self,
            prompt: Union[str, List[str]] = None,
            control_image: Union[
                torch.FloatTensor, PIL.Image.Image, List[torch.FloatTensor], List[PIL.Image.Image]] = None,
    ):
        generator = torch.manual_seed(0)
        image = self.pipeline(prompt, num_inference_steps=20, generator=generator, image=control_image).images[0]
        return image
