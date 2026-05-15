from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Location(Base):
    __tablename__ = "location"

    zip = Column(String, primary_key=True)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
