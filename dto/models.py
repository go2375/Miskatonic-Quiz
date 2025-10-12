# from pydantic import BaseModel, Field
# from typing import Optional, Dict, List

# class UserCreate(BaseModel):
#     nom_utilisateur: str
#     identifiant: str
#     mot_de_passe: str
#     confirm_password: str

# class UserLogin(BaseModel):
#     identifiant: str
#     mot_de_passe: str

# class UserChangePassword(BaseModel):
#     identifiant: str
#     ancien_password: str
#     nouveau_password: str
#     confirm_password: str

# class QuestionCreate(BaseModel):
#     subject: str
#     use: str
#     question: str
#     responses: Dict[str, str]
#     correct: str
#     remark: Optional[str] = None