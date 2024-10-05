from app.dao.base import BaseDAO
from app.admin.models import Admins


class AdminDao(BaseDAO):
  model = Admins
