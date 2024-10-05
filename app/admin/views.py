from sqladmin import  ModelView

from fastapi_cache import FastAPICache

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

  @staticmethod
  def get_main_admin():
    redis = FastAPICache.get_backend().redis

    #admin_data_from_cache =  redis.hgetall(f"current_admin:{admin.name}")
