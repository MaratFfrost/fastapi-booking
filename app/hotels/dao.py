from app.dao.base import BaseDAO
from app.hotels.models import Hotels

from app.database import async_session_maker
from sqlalchemy import select, insert
class HotelsDAO(BaseDAO):
  model = Hotels


  @classmethod
  async def find_all_in_limit(cls, limit, **filter_by):
    async with async_session_maker() as session:
      query = select(cls.model).filter_by(**filter_by).limit(limit)
      result = await session.execute(query)
      return result.scalars().all()
