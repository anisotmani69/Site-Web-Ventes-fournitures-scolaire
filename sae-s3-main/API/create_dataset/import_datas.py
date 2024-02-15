import json
import sqlite3

conn = sqlite3.connect("../sql_app.db")
cursor = conn.cursor()

cursor.execute('DELETE FROM article;')
cursor.execute('DELETE FROM utilisateur;')
cursor.execute('DELETE FROM categorie;')
cursor.execute('DELETE FROM type;')
cursor.execute('DELETE FROM vendeur;')
cursor.execute('DELETE FROM avis;')
cursor.execute('DELETE FROM couleur;')
cursor.execute('DELETE FROM facture;')
cursor.execute('DELETE FROM panier;')
cursor.execute('DELETE FROM ville;')
cursor.execute('DELETE FROM marque;')
cursor.execute('DELETE FROM commande;')

conn.commit()

# 200 articles

user_url = "../../DataSet/utilisateur26.json"
user_data = json.load(open(user_url, encoding="utf-8"))

avis_url = "../../DataSet/avis500.json"
avis_data = json.load(open(avis_url, encoding="utf-8"))

ville_url = "../../DataSet/ville20.json"
ville_data = json.load(open(ville_url, encoding="utf-8"))

article_url = "../../DataSet/article.json"
article_data = json.load(open(article_url, encoding="utf-8"))

couleur_url = "../../DataSet/couleur.json"
couleur_data = json.load(open(couleur_url, encoding="utf-8"))

type_url = "../../DataSet/type.json"
type_data = json.load(open(type_url, encoding="utf-8"))

categorie_url = "../../DataSet/categorie.json"
categorie_data = json.load(open(categorie_url, encoding="utf-8"))

marque_url = "../../DataSet/marque.json"
marque_data = json.load(open(marque_url, encoding="utf-8"))
def import_article_data():
    try:
        for u in article_data:
            id_marque = u["id_marque"]
            id_categorie = u["id_categorie"]
            id_vendeur = u["id_vendeur"]
            id_type = u["id_type"]
            id_couleur = u["id_couleur"]
            titre = u["titre"]
            description = u["description"]
            prix = u["prix"]
            image = u["image"]
            cursor.execute("INSERT INTO article (id_marque, id_categorie, id_vendeur, id_type, id_couleur, titre, description, prix, image) VALUES(?,?,?,?,?,?,?,?,?)",
                           [id_marque, id_categorie, id_vendeur, id_type, id_couleur, titre, description, prix, image]
                           )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False
def import_user_data():
    try:
        for u in user_data:

            nom_utilisateur = u["nom_utilisateur"]
            mdp_hash = u["mdp_hashmdp_hash"]
            nom = u["nom"]
            prenom = u["prenom"]
            email = u["email"]
            adresse = u["adresse"]
            ville = u["ville"]
            telephone = u["telephone"]

            cursor.execute(
                "INSERT INTO utilisateur (nom_utilisateur, mdp_hash, nom, prenom, email, adresse, ville, telephone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [nom_utilisateur, mdp_hash, nom, prenom, email, adresse, ville, telephone]
            )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False


def import_vendeur_data():
    try:
        for u in user_data:

            nom_utilisateur = u["nom_utilisateur"]
            mdp_hash = u["mdp_hashmdp_hash"]
            nom_vendeur = u["nom"]
            email = u["email"]
            adresse = u["adresse"]
            ville = u["ville"]
            telephone = u["telephone"]

            cursor.execute(
                "INSERT INTO vendeur (nom_utilisateur, mdp_hash, nom_vendeur,  email, adresse, ville, telephone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                [nom_utilisateur, mdp_hash, nom_vendeur, email, adresse, ville, telephone]
            )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False


def import_avis_data():
    try:
        for a in avis_data:

            id_utilisateur = a["id_utilisateur"]
            id_article = a["id_article"]
            note = a["note"]
            text = a["text"]
            dateAvis = a["dateAvis"]

            cursor.execute(
                "INSERT INTO avis (id_utilisateur, id_article, note, text, dateAvis) VALUES (?, ?, ?, ?, ?)",
                [id_utilisateur, id_article, note, text, dateAvis]
            )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False


def import_ville_data():
    try:
        for v in ville_data:

            nom_ville = v["nom_ville"]
            code_ville = v["code_postal"]

            cursor.execute(
                "INSERT INTO ville (nom_ville, code_ville) VALUES (?, ?)",
                [nom_ville, code_ville]
            )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False


def import_couleur_data():
    try:
        for v in couleur_data:
            nom = v["nom"]

            cursor.execute(
                "INSERT INTO couleur (nom) VALUES (?)",
                [nom]
            )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False


def import_type_data():
    try:
        for v in type_data:
            nom = v["nom"]


            cursor.execute(
                "INSERT INTO type (nom) VALUES (?)",
                [nom]
            )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False
def import_categorie_data():
    try:
        for v in categorie_data:

            nom = v["nom"]


            cursor.execute(
                "INSERT INTO categorie (nom) VALUES (?)",
                [nom]
            )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False

def import_marque_data():
    try:
        for v in marque_data:

            nom = v["nom"]


            cursor.execute(
                "INSERT INTO marque (nom) VALUES (?)",
                [nom]
            )
        conn.commit()
        print("Tout s'est bien passé")
        return True
    except Exception as e:
        print(e)
        return False

import_marque_data()
import_user_data()
import_vendeur_data()
import_ville_data()
import_avis_data()
import_couleur_data()
import_categorie_data()
import_type_data()
import_article_data()

