"""В данном файле находятся функции, которые необходимо реализовать в рамках ППК.

Код для запуска моделей взят из их карточек на HuggingFace:
- https://huggingface.co/llava-hf/llava-onevision-qwen2-0.5b-ov-hf#using-pure-transformers
- https://huggingface.co/openai/clip-vit-base-patch32#use-with-transformers

Интерфейсы функций можно менять, если возникает необходимость в этом.
"""

from PIL import Image
import torch
from transformers import AutoProcessor, LlavaOnevisionForConditionalGeneration, CLIPProcessor, CLIPModel

__all__ = ("extract_clothes_images",)


def extract_clothes_images(image: Image.Image) -> list[Image.Image]:
    """Функция возвращает список фотографий предметов одежды, которые находятся на переданной фотографии.

    Это главная функция, которую будет использовать наше приложение.
    Её необходимо написать, используя функции ниже (но не только их).
    Также вам, вероятно, потребуется менять интерфейсы функций ниже: это разрешено делать.
    """

    raise NotImplementedError()


def _get_prompt() -> str:
    """Возвращает промпт, который будет подан VLM-модели."""

    raise NotImplementedError()


def _run_vlm(image: Image.Image) -> str:
    model_id = "llava-hf/llava-onevision-qwen2-0.5b-ov-hf"
    model = LlavaOnevisionForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    ).to(0)

    processor = AutoProcessor.from_pretrained(model_id)
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": _get_prompt()},
                {"type": "image"},
            ],
        },
    ]
    prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(images=image, text=prompt, return_tensors="pt").to(0, torch.float16)

    output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
    return processor.decode(output[0][2:], skip_special_tokens=True)


def _run_clip(image: Image.Image, items: list[str]) -> list[Image.Image]:
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    inputs = processor(text=items, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1).tolist()[0]

    return probs
