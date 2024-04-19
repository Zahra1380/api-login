from pydantic import BaseModel, Field
from typing import Union


class ProfileBase(BaseModel):
    personal_id: int
    name: str
    last_name: str
    age: int = Field(gt=19, lt=100)
    phone_number: str =Field(pattern=r"^09[0|1|2|3][0-9]{8}$")

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    user_profile_id: int
    user_id: int

    class Config:
        orm_mode = True

class ProfileUpdate(ProfileBase):
    personal_id: Union[int, None] = None
    name: Union[str, None] = None
    last_name: Union[str, None] = None
    age: Union[int, None] = None
    phone_number: Union[str, None] = None

