# import os
# import sqlite3
# from pymongo import MongoClient

# # --- SQLite ---
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# DB_PATH = os.path.join(BASE_DIR, 'SQLite', 'data', 'bdd_connexion.sqlite')
# os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# def get_sqlite_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row  # pour accéder aux colonnes par nom
#     return conn

# # --- MongoDB ---
# MONGO_URI = "mongodb://isen:isen@localhost:27017/"
# MONGO_DB_NAME = "quiz_db"

# mongo_client = MongoClient(MONGO_URI)
# mongo_db = mongo_client[MONGO_DB_NAME]

# questions_collection = mongo_db['questions']
# questionnaires_collection = mongo_db['questionnaires']