from pymongo import MongoClient

def get_database():
    # Connexion à MongoDB
    CONNECTION_STRING = "mongodb://isen:isen@localhost:27017/admin"
    client = MongoClient(CONNECTION_STRING)
    
    # Création / récupération de la base "etudiants"
    db = client['etudiants']
    
    return db

# Si on exécute le fichier directement
if __name__ == "__main__":   
    dbname = get_database()
    
    # Récupération de la collection "etudiants"
    etudiants_collection = dbname["etudiants"]
    
    print("Connexion à MongoDB réussie !")

