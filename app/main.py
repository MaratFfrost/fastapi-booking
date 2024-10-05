from fastapi import FastAPI
from sqladmin import Admin, ModelView


from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from app.bookings.router import router as router_booking
from app.users.models import Users
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.database import engine

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    try:
        yield
    finally:
        await redis.close()



app = FastAPI(lifespan=lifespan)
app.include_router(router_users)
app.include_router(router_booking)
app.include_router(router_hotels)


admin = Admin(app, engine)


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    can_delete = False
    can_edit = False



admin.add_view(UserAdmin)
