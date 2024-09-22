from fastapi import APIRouter
from app.hotels.dao import HotelsDAO


router = APIRouter(
  prefix="/hotels",
  tags=["hotels"]
)

@router.get("/all")
async def get_all_hotels():
  return await HotelsDAO.find_all()
