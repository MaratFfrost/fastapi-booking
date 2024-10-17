from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates

from fastapi_cache.decorator import cache
from app.hotels.dao import HotelsDAO
from app.hotels.router import get_all_hotels, get_info_by_id




router = APIRouter(
  prefix="",
  tags=["Front-end"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_main_page(request: Request):
    try:
      some_hotels = await HotelsDAO.find_all_in_limit(limit=6)
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Ошибка при получении отелей, {e}")

    return templates.TemplateResponse("index.html", {"request": request, "hotels": some_hotels})


@router.get("/hotels")
async def get_all_hotels(request: Request,
  hotels = Depends(get_all_hotels)):

  return templates.TemplateResponse("hotels.html", {"request": request, "hotels": hotels, })

@router.get("/hotels/{id}")
async def get_current_hotel(
    request: Request,
    info = Depends(get_info_by_id)
):
    return templates.TemplateResponse("hotel.html", {"request": request, "info": info})


