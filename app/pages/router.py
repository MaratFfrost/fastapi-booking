from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates

from fastapi_cache.decorator import cache
from app.hotels.dao import HotelsDAO




router = APIRouter(
  prefix="",
  tags=["Front-end"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
#@cache(expire=300)
async def get_main_page(request: Request):
    try:
      hotels = await HotelsDAO.find_all_in_limit(limit=6)
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Ошибка при получении отелей, {e}")

    return templates.TemplateResponse("hotels.html", {"request": request, "hotels": hotels})
