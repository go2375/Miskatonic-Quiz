# import sqlite3
# import bcrypt
# from pymongo import MongoClient
# from typing import Tuple

# import os

# BASE_DIR = os.path.dirname(__file__)
# DB_PATH = os.path.join(BASE_DIR, 'SQLite', 'data', 'bdd_connexion.sqlite')
# os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# # MongoDB
# client = MongoClient("mongodb://isen:isen@localhost:27017/")
# db = client['quiz_db']
# questions_collection = db['questions']

# # ---- SQLite Utilisateurs ----
# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS roles(
#         role_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         role TEXT NOT NULL
#     );
#     """)
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS utilisateurs(
#         utilisateur_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         nom_utilisateur TEXT NOT NULL,
#         identifiant TEXT NOT NULL UNIQUE,
#         mot_de_passe TEXT NOT NULL,
#         role_id INTEGER,
#         FOREIGN KEY (role_id) REFERENCES roles(role_id)
#     );
#     """)
#     conn.commit()
#     conn.close()

# def create_user(nom_utilisateur: str, identifiant: str, mot_de_passe: str, role_id: int = 1) -> Tuple[bool, str]:
#     hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         cur = conn.cursor()
#         cur.execute("""
#             INSERT INTO utilisateurs (nom_utilisateur, identifiant, mot_de_passe, role_id)
#             VALUES (?, ?, ?, ?)
#         """, (nom_utilisateur, identifiant, hashed_password, role_id))
#         conn.commit()
#         return True, "Utilisateur créé avec succès !"
#     except sqlite3.IntegrityError:
#         return False, "Identifiant déjà utilisé"
#     finally:
#         conn.close()

# def authenticate_user(identifiant: str, mot_de_passe: str) -> bool:
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     cur.execute("SELECT mot_de_passe FROM utilisateurs WHERE identifiant = ?", (identifiant,))
#     row = cur.fetchone()
#     conn.close()
#     if not row:
#         return False
#     stored_hash = row[0]
#     if isinstance(stored_hash, str):
#         stored_hash = stored_hash.encode('utf-8')
#     return bcrypt.checkpw(mot_de_passe.encode('utf-8'), stored_hash)

# def change_password(identifiant: str, ancien_password: str, nouveau_password: str) -> Tuple[bool, str]:
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT mot_de_passe FROM utilisateurs WHERE identifiant = ?", (identifiant,))
#         row = cur.fetchone()
#         if not row:
#             return False, "Identifiant introuvable"
#         hashed_old = row[0]
#         if isinstance(hashed_old, str):
#             hashed_old = hashed_old.encode('utf-8')
#         if not bcrypt.checkpw(ancien_password.encode('utf-8'), hashed_old):
#             return False, "Ancien mot de passe incorrect"
#         hashed_new = bcrypt.hashpw(nouveau_password.encode('utf-8'), bcrypt.gensalt())
#         cur.execute("UPDATE utilisateurs SET mot_de_passe = ? WHERE identifiant = ?", (hashed_new, identifiant))
#         conn.commit()
#         return True, "Mot de passe changé avec succès !"
#     finally:
#         conn.close()

# # # ---- MongoDB Questions ----


# import bcrypt
# from database.connections import get_sqlite_connection

# def create_user(username: str, password: str, role_id: int = 1):
#     hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#     conn = get_sqlite_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute(
#             "INSERT INTO utilisateurs (nom_utilisateur, identifiant, mot_de_passe, role_id) VALUES (?, ?, ?, ?)",
#             (username, username, hashed, role_id)
#         )
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False
#     finally:
#         conn.close()