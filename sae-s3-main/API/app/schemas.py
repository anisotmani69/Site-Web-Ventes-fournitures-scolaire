import datetime
from typing import Union, List
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict
from app import models

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom_utilisateur: str
    nom: str
    prenom: str
    email: str
    adresse: str
    ville: str
    telephone: str
    reduction: int |None = None


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom_utilisateur: str
    email: str
    mot_de_passe: str

class UserData(User):
    id: int
    date_inscription: datetime.date


class UserInDb(User):
    mot_de_passe: str


class VendeurCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom_utilisateur: str
    email: str
    mot_de_passe: str


class Vendeur(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom_utilisateur: str
    nom_vendeur: str
    email: str
    adresse: str
    ville: str
    telephone: str


class VendeurData(Vendeur):
    id: int
    date_inscription: datetime.date

class VendeurInDb(VendeurData):
    mot_de_passe: str


class VendeurInDb(Vendeur):
    mot_de_passe: str


class Ville(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom_ville: str
    code_ville: str


class VilleData(Ville):
    id: int


class Avis_modification(BaseModel):
    note: int
    text: str

class Avis(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_utilisateur: int
    id_article: int
    note: int
    text: str
    dateAvis: str | None


class AvisData(Avis):
    id: int


class Couleur(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: str



class CouleurData(Couleur):
    id: int


class Marque(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: str


class MarqueData(Marque):
    id: int


class Categorie(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: str



class CategorieData(Categorie):
    id: int


class Type(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: str



class TypeData(Type):
    id: int


class Facture(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_utilisateur: int
    date: datetime.date




class FactureData(Facture):
    id: int

class ArticleCreate(BaseModel):
    id_marque: int
    id_categorie: int
    id_vendeur: int
    id_type: int
    id_couleur: int
    titre: str
    description: str
    prix: float
    image: str
class Article(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    titre: str
    description: str
    prix: float
    image: str 
    id_vendeur: int
    marque: MarqueData |None = None
    categorie : CategorieData | None = None
    #vendeur : VendeurData | None = None
    type : TypeData | None = None
    couleur : CouleurData | None = None
    note : float | None = None
    avis : list[Avis] = []



class ArticleData(Article):
    id: int


class ArticleUpdate(BaseModel):
    id_marque: int | None = None
    id_categorie: int | None = None
    id_vendeur: int | None = None
    id_type: int | None = None
    id_couleur: int | None = None
    titre: str | None = None
    description: str | None = None
    prix: float | None = None
    image: str | None = None


class Panier(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_article: int
    type: int
    nb_article: int
    datePanier: str


class PanierData(Panier):
    id_utilisateur: int
    id: int


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class ArticleFilter(Filter):
    id: int | None = None
    titre__like: str | None = None
    id_marque: int | None = None
    id_categorie: int | None = None
    id_vendeur: int | None = None
    id_type: int | None = None
    prix__lte: int | None = None
    custom_order_by: List[str] |None = None

    class Constants(Filter.Constants):
        model = models.Article
        ordering_field_name = "custom_order_by"
        search_model_fields = ["id_marque", "id_categorie", "id_type"]


class Historique(BaseModel):
    id_utilisateur: int
    id_article: int



class CreateCommande(BaseModel):
    prenomCommande : str
    nomCommande: str
    dateCommande : str
    adresseLivraison : str
    infosSupp : str
    nom_ville : str



class Commande(BaseModel):
    #model_config = ConfigDict(from_attributes=True)
    id: int
    prenomCommande : str
    nomCommande: str
    dateCommande : str
    adresseLivraison : str
    infosSupp : str
    id_user : int
    nom_ville : str
    montant: float | None = None
    paniers_item : str
    montant_reduc : float |None = None
