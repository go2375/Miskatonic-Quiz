import os
import sqlite3
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from functools import wraps
import random

app = Flask(__name__)
app.secret_key = "une_clef_secrete"

# --- Base SQLite ---
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'SQLite', 'data', 'bdd_connexion.sqlite')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# --- Initialisation SQLite ---
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS roles(
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs(
    utilisateur_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_utilisateur TEXT NOT NULL,
    identifiant TEXT NOT NULL UNIQUE,
    mot_de_passe TEXT NOT NULL,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
""")
conn.commit()
conn.close()

# --- Connexion MongoDB ---
client = MongoClient("mongodb://isen:isen@localhost:27017/")
db = client['quiz_db']
questions_collection = db['questions']

# ======================= UTILITAIRES =======================
def get_user_password(identifiant):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT mot_de_passe FROM utilisateurs WHERE identifiant = ?", (identifiant,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def update_user_password(identifiant, new_hashed):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE utilisateurs SET mot_de_passe = ? WHERE identifiant = ?", (new_hashed, identifiant))
    conn.commit()
    conn.close()

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash("Veuillez vous connecter d'abord")
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return wrapper

# ======================= ROUTES =======================

# --- CGU ---
@app.route('/cgu')
def cgu():
    return render_template('cgu.html')

# --- LOGIN ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        identifiant = request.form.get('identif', '').strip()
        mdp = request.form.get('password', '')

        if not identifiant or not mdp:
            flash("Veuillez remplir tous les champs")
            return redirect(url_for('home'))

        stored_hash = get_user_password(identifiant)
        if stored_hash:
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')
            if bcrypt.checkpw(mdp.encode('utf-8'), stored_hash):
                session['user'] = identifiant
                return redirect(url_for('selection'))

        flash("Identifiant ou mot de passe incorrect")
        return redirect(url_for('home'))

    return render_template('index.html')

# --- INSCRIPTION ---
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        identifiant = request.form.get('identif', '').strip()
        mot_de_passe = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not identifiant or not mot_de_passe or not confirm_password:
            flash("Tous les champs sont obligatoires")
            return redirect(url_for('inscription'))

        if mot_de_passe != confirm_password:
            flash("Les mots de passe ne correspondent pas")
            return redirect(url_for('inscription'))

        hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        role_id = 1

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO utilisateurs (nom_utilisateur, identifiant, mot_de_passe, role_id)
                VALUES (?, ?, ?, ?)
            """, (identifiant, identifiant, hashed_password, role_id))
            conn.commit()
            flash("Utilisateur créé avec succès !")
            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            flash("Identifiant déjà utilisé")
            return redirect(url_for('inscription'))
        finally:
            conn.close()

    return render_template('create.html')

# --- CHANGEMENT MOT DE PASSE ---
@app.route('/changer_mdp', methods=['GET', 'POST'])
@login_required
def changer_mdp():
    identifiant = session['user']
    if request.method == 'POST':
        ancien_mdp = request.form.get('ancien_password', '')
        nouveau_mdp = request.form.get('nouveau_password', '')
        confirm_mdp = request.form.get('confirm_password', '')

        if not ancien_mdp or not nouveau_mdp or not confirm_mdp:
            flash("Tous les champs sont obligatoires")
            return redirect(url_for('changer_mdp'))

        if nouveau_mdp != confirm_mdp:
            flash("Les nouveaux mots de passe ne correspondent pas")
            return redirect(url_for('changer_mdp'))

        stored_hash = get_user_password(identifiant)
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
        if not bcrypt.checkpw(ancien_mdp.encode('utf-8'), stored_hash):
            flash("Ancien mot de passe incorrect")
            return redirect(url_for('changer_mdp'))

        hashed_new = bcrypt.hashpw(nouveau_mdp.encode('utf-8'), bcrypt.gensalt())
        update_user_password(identifiant, hashed_new)
        flash("Mot de passe changé avec succès !")
        return redirect(url_for('home'))

    return render_template('changer_mdp.html')

# --- RESET MOT DE PASSE ---
@app.route('/reset_mdp', methods=['GET', 'POST'])
def reset_mdp():
    if request.method == 'POST':
        identifiant = request.form.get('identif', '').strip()
        nouveau_mdp = request.form.get('nouveau_password', '')
        confirm_mdp = request.form.get('confirm_password', '')

        if not identifiant or not nouveau_mdp or not confirm_mdp:
            flash("Tous les champs sont obligatoires")
            return redirect(url_for('reset_mdp'))

        if nouveau_mdp != confirm_mdp:
            flash("Les mots de passe ne correspondent pas")
            return redirect(url_for('reset_mdp'))

        if get_user_password(identifiant) is None:
            flash("Identifiant introuvable")
            return redirect(url_for('reset_mdp'))

        hashed_new = bcrypt.hashpw(nouveau_mdp.encode('utf-8'), bcrypt.gensalt())
        update_user_password(identifiant, hashed_new)
        flash("Mot de passe réinitialisé avec succès !")
        return redirect(url_for('home'))

    return render_template('reset_mdp.html')

# --- AJOUT DE QUESTIONS ---
@app.route('/add_quest', methods=['GET', 'POST'])
@login_required
def add_quest():
    test_types = ["QCM", "Vrai/Faux", "Texte Libre"]
    subjects = questions_collection.distinct("subject")
    if request.method == 'POST':
        flash("Questions ajoutées avec succès !")
        return redirect(url_for('choix'))
    return render_template('add_quest.html', subjects=subjects, test_types=test_types)

# --- SELECTION DE QUESTIONS ---
@app.route('/selection', methods=['GET', 'POST'])
@login_required
def selection():
    sujets = questions_collection.distinct("subject")
    categories = questions_collection.distinct("use")
    selected_subjects = []
    selected_categories = []

    if request.method == 'POST':
        selected_subjects = request.form.getlist('subject')
        selected_categories = request.form.getlist('category')
        if not selected_subjects or not selected_categories:
            flash("Veuillez choisir au moins un sujet et une catégorie.")
            return redirect(url_for('selection'))

        return redirect(url_for('visualisation',
                                subjects=",".join(selected_subjects),
                                categories=",".join(selected_categories)))

    return render_template("selection.html",
                           sujets=sujets,
                           categories=categories,
                           selected_subjects=selected_subjects,
                           selected_categories=selected_categories)

# --- VISUALISATION DU QUIZ ---
@app.route('/visualisation')
@login_required
def visualisation():
    subjects = request.args.get('subjects', '').split(',')
    categories = request.args.get('categories', '').split(',')

    questions_cursor = questions_collection.find({
        "subject": {"$in": subjects},
        "use": {"$in": categories}
    })

    questions_list = []
    sujets_set = set()
    for q in questions_cursor:
        questions_list.append({
            "question": q.get("question"),
            "subject": q.get("subject"),
            "possible_answers": list(q.get("responses", {}).values()),
            "correct_answers": q.get("correct", "").split(",")
        })
        sujets_set.add(q.get("subject"))

    random.shuffle(questions_list)
    return render_template('visualisation.html',
                           subjects=list(sujets_set),
                           categories=categories,
                           questions=questions_list)

# --- LOGOUT ---
@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    flash("Déconnecté avec succès")
    return redirect(url_for('home'))

# ======================= LANCEMENT =======================
if __name__ == '__main__':
    app.run(debug=True)
