from dbase.models.users import User
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from core.hashed import HashPassword


def create_new_user(user : UserCreate, db : Session):
    user = User(
        email = user.email,
        password = HashPassword().get_password_hash(user.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(email:str,db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user