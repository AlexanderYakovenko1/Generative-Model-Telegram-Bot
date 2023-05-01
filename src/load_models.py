"""Stable Diffusion loading."""
import torch
from typing import Tuple, Union
from diffusers import StableDiffusionControlNetPipeline, \
    ControlNetModel, \
    UniPCMultistepScheduler, \
    StableDiffusionPipeline


def speedup_pipeline(pipeline: Union[StableDiffusionPipeline, StableDiffusionControlNetPipeline]) -> None:
    """
    Speed up pipeline setting up scheduler, xformers, cpu_offload.

    :param pipeline: StableDiffusionPipeline with modifications
    :return: None
    """
    pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
    pipeline.enable_xformers_memory_efficient_attention()
    pipeline.enable_model_cpu_offload()


def load_model(model_dir: str) -> Tuple[StableDiffusionPipeline, StableDiffusionControlNetPipeline]:
    """Load Pipelines.

    Load two pipelines for text to image generation (stable diffusion)
    and text to image with additional image condition (stable diffusion with controlnet).

    :param model_dir: path to directory with model weights
    :return: pipeline SD, pipeline SD with ControlNet
    """
    # load control net and stable diffusion v1-5
    torch_dtype = torch.float16

    controlnet = ControlNetModel.from_pretrained(
        pretrained_model_name_or_path="lllyasviel/sd-controlnet-canny",
        torch_dtype=torch_dtype,
        cache_dir=model_dir,
    )

    pipeline_sd = StableDiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5",
        torch_dtype=torch_dtype,
        cache_dir=model_dir,
    )
    pipeline_sketch = StableDiffusionControlNetPipeline.from_pretrained(
        pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5",
        controlnet=controlnet,
        torch_dtype=torch_dtype,
        cache_dir=model_dir,
    )

    # speed up diffusion process with faster scheduler and memory optimization
    speedup_pipeline(pipeline_sd)
    speedup_pipeline(pipeline_sketch)

    return pipeline_sd, pipeline_sketch
