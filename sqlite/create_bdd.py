import sqlite3

DB_NAME = "utilisateurs.db"
conn = sqlite3.connect(DB_NAME)

# Script SQL complet
schema_sql = """



CREATE TABLE IF NOT EXISTS roles (
    id_role INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_role TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS utilisateurs (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_utilisateur TEXT NOT NULL,
    identifiant TEXT NOT NULL UNIQUE, 
    id_role INTEGER NOT NULL,
    FOREIGN KEY (id_role) REFERENCES roles(id_role) ON DELETE RESTRICT
);


INSERT INTO roles (nom_role) VALUES ('Étudiant');
INSERT INTO roles (nom_role) VALUES ('Enseignant');
INSERT INTO roles (nom_role) VALUES ('Administrateur');
"""


conn.executescript(schema_sql)

print(f"Base SQLite '{DB_NAME}' créée avec tables (roles, utilisateurs).")

conn.commit()
conn.close()
