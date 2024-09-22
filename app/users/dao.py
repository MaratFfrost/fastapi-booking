from fastapi import Response
from sqlalchemy import delete
from app.bookings.dao import BookingDao
from app.dao.base import BaseDAO
from app.users.models import Users
from app.database import async_session_maker

class UsersDAO(BaseDAO):
  model = Users

  @classmethod
  async def delete_user(cls, response: Response, user_id: int):
    async with async_session_maker() as session:
        query = await BookingDao.find_user_bookings(userid=user_id)
        if not query:
            stck = delete(cls.model).where(cls.model.id == user_id)
            await session.execute(stck)
            await session.commit()
            response.delete_cookie("booking_access_token")
            return "User has been deleted."
        else:
            for i in query:
                await BookingDao.del_user_bookings(userid=user_id, bookid=i.id)
            stck = delete(cls.model).where(cls.model.id == user_id)
            await session.execute(stck)
            await session.commit()
            response.delete_cookie("booking_access_token")
            return "User and all related bookings have been deleted."
