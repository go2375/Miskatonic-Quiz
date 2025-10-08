from fastapi import FastAPI, HTTPException
from dto.models import EtudiantModel
from dto.services import EtudiantService


app = FastAPI()

@app.get("/")
def get_index():
    return {"message": "Hello"}

@app.put("/api/etudiants/{etudiant_id}")
def update_etudiant(etudiant_id: int, etudiant: EtudiantModel):
    updated_etudiant = EtudiantService.update_etudiant_by_id(etudiant_id, etudiant)
    if updated_etudiant is None:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return updated_etudiant

@app.get("/api/etudiants/{etudiant_id}")
def get_etudiant(etudiant_id: int):
    etudiant = EtudiantService.get_etudiant_by_id(etudiant_id)
    if etudiant is None:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return etudiant

@app.get("/api/etudiants/")
def get_all_etudiants():
    etudiants = EtudiantService.get_all_etudiants()
    if not etudiants:
        raise HTTPException(status_code=404, detail="Aucun étudiant trouvé")
    return etudiants

@app.post("/api/etudiants/")
def create_etudiant(etudiant: EtudiantModel):
    id_etudiant = EtudiantService.add_etudiant(etudiant)
    return {"id": id_etudiant}

@app.delete("/api/etudiants/{etudiant_id}")
def del_etudiant(etudiant_id: int):
    result = EtudiantService.delete_etudiant_by_id(etudiant_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Etudiant not found")
    return {"message": "Etudiant deleted successfully"}







# @app.delete("/animals/{animal_id}")
# async def delete_animal(animal_id: int):
#     result = AnimalService.delete_animal_by_id(animal_id)
    
#     if result is None:
#         return {"error": "Animal not found"}
    
#     return {"message": "Animal deleted successfully"}



# @app.get("/animals/{animal_id}")
# async def get_animal(animal_id: int):
#     animal = AnimalService.get_animal_by_id(animal_id)



# #Endpoint : Ajouter un animal
# @app.post("/animals/")
# async def create_animal(animal: AnimalModel):
#     id_animal = AnimalService.add_animal(animal)
#     return {"id": id_animal}

# #Endpoint : Récupérer tous les noms des animaux
# @app.get("/animals/")
# async def get_all_animals():
#     animals = AnimalService.get_all_animals()
#     return animals

# #Endpoint : Récupérer un animal par son id
# @app.get("/animals/{animal_id}")
# async def get_animal(animal_id: int):
#     animal = AnimalService.get_animal_by_id(animal_id)
    
#     if animal is None:
#         return {"error": "Animal not found"}
    
#     return animal
