import os
import sqlite3
import bcrypt

# Chemin absolu vers la base SQLite
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'data', 'bdd_connexion.sqlite')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# ---- INITIALISATION DE LA BASE ----
def init_db():
    """Crée les tables roles et utilisateurs si elles n'existent pas"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Table roles
    cur.execute("""
    CREATE TABLE IF NOT EXISTS roles(
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL UNIQUE
    );
    """)

    # Table utilisateurs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS utilisateurs(
        utilisateur_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_utilisateur TEXT NOT NULL,
        identifiant TEXT NOT NULL UNIQUE,
        mot_de_passe BLOB NOT NULL,
        role_id INTEGER,
        FOREIGN KEY (role_id) REFERENCES roles(role_id)
    );
    """)

    # Insérer les rôles par défaut
    roles = ["enseignant", "etudiant", "administrateur"]
    for role in roles:
        cur.execute("INSERT OR IGNORE INTO roles (role) VALUES (?)", (role,))

    conn.commit()
    conn.close()


# ---- LOGIN ----
def add_users(nom_utilisateur, identifiant, mot_de_passe, role_id=1):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT mot_de_passe, role_id FROM utilisateurs WHERE identifiant=?", (identifiant,))
    result = cur.fetchone()

    if result:
        stored_hashed_password = result[0]
        if isinstance(stored_hashed_password, str):
            stored_hashed_password = stored_hashed_password.encode('utf-8')
        if bcrypt.checkpw(mot_de_passe.encode('utf-8'), stored_hashed_password):
            conn.close()
            return True, "Connexion réussie."
        else:
            conn.close()
            return False, "Mot de passe incorrect, veuillez le changer."
    else:
        conn.close()
        return False, "Identifiant inconnu, veuillez créer un compte."

# ---- CREATION UTILISATEUR ----
def register_user(nom_utilisateur, identifiant, mot_de_passe, role_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Vérifie si identifiant déjà utilisé
    cur.execute("SELECT * FROM utilisateurs WHERE identifiant=?", (identifiant,))
    result = cur.fetchone()

    if result:
        conn.close()
        return False, "Identifiant déjà utilisé, changez votre mot de passe"

    hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
    cur.execute(
        "INSERT INTO utilisateurs (nom_utilisateur, identifiant, mot_de_passe, role_id) VALUES (?, ?, ?, ?)",
        (nom_utilisateur, identifiant, hashed_password, role_id)
    )
    conn.commit()
    conn.close()
    return True, "Vous êtes bien inscrit !"