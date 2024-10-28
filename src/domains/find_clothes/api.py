import typing as tp

from fastapi import APIRouter, File

find_clothes_router = APIRouter()


@find_clothes_router.post("/findClothes")
def find_clothes_file_handler(input_file: tp.Annotated[bytes, File()]):  # type: ignore[no-untyped-def]
    return {"file_size": len(input_file)}
