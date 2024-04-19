from pydantic import BaseModel, EmailStr
from typing import Union



class UserBase(BaseModel):
    user_email: EmailStr

class UserCreate(UserBase):
    user_passwrod: str

class User(UserBase):

    # when reading a user,
    # we can now declare that items will contain 
    # the items that belong to this user.
    user_id: int
    is_active: bool
    

    class Config:
        # And with this, the Pydantic model is compatible 
        # with ORMs, and you can just 
        # declare it in the response_model argument in your path operations.
        orm_mode = True
        from_attributes=True

class UserUpdate(UserBase):
    user_email:  Union[EmailStr, None] = None 
    is_active: Union[bool, None] = None 

class UserLogin(UserCreate):
    pass

class UserChangePassword(BaseModel):
    user_old_password: str

    user_new_passwrod: str
    user_repeate_new_passwrod: str

class UserLogin(BaseModel):
    user_email: EmailStr
    user_passwrod: str

    