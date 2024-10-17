from fastapi import APIRouter
from app.hotels.dao import HotelsDAO
from fastapi_cache.decorator import cache


router = APIRouter(
  prefix="/hotels",
  tags=["hotels"]
)

@router.get("/all")
@cache(expire=600)
async def get_all_hotels():
  return await HotelsDAO.find_all()


@router.get("/{id}")
@cache(expire=50)
async def get_info_by_id(id: int):
  return await HotelsDAO.find_by_id(model_id=id)
