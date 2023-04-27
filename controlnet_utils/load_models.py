import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler


def load_model(model_dir: str) -> StableDiffusionControlNetPipeline:
    # load control net and stable diffusion v1-5

    torch_dtype = torch.float16

    controlnet = ControlNetModel.from_pretrained(
        pretrained_model_name_or_path="lllyasviel/sd-controlnet-canny",
        torch_dtype=torch_dtype,
        cache_dir=model_dir,
    )

    pipeline = StableDiffusionControlNetPipeline.from_pretrained(
        pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5",
        controlnet=controlnet,
        torch_dtype=torch_dtype,
        cache_dir=model_dir,
    )

    # speed up diffusion process with faster scheduler and memory optimization
    pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
    pipeline.enable_xformers_memory_efficient_attention()
    pipeline.enable_model_cpu_offload()

    return pipeline
