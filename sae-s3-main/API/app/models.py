import datetime

from sqlalchemy import Boolean, Column, Integer, String, Date, Time, ForeignKey, func, select, ARRAY
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.hybrid import hybrid_property
from .database import Base

from typing import List

class Ville(Base):
    __tablename__ = "ville"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    nom_ville = Column(String, unique=True, index=True)
    code_ville = Column(String, unique=True, index=True)

    vendeurs = relationship("Vendeur", back_populates="ville_res")
    clients = relationship("User", back_populates="ville_res")
    commandes = relationship("Commande", back_populates="ville")

class User(Base):
    __tablename__ = "utilisateur"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    nom_utilisateur = Column(String, unique=True, index=True)
    mdp_hash = Column(String)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    adresse = Column(String, index=True)
    ville = Column(String, ForeignKey("ville.nom_ville"))
    telephone = Column(String, index=True, default=None)
    date_inscription = Column(Date, index=True, default=datetime.date.today())
    reduction = Column(Integer, default=0)

    #paniers = relationship("Panier", back_populates="utilisateur", cascade="all,delete")
    ville_res = relationship("Ville", back_populates="clients")
    avis = relationship("Avis", back_populates="utilisateur")
    factures = relationship("Facture", back_populates="utilisateur")

class Vendeur(Base):
    __tablename__ = "vendeur"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    nom_utilisateur = Column(String, unique=True, index=True)
    mdp_hash = Column(String)
    nom_vendeur = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    adresse = Column(String, index=True)
    ville = Column(String, ForeignKey("ville.nom_ville"))
    telephone = Column(String, index=True, default=None)
    date_inscription = Column(Date, index=True, default=datetime.date.today())

    ville_res = relationship("Ville", back_populates="vendeurs")
    articles = relationship("Article", back_populates="vendeur")

class Avis(Base):
    __tablename__ = "avis"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id"), index=True)
    id_article = Column(Integer, ForeignKey("article.id"), index=True)
    note = Column(Integer, index=True)
    text = Column(String)
    dateAvis = Column(String, index=True)

    utilisateur = relationship("User", back_populates="avis")
    article = relationship("Article", back_populates="avis")

class Couleur(Base):
    __tablename__ = "couleur"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    nom = Column(String, unique=True, index=True)
    articles = relationship("Article", back_populates="couleur")


class Marque(Base):
    __tablename__ = "marque"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    nom = Column(String, unique=True, index=True)
    articles = relationship("Article", back_populates="marque")


class Categorie(Base):
    __tablename__ = "categorie"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    nom = Column(String, unique=True, index=True)

    articles = relationship("Article", back_populates="categorie")


class Type(Base):
    __tablename__ = "type"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    nom = Column(String, unique=True, index=True)
    articles = relationship("Article", back_populates="type")


class Facture(Base):
    __tablename__ = "facture"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id"), index=True)
    date_facture = Column(Date, index=True)

    utilisateur = relationship("User", back_populates="factures")

class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    id_marque = Column(Integer, ForeignKey("marque.id"), index=True)
    id_categorie = Column(Integer, ForeignKey("categorie.id"), index=True)
    id_vendeur = Column(Integer, ForeignKey("vendeur.id"), index=True)
    id_type = Column(Integer, ForeignKey("type.id"), index=True)
    id_couleur = Column(Integer, ForeignKey("couleur.id"), index=True)
    titre = Column(String, unique=True, index=True)
    description = Column(String)
    prix = Column(Integer, index=True)
    image = Column(String, unique=True)

    marque = relationship("Marque", back_populates="articles")
    categorie = relationship("Categorie", back_populates="articles")
    vendeur = relationship("Vendeur", back_populates="articles")
    type = relationship("Type", back_populates="articles")
    couleur = relationship("Couleur", back_populates="articles")

    #paniers = relationship("Panier", back_populates="article", cascade="all,delete")
    avis = relationship("Avis", cascade="all, delete", back_populates="article")
    note = column_property(select(func.avg(Avis.note)).where(Avis.id_article == id).correlate_except(Avis).scalar_subquery())

class Panier(Base):
    __tablename__ = "panier"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    type = Column(Integer, index=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id"), index=True)
    id_article = Column(Integer, ForeignKey("article.id"), index=True)
    nb_article = Column(Integer, default=0)
    datePanier = Column(String)
    montant = column_property(select(Article.prix * nb_article).where(Article.id == id_article).correlate_except(Article).scalar_subquery())
    #utilisateur = relationship("User", back_populates="paniers")
    #article = relationship("Article", back_populates="paniers")



class Historique(Base):
    __tablename__ = "historique"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    id_utilisateur = Column(Integer, index=True)
    id_article = Column(Integer, index=True)


class Commande(Base):
    __tablename__ = "commande"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)

    prenomCommande = Column(String, index=True)
    nomCommande = Column(String, index=True)
    dateCommande = Column(String, index=True)
    adresseLivraison = Column(String, index=True)
    infosSupp = Column(String, index=True)
    nom_ville = Column(String, ForeignKey(Ville.nom_ville), index=True)
    id_user = Column(Integer, ForeignKey(User.id), index=True)
    reduction = Column(Integer, index=True)
    montant = column_property(select(func.sum(Panier.montant)).where(Panier.type == 0, Panier.id_utilisateur == id_user ).correlate_except(Panier).scalar_subquery(), deferred=True)
    ville = relationship("Ville", back_populates="commandes")
    paniers_item = Column(String, index=True)

    @hybrid_property
    def montant_reduc(self):
        print(self.reduction)
        if self.reduction == 1:
            return self.montant * 0.95
        else:
            return self.montant



