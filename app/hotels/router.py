from fastapi import APIRouter
from app.hotels.dao import HotelsDAO
from fastapi_cache.decorator import cache


router = APIRouter(
  prefix="/hotels",
  tags=["hotels"]
)

@router.get("/all")
@cache(expire=60)
async def get_all_hotels():
  return await HotelsDAO.find_all()
