from fastapi import APIRouter, FastAPI


from app.bookings.router import router as router_booking
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels



app = FastAPI()
app.include_router(router_users)
app.include_router(router_booking)
app.include_router(router_hotels)
