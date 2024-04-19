from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm import relationship
from . import Base
from api import pwd_context


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_email = Column(String, unique=True, index=True)
    user_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    user_profile = relationship("UserProfile", back_populates="user", cascade="all,delete" )

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.user_password)