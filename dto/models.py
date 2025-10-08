from pydantic import BaseModel

class EtudiantModel(BaseModel):
    nom: str
    prenom: str
    age: int
    classe: str