from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_all_hotels



router = APIRouter(
  prefix="",
  tags=["Front-end"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_hotels_page(
  request: Request,
  hotels=Depends(get_all_hotels)
):
  return templates.TemplateResponse(name="hotels.html", context={ "request": request})
