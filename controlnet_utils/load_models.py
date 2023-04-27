import torch
from typing import Tuple, Union
from diffusers import StableDiffusionControlNetPipeline, \
    ControlNetModel, \
    UniPCMultistepScheduler, \
    StableDiffusionPipeline


def speedup_pipeline(pipeline: Union[StableDiffusionPipeline, StableDiffusionControlNetPipeline]) -> None:
    pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
    pipeline.enable_xformers_memory_efficient_attention()
    pipeline.enable_model_cpu_offload()


def load_model(model_dir: str) -> Tuple[StableDiffusionPipeline, StableDiffusionControlNetPipeline]:
    # load control net and stable diffusion v1-5

    torch_dtype = torch.float16

    controlnet = ControlNetModel.from_pretrained(
        pretrained_model_name_or_path="lllyasviel/sd-controlnet-canny",
        torch_dtype=torch_dtype,
        cache_dir=model_dir,
    )

    pipeline_sd = pipeline_sketch = StableDiffusionPipeline.from_pretrained(
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
