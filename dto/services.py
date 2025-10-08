from .models import EtudiantModel
from .connexion import get_database

class EtudiantService:
    db = get_database()
    collection = db["etudiants"]

    @classmethod
    def get_etudiant_by_id(cls, etudiant_id: int):
        return cls.collection.find_one({"id": etudiant_id})

    @classmethod
    def get_all_etudiants(cls):
        return list(cls.collection.find())

    @classmethod
    def add_etudiant(cls, etudiant: EtudiantModel):
        result = cls.collection.insert_one(etudiant.dict())
        return str(result.inserted_id)

    @classmethod
    def delete_etudiant_by_id(cls, etudiant_id: int):
        result = cls.collection.delete_one({"id": etudiant_id})
        return result.deleted_count if result.deleted_count > 0 else None

    @classmethod
    def update_etudiant_by_id(cls, etudiant_id: int, etudiant: EtudiantModel):
        result = cls.collection.update_one(
            {"id": etudiant_id}, {"$set": etudiant.dict()}
        )
        if result.matched_count == 0:
            return None
        return cls.collection.find_one({"id": etudiant_id})