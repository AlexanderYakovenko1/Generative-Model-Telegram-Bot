import cv2
import sys
import numpy as np
from PIL import Image

sys.path.append("/home/vmeshchaninov/Education/Generative-Model-Telegram-Bot")

from controlnet import Controlnet


def create_edges() -> None:
    image = Image.open("bird.png")
    image = np.asarray(image)

    low_threshold = 200
    high_threshold = 220

    edges = cv2.Canny(image, low_threshold, high_threshold)
    edges = edges[:, :, None]
    edges = np.concatenate([edges, edges, edges], axis=2)
    control_image = Image.fromarray(edges)

    control_image.save("./bird_edges.png")


def test_prompt_sketch() -> None:
    prompt = "a blue paradise bird in the jungle"

    control_image = Image.open("controlnet_utils/bird_edges.png")

    controlnet = Controlnet()

    image = controlnet.generate_image(prompt=prompt, control_image=control_image)
    image.save('controlnet_utils/image_test_prompt_scetch.png')


def test_prompt() -> None:
    prompt = "a blue paradise bird in the jungle"
    controlnet = Controlnet()

    image = controlnet.generate_image(prompt=prompt)
    image.save('controlnet_utils/image_test_prompt.png')


if __name__ == "__main__":
    test_prompt_sketch()
