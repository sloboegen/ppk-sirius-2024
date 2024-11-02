"""В данном файле находятся функции, которые необходимо реализовать в рамках ППК.

Код для запуска моделей взят из их карточек на HuggingFace:
- https://huggingface.co/llava-hf/llava-onevision-qwen2-0.5b-ov-hf#using-pure-transformers
- https://huggingface.co/openai/clip-vit-base-patch32#use-with-transformers

Интерфейсы функций можно менять, если возникает необходимость в этом.
"""

from PIL import Image
import torch
from transformers import AutoProcessor, LlavaOnevisionForConditionalGeneration, CLIPProcessor, CLIPModel
from datasets import load_dataset

__all__ = ("extract_clothes_images",)


def extract_clothes_images(image: Image.Image) -> list[Image.Image]:
    """Функция возвращает список фотографий предметов одежды, которые находятся на переданной фотографии.

    Это главная функция, которую будет использовать наше приложение.
    Её необходимо написать, используя функции ниже (но не только их).
    Также вам, вероятно, потребуется менять интерфейсы функций ниже: это разрешено делать.
    """

    # 1. Запускаем VLM для получения описания предметов одежды на картинке.
    description = _run_vlm(image)
    print("Описание", description)

    # 2. Превращаем описание в список названий предметов одежды.
    clothes_list = _process_desc(description)
    print("Список одежды", clothes_list)

    # 3. Загружаем датасет.
    dataset = load_dataset("ghoumrassi/clothes_sample")
    dataset = dataset["train"]  # Все записи в датасете лежат по ключу train.

    # 4. Для каждой вещи будем помнить максимальную вероятность,
    # которую вернул CLIP, и картинку, на которой эта вероятность достигается.
    best_probs = [0 for _ in clothes_list]
    best_images = [None for _ in clothes_list]

    # 5. Инициализируем CLIP, чтобы не делать это на каждой итерации.
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    # 6. Проходимся по всему датасету и ищем картинки, на которых
    # достигается максимальная вероятность.
    for i, row in enumerate(dataset):
        print("CLIP шаг", i)

        image_from_ds = row["image"]
        probs = _run_clip(model, processor, image_from_ds, clothes_list)

        # Обновляем вероятность и картинку.
        # enumerate(['a', 'b', 'c']) --> (0, 'a'), (1, 'b'), (2, 'c')
        for i, prob in enumerate(probs):
            if best_probs[i] < prob:
                best_probs[i] = prob
                best_images[i] = image_from_ds

    print("Вероятности", best_probs)
    return best_images


def _process_desc(desc: str) -> list[str]:
    assistent_idx = desc.find("assistant")
    answer = desc[(assistent_idx + 9) :].strip("\n")

    items = []
    for line in answer.split("\n"):
        _, item = line.split("- ")
        items.append(item.strip("\n").strip("."))

    return items


def _get_prompt() -> str:
    """Возвращает промпт, который будет подан VLM-модели."""

    return "Describe all the clothing items in this image in detail. List each item as a numbered list, specifying the type of clothing (e.g., shirt, pants, shoes, accessories) and any distinguishing features such as color, pattern, material, or unique style. Please include any additional details that help identify the clothing item clearly."


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


def _run_clip(model, processor, image: Image.Image, items: list[str]) -> list[float]:
    inputs = processor(text=items, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1).tolist()[0]

    return probs
