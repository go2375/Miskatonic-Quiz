from app.database import get_user_collection
from app.security import hash_password, verify_password
from app.models.user import UserCreate, UserInDB

def create_user(user: UserCreate):
    hashed = hash_password(user.password)
    user_dict = {"username": user.username, "email": user.email, "hashed_password": hashed}
    get_user_collection().insert_one(user_dict)
    return user_dict

def authenticate_user(username: str, password: str):
    user = get_user_collection().find_one({"username": username})
    if user and verify_password(password, user['hashed_password']):
        return user
    return None