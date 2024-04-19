from sqlalchemy.orm import Session
import models.user_model as user_model
import schemas.user_schema as user_schema
from api import pwd_context

def get_user(db: Session, user_id:int):
    return db.query(user_model.User).filter(user_model.User.user_id == user_id).first()
   

async def get_user_by_email(db: Session, email:str):
    try:
        return db.query(user_model.User).filter(user_model.User.user_email == email).first()
    except Exception as e:
        return {'error': str(e)}

def get_users(db:Session):
    try:
        return db.query(user_model.User).all()
    except Exception as e:
        return {'error': str(e)}

def create_user(db:Session, user: user_schema.UserCreate):
    try:
        hashed_passwrod = pwd_context.hash(user.user_passwrod)
        db_user = user_model.User(user_email=user.user_email, user_password = hashed_passwrod)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        return {'error': str(e)}

def update_user(db:Session, user_schema: user_schema.UserUpdate, user_model: user_model.User):
        try:
            if user_schema.user_email is not None:
                user_model.user_email = user_schema.user_email
            if user_schema.is_active is not None:
                user_model.is_active = user_schema.is_active
                print(user_model.is_active)

            db.commit()  # Commit the changes to the database
            db.refresh(user_model)  # Refresh the user_profile
            return(user_model)
        except Exception as e:
            db.rollback()
            return {'error': str(e)}

def delete_user(db:Session, user: user_model.User):
        try:
            db.delete(user)
            db.commit()
        except Exception as e:
            db.rollback()
            return {'error': str(e)}

def change_user_password(db:Session, user_schema: user_schema.UserChangePassword, user_model: user_model.User):
    try:
        user_model.user_password = pwd_context.hash(user_schema.user_new_passwrod)
        db.commit()  # Commit the changes to the database
        db.refresh(user_model)  # Refresh the user_profile
        return(user_model)
    except Exception as e:
        db.rollback()
        return {'error': str(e)}