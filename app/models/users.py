from pydantic import BaseModel

# Pour créer un utilisateur (entrée de formulaire)
class UserCreate(BaseModel):
    username: str
    password: str

# Pour stockage en base (mot de passe haché)
class UserInDB(BaseModel):
    username: str
    hashed_password: str