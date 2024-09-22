from datetime import date
from pydantic import BaseModel

class SBookingDel(BaseModel):
  roomid: int
  nums_of_rooms: int


class DeleteBookingRequest(BaseModel):
    user_id: int
    room_id: int
    id: int
    date_from: date
    date_to: date
