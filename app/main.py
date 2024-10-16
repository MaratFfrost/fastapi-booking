from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


from sqladmin import Admin

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend



from redis import asyncio as aioredis

from app.admin.views import  SuperUsers, UserAdmin, HotelAdmin, RoomsAdmin, UserBokings
from app.admin.auth import authentication_backend
from app.pages.router import router as router_pages
from app.bookings.router import router as router_booking
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.database import engine

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield



app = FastAPI(lifespan=lifespan)



app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_pages)
app.include_router(router_users)
app.include_router(router_booking)
app.include_router(router_hotels)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(SuperUsers)
admin.add_view(UserBokings)
