import torch
from typing import Union, List
import PIL

from controlnet_utils.load_models import load_model


class Controlnet:
    def __init__(self):
        self.model_dir = "/home/vmeshchaninov/Education/Generative-Model-Telegram-Bot/models"
        self.pipeline_sd, self.pipeline_sketch = load_model(self.model_dir)
        self.num_inference_steps = 20

    def generate_image(
            self,
            prompt: Union[str, List[str]] = None,
            control_image: Union[
                torch.FloatTensor, PIL.Image.Image, List[torch.FloatTensor], List[PIL.Image.Image]] = None,
    ) -> PIL.Image.Image:
        generator = torch.manual_seed(0)
        if control_image is None:
            image = self.pipeline_sd(
                prompt,
                num_inference_steps=self.num_inference_steps,
                generator=generator
            ).images[0]
        else:
            image = self.pipeline_sketch(
                prompt,
                num_inference_steps=20,
                generator=generator,
                image=control_image
            ).images[0]
        return image
