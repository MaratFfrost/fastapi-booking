from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.database import Base

class Rooms(Base):
  __tablename__ = "rooms"

  id = Column(Integer, primary_key=True, nullable=False)
  hotel_id = Column(ForeignKey('hotels.id'), nullable=False)
  name = Column(String, nullable=False)
  location = Column(String, nullable=False)
  price = Column(Integer, nullable=False)
  services = Column(JSON, nullable=True)
  description = Column(String, nullable=True)
  quantity = Column(Integer, nullable=False)
  image_id = Column(Integer)
