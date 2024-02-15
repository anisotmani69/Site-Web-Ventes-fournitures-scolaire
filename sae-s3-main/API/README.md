# Projet SAE (Partie API)

API faite avec **FastAPI** en python.   
La parie génération de la base de données à été faite avec **SqlAlchemy**.  
Avec l'**ORM** nous avons décidé de générer la base de données en **SQLite**.

## Installation

Pour installer les dépendances du projet, il faut exécuter la commande suivante :  
```bash
pip install -r requirements.txt
python -m uvicorn app.api:app --reload
```

## Endpoints

- **/** : Endpoint de test de l'API **GET**
- **/signup** : Endpoint d'inscription (création d'un compte) **POST**
- **/token** : Endpoint de connexion (retroune un token JWT à stocker) **POST**
- **/user/me** : Endpoint de récupération des informations de l'utilisateur connecté **GET**
- **/user/me** : Endpoint de suppression du compte de l'utilisateur connecté **DELETE**
- **/createproduct** : Endpoint de création d'un produit **POST**
- **/panier** : Endpoint de récupération du panier de l'utilisateur connecté **GET**
- **/panier** : Endpoint de d'ajout d'un article au panier de l'utilisateur connecté **PUT**
- **/panier** : Endpoint de suppression d'un article du panier de l'utilisateur connecté **DELETE**
- **/search** : Endpoint de recherche d'un article **GET**
- **/article** : Endpoint de modification d'un article **PATCH**
- **/article** : Endpoint de suppression d'un article **DELETE**