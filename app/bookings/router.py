from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status

from app.bookings.dao import BookingDao
from app.bookings.schemas import DeleteBookingRequest, SBookingDel
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
  tags=["Booking"],
  prefix="/bookings"
)

@router.get("/my_bokings")
async def get_booking(user: Users = Depends(get_current_user)):
  return await BookingDao.find_user_bookings(user.id)

@router.post("/book_a_room")
async def add_booking(
  room_id:int, date_from: date, date_to: date,
  user: Users = Depends(get_current_user)
 ):
  booking = await BookingDao.add(user.id, room_id, date_from, date_to)
  if not booking:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete("/del_booking")
async def del_booking(book_id: int, user: Users = Depends(get_current_user)):
    return await BookingDao.del_user_bookings(bookid=book_id, userid=user.id)
