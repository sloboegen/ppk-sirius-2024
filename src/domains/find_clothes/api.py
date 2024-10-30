import base64
import io
import logging
import typing as tp
import uuid

import requests
from PIL import Image
from src.domains.find_clothes.core import extract_clothes_images
from fastapi import APIRouter, BackgroundTasks, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates


logger = logging.getLogger(__name__)


find_clothes_router = APIRouter()
_RESULTS: dict[uuid.UUID, list[Image.Image]] = {}


def _run_extracting(request_id: uuid.UUID, image_file: bytes) -> None:
    logger.debug("Processing request with ID=%s", request_id)

    image = Image.open(io.BytesIO(image_file))
    clothes_images = extract_clothes_images(image)
    _RESULTS[request_id] = clothes_images


def _mock_run_extracting(request_id: uuid.UUID, image_file: bytes) -> None:
    logger.debug("Processing request with ID=%s", request_id)

    image_url = "https://www.cbbiomass.com/wp-content/uploads/2017/04/Square-500x500-red.png"
    image = Image.open(requests.get(image_url, stream=True, timeout=20).raw)
    _RESULTS[request_id] = [image]


@find_clothes_router.post("/findClothes")
def find_clothes_file_handler(
    input_file: tp.Annotated[bytes, File()],
    background_tasks: BackgroundTasks,
) -> RedirectResponse:
    request_id = uuid.uuid4()
    # TODO: как будет готова функция по получению настоящих картинок,
    # то тут необходимо поменять `_mock_run_extracting` на `_run_extracting`.

    background_tasks.add_task(_mock_run_extracting, request_id=request_id, image_file=input_file)

    return RedirectResponse(f"/findClothes/{request_id}", status_code=302)


@find_clothes_router.get("/findClothes/{request_id}")
def get_find_clothes_result(request: Request, request_id: uuid.UUID) -> HTMLResponse:
    templates = Jinja2Templates(directory="templates")

    images = _RESULTS.get(request_id)
    if images is None:
        return templates.TemplateResponse(request, "result_not_ready.jinja")

    images64 = []
    for image in images:
        buffer = io.BytesIO()
        image.save(buffer, "PNG")

        image64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        images64.append(image64)

    return templates.TemplateResponse(
        request,
        "result_ok.jinja",
        context={"images": images64},
    )
