from sqlalchemy.orm import Session
import models.user_profile_model as user_profile_model
import schemas.profile_schema as profile_schema

def get_user_profile(db:Session, user_id: int):
    try:
        return db.query(user_profile_model.UserProfile).filter(user_profile_model.UserProfile.user_id == user_id).first()
    except Exception as e:
        # for when error occure evry thing that save inside the db will be rolback
        return {'error': str(e)}

def create_user_profile(db: Session, profile: profile_schema.ProfileCreate, user_id: int):
    try:
        db_profile = user_profile_model.UserProfile(**profile.dict(), user_id=user_id)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    except Exception as e:
        db.rollback()
        return {'error': str(e)}  

def delete_user_profile(db: Session, user_profile: user_profile_model.UserProfile):
    try:
        db.delete(user_profile)
        db.commit()
    except Exception as e:
        db.rollback()
        return {'error': str(e)}
    
def update_user_profile(db: Session, profile: profile_schema.ProfileUpdate, user_profile: user_profile_model.UserProfile):
    try:
        if profile.personal_id is not None:
            user_profile.personal_id = profile.personal_id
        if profile.name is not None:
            user_profile.name = profile.name
        if profile.last_name is not None:
            user_profile.last_name = profile.last_name
        if profile.age is not None:
            user_profile.age = profile.age
        if profile.phone_number is not None:
            user_profile.phone_number = profile.phone_number
        db.commit()  # Commit the changes to the database
        db.refresh(user_profile)  # Refresh the user_profile
        return(user_profile)
    except Exception as e:
        db.rollback()
        return {'error': str(e)}
    

