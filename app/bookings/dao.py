from datetime import date
from fastapi import HTTPException
from sqlalchemy import and_, delete, func, insert, or_, select, text

from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.rooms.models import Rooms


class BookingDao(BaseDAO):
  model = Bookings


  @classmethod
  async def del_user_bookings(cls, bookid: int, userid: int):
    async with async_session_maker() as session:
        query = await BookingDao.find_user_bookings(userid=userid)
        if not query:
            raise HTTPException(status_code=404, detail="User has no bookings")
        if bookid not in [i.id for i in query]:
            raise HTTPException(status_code=404, detail="Booking not found")
        stmt = delete(Bookings).where(and_(Bookings.user_id == userid, Bookings.id == bookid))
        await session.execute(stmt)
        await session.commit()
        return {"message": "Booking deleted successfully"}


  @classmethod
  async def find_user_bookings(cls, userid:int):
    async with async_session_maker() as session:
      query = select(cls.model).filter_by(user_id=userid)
      result = await session.execute(query)
      return result.scalars().all()

  @classmethod
  async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            try:
                room_exists = await session.execute(select(Rooms.id).where(Rooms.id == room_id))
                if not room_exists.scalar():
                    raise HTTPException(status_code=404)
                booked_rooms_query = text("""
                    WITH booked_rooms AS (
                        SELECT room_id
                        FROM bookings
                        WHERE room_id = :room_id
                          AND (
                            (date_from >= :date_from AND date_from <= :date_to) OR
                            (date_from <= :date_from AND date_to > :date_to)
                          )
                    )
                    SELECT (r.quantity - COALESCE(COUNT(br.room_id), 0)) AS rooms_left
                    FROM rooms r
                    LEFT JOIN booked_rooms br ON r.id = br.room_id
                    WHERE r.id = :room_id
                    GROUP BY r.quantity
                """)

                rooms_left_result = await session.execute(booked_rooms_query, {"room_id": room_id, "date_from": date_from, "date_to": date_to})
                rooms_left = rooms_left_result.scalar()
                if rooms_left is not None and rooms_left > 0:
                    get_price_query = text("SELECT price FROM rooms WHERE id = :room_id")
                    price_result = await session.execute(get_price_query, {"room_id": room_id})
                    price = price_result.scalar()
                    if price is not None:
                        add_booking_query = text("""
                            INSERT INTO bookings (room_id, user_id, date_from, date_to, price)
                            VALUES (:room_id, :user_id, :date_from, :date_to, :price)
                            RETURNING *;
                        """)
                        new_booking_result = await session.execute(add_booking_query, {"room_id": room_id, "user_id": user_id, "date_from": date_from, "date_to": date_to, "price": price})
                        await session.commit()
                        new_booking = new_booking_result.fetchone()

                        return {"status": "success", "booking": new_booking}, 201
                    else:
                        return {"status": "error", "message": "Room price not found"}, 500
                else:
                    raise HTTPException(status_code=409)
            except Exception as e:
                raise HTTPException(status_code=404)
