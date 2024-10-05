from sqlalchemy import Column, String, Integer
from app.database import Base

class Admins(Base):
  __tablename__ = "admins"

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False)
  hashed_password = Column(String, nullable=False)
