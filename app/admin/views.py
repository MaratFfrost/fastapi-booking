from sqladmin import  ModelView

from fastapi_cache import FastAPICache

from app.bookings.models import Bookings
from app.users.models import Users
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.admin.models import Admins

class UserAdmin(ModelView, model=Users):
  name = "User"
  name_plural = "Users"
  icon = "fa-solid fa-user"
  column_list = [Users.id, Users.email]
  column_details_exclude_list = [Users.hashed_password]
  can_delete = False
  can_edit = False

class HotelAdmin(ModelView, model=Hotels):
  column_list = [Hotels.name]
  name = "Hotel"
  icon = 'fa-solid fa-hotel'


class RoomsAdmin(ModelView, model=Rooms):
  column_list = [Rooms.name, Rooms.hotel_id]
  name = "Room"
  icon = "fa-solid fa-bed"

class SuperUsers(ModelView, model=Admins):
  name ="SuperUser"
  column_list = [Admins.name, Users.email]
  #column_details_exclude_list = [Admins.hashed_password]
  icon = "fa-duotone fa-solid fa-user-tie"


class UserBokings(ModelView, model=Bookings):
  name="Booking"
  icon="fa-solid fa-bed"
  column_list = [Bookings.room_id, Bookings.user_id, Bookings.date_from, Bookings.date_to, Bookings.price]
  can_delete = False
  can_edit = False
