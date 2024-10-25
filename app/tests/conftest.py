import asyncio
from datetime import datetime
import json
import pytest
from sqlalchemy import insert
from app.config import settings
from app.database import Base, async_session_maker, engine

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock(model: str):
      with open(f"app/tests/mock_{model}.json") as file:
        return json.load(file)

    def convert_dates(data):
      for item in data:
        for key, value in item.items():
            if isinstance(value, str) and value.count('-') == 2:
                try:
                  item[key] = datetime.strptime(value, '%Y-%m-%d')
                except:
                    pass
      return data


    hotels = convert_dates(open_mock("hotels"))
    rooms = convert_dates(open_mock("rooms"))
    users = convert_dates(open_mock("users"))
    bookings = convert_dates(open_mock("bookings"))

    async with async_session_maker() as session:
      add_hotels = insert(Hotels).values(hotels)
      add_rooms = insert(Rooms).values(rooms)
      add_users = insert(Users).values(users)
      add_bookings = insert(Bookings).values(bookings)

      await session.execute(add_hotels)
      await session.execute(add_rooms)
      await session.execute(add_users)
      await session.execute(add_bookings)

      await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
   loop = asyncio.get_event_loop_policy().new_event_loop()
   yield loop
   loop.close()