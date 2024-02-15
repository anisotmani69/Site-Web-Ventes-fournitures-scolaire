from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session

from app import schemas, models, crudUser


# ---------------------------Creation produit et ses attributs----------------------------------


def create_article(db: Session, article: schemas.ArticleCreate):
    print(verification_article(db=db, article=article))
    if (not verification_article(db=db, article=article)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saisit incorrect, cle etrangere non existante!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    db_article = models.Article(
        id_marque=article.id_marque,
        id_categorie=article.id_categorie,
        id_couleur=article.id_couleur,
        id_vendeur=article.id_vendeur,
        id_type=article.id_type,
        titre=article.titre,
        description=article.description,
        prix=article.prix,
        image=article.image,
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def verification_article(db: Session, article: schemas.ArticleCreate):
    marque_exist = db.query(models.Marque).filter(models.Marque.id == article.id_marque).first() is not None
    categorie_exist = db.query(models.Categorie).filter(models.Categorie.id == article.id_categorie).first() is not None
    type_exist = db.query(models.Type).filter(models.Type.id == article.id_type).first() is not None
    # vendeur_exist = db.query(models.Vendeur).filter(models.Vendeur.id == article.id_vendeur).first() is not None
    couleur_exist = db.query(models.Couleur).filter(models.Couleur.id == article.id_couleur).first() is not None
    print("marque:" + str(marque_exist))
    print("categorie: " + str(categorie_exist))
    print("type: " + str(type_exist))
    # print("vendeur: " + str(vendeur_exist))
    print("couleur: " + str(couleur_exist))
    return marque_exist and categorie_exist and type_exist and couleur_exist


def del_article(db: Session, id: int):
    db_article = get_article_by_id(db=db, id=id)
    if db_article is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'article n'existe pas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    db.delete(db_article)
    db.commit()
    return db_article


def update_article(db: Session, article_id: int, article: schemas.ArticleUpdate):
    db_article = get_article_by_id(db=db, id=article_id)
    if not db_article:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'article n'existe pas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    if not verification_update(db=db, article=article):
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=" Saisit incorrect, cle etrangere non existante!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    article_data = article.model_dump(exclude_unset=True)
    for key, value in article_data.items():
        setattr(db_article, key, value)

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def verification_update(db: Session, article: schemas.ArticleUpdate):
    verif = True
    if article.id_type:
        verif = verif and db.query(models.Type).filter(models.Type.id == article.id_type).first() is not None

    if article.id_categorie:
        verif = verif and db.query(models.Categorie).filter(
            models.Categorie.id == article.id_categorie).first() is not None
    if article.id_marque:
        verif = verif and db.query(models.Marque).filter(models.Marque.id == article.id_marque).first() is not None
    if article.id_couleur:
        verif = verif and db.query(models.Couleur).filter(models.Couleur.id == article.id_couleur).first() is not None
    # if article.id_vendeur:
    # verif = verif and db.query(models.Vendeur).filter(models.Vendeur.id == article.id_vendeur).first() is not None

    return verif


""" Je sais pas si c'est utile
def create_type(db: Session, type: schemas.Type):
    db_type = models.Type(
        nom=type.nom,
    )
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


def create_marque(db: Session, marque: schemas.Marque):
    db_marque = models.Type(
        nom=marque.id,
    )

    db.add(db_marque)
    db.commit()
    db.refresh(db_marque)
    return db_marque


def create_couleur(db: Session, couleur: schemas.Couleur):
    db_couleur = models.Couleur(
        nom=couleur.nom,
    )
    db.add(db_couleur)
    db.commit()
    db.refresh(db_couleur)
    return db_couleur
"""


# -----------------------------------------------filtres et recherche-------------------------------------
# -------------article-----------------


def get_article_by_id(db: Session, id: int):
    return db.query(models.Article).filter(models.Article.id == id).first()


# ----------------categorie----------------

def create_categorie(db: Session, categorie: schemas.Categorie):
    db_categorie = models.Categorie(
        nom=categorie.nom
    )
    db.add(db_categorie)
    db.commit()
    db.refresh(db_categorie)
    return db_categorie


def del_categorie(db: Session, id: int):
    db_categorie = get_categorie_by_id(db=db, id=id)
    if db_categorie is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categorie n'existe pas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    db.delete(db_categorie)
    db.commit()
    return db_categorie


def get_categorie(db: Session, nom: str):
    return db.query(models.Categorie).filter(models.Categorie.nom == nom).first()


def get_categorie_by_id(db: Session, id: int):
    return db.query(models.Categorie).filter(models.Categorie.id == id).first()


def get_all_categorie(db: Session):
    return db.query(models.Categorie).all()


# ----------------type----------------

def create_type(db: Session, type: schemas.Type):
    db_type = models.Type(
        nom=type.nom
    )
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


def del_type(db: Session, id: int):
    db_type = get_type_by_id(db=db, id=id)
    if db_type is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le type n'existe pas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    db.delete(db_type)
    db.commit()
    return db_type


def get_type(db: Session, nom: str):
    return db.query(models.Type).filter(models.Type.nom == nom).first()


def get_type_by_id(db: Session, id: int):
    return db.query(models.Type).filter(models.Type.id == id).first()


def get_all_type(db: Session):
    return db.query(models.Type).all()


# ----------------marque----------------

def create_marque(db: Session, marque: schemas.Marque):
    db_marque = models.Marque(
        nom=marque.nom
    )
    db.add(db_marque)
    db.commit()
    db.refresh(db_marque)
    return db_marque


def del_marque(db: Session, id: int):
    db_marque = get_marque_by_id(db=db, id=id)
    if db_marque is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La marque n'existe pas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    db.delete(db_marque)
    db.commit()
    return db_marque


def get_marque_by_id(db: Session, id: int):
    return db.query(models.Marque).filter(models.Marque.id == id).first()


def get_marque(db: Session, nom: str):
    return db.query(models.Marque).filter(models.Marque.nom == nom).first()


def get_all_marque(db: Session):
    return db.query(models.Marque).all()


# ----------------couleur----------------

def create_couleur(db: Session, couleur: schemas.Couleur):
    db_couleur = models.Couleur(
        nom=couleur.nom
    )
    db.add(db_couleur)
    db.commit()
    db.refresh(db_couleur)
    return db_couleur


def del_couleur(db: Session, id: int):
    db_couleur = get_couleur_by_id(db=db, id=id)
    if db_couleur is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La couleur n'existe pas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    db.delete(db_couleur)
    db.commit()
    return db_couleur


def get_couleur(db: Session, nom: str):
    return db.query(models.Couleur).filter(models.Couleur.nom == nom).first()


def get_couleur_by_id(db: Session, id: int):
    return db.query(models.Couleur).filter(models.Couleur.id == id).first()


def get_avis_by_id(db: Session, id: int):
    return db.query(models.Avis).filter(models.Avis.id == id).first()


def get_avis_by_article_id(db: Session, id_article: int):
    return db.query(models.Avis).filter(models.Avis.id_article == id_article).all()


def create_avis(db: Session, avis: schemas.Avis, user_id: int):
    db_avis = models.Avis(
        id_utilisateur=user_id,
        id_article=avis.id_article,
        note=avis.note,
        text=avis.text,
        dateAvis=avis.dateAvis
    )
    db.add(db_avis)
    db.commit()
    db.refresh(db_avis)
    return db_avis


def delete_avis(db: Session, avis_id: int, user_id: int):
    db_avis: schemas.AvisData = get_avis_by_id(db=db, id=avis_id)
    if db_avis is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'avis n'existe pas!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    if db_avis.id_utilisateur == user_id:
        db.delete(db_avis)
        db.commit()
    else:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas le droit de supprimer un avis qui n'est pas le votre!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    return db_avis


def edit_avis(db: Session, avis_id: int, user_id:int, data: schemas.Avis_modification):
    if (get_avis_by_id(db=db, id=avis_id).id_utilisateur != user_id):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'avez pas le droit de avis un avis qui n'est pas le votre!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    else:
        data_to_update = {
            "note": data.note,
            "text": data.text
        }
        db.execute(update(models.Avis).where(models.Avis.id == avis_id).values(data_to_update))
        db.commit()
        return True



def create_historique(db: Session, histo: schemas.Historique):
    db_histo = models.Historique(
        id_utilisateur=histo.id_utilisateur,
        id_article=histo.id_article,
    )
    db.add(db_histo)
    db.commit()
    db.refresh(db_histo)
    return db_histo


def get_histo(db:Session, id_utilisateur: int):
    return db.query(models.Historique).filter(models.Historique.id_utilisateur == id_utilisateur).all()



def create_commande(db: Session, commande: schemas.CreateCommande, user_id: int, user:schemas.UserData):
    liste_id =""
    for value in db.query(models.Panier).filter(models.Panier.id_utilisateur == user_id, models.Panier.type == 0).all():
        liste_id += "["+ str(value.id_article) +","+ str(value.nb_article) + "] "


    db_commande = models.Commande(
        nom_ville = commande.nom_ville,
        reduction = user.reduction,
        dateCommande = commande.dateCommande,
        prenomCommande = commande.prenomCommande,
        nomCommande = commande.nomCommande,
        id_user = user_id,
        infosSupp = commande.infosSupp,
        adresseLivraison = commande.adresseLivraison,
        paniers_item = liste_id
    )
    db.add(db_commande)
    db.commit()
    db.refresh(db_commande)
    if (user.reduction == 1):
        crudUser.change_reduction(db=db, user=user)
    return db_commande

def get_commande(db:Session, id: int):
    return db.query(models.Commande).filter(models.Commande.id == id).first()


def get_histo_commande(db:Session, id_user: int):
    return db.query(models.Commande).filter(models.Commande.id_user==id_user).order_by(models.Commande.id.desc())