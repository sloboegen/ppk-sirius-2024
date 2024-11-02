from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api import find_clothes_router

app = FastAPI()

app.include_router(find_clothes_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def start(request: Request) -> HTMLResponse:
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        request=request,
        name="start.jinja",
    )
