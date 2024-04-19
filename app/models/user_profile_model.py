from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from . import Base

class UserProfile(Base):
    __tablename__ = "user_profile"

    user_profile_id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    age = Column(Integer, CheckConstraint('age > 19 AND age < 100'))
    personal_id = Column(Integer, unique=True)
    phone_number = Column(String)

    user_id = Column(Integer, ForeignKey("user.user_id"))
    user = relationship("User", back_populates="user_profile")
