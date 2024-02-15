from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session

from app import schemas, models


def get_article(db: Session, id_article: int, id_utilisateur: int):
    return db.query(models.Panier).filter(models.Panier.id_article == id_article,
                                          models.Panier.id_utilisateur == id_utilisateur).first()


def get_article_type(db: Session, id_article: int, type_id:int,  id_utilisateur: int):
    return db.query(models.Panier).filter(models.Panier.id_article == id_article,
                                          models.Panier.id_utilisateur == id_utilisateur, models.Panier.type == type_id).first()


def get_cart(db: Session, type_id: int, user_id: int):
    return db.query(models.Panier).filter(models.Panier.id_utilisateur == user_id, models.Panier.type == type_id).all()


def add_cart(db: Session, article: schemas.Panier, user: int):
    # 3 est égal aux favoris
    if article.type == 3:
        article.nb_article = 0
    article_temp: schemas.PanierData = get_article(db=db, id_article=article.id_article, id_utilisateur=user)
    if article_temp is None or article_temp.type != article_temp:
        db_cart = models.Panier(
            type=article.type,
            id_utilisateur=user,
            id_article=article.id_article,
            nb_article=article.nb_article,
            datePanier=article.datePanier
        )
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        return db_cart
    else:
        return put_cart(db=db, id_article=article.id_article, nb_article=article_temp.nb_article + article.nb_article,
                        user_id=user)


def remove_cart(db: Session, article_id: int, type_id: int, current_user: schemas.UserData):
    db_cart = get_article_type(db=db, id_article=article_id, type_id=type_id, id_utilisateur=current_user.id)
    if db_cart is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le produit n'est pas dans le panier!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    db.delete(db_cart)
    db.commit()
    return db_cart


def put_cart(db: Session, id_article: int, nb_article: int, user_id: int):
    db_cart = get_article(db=db, id_article=id_article, id_utilisateur=user_id)
    if db_cart is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le produit n'est pas dans le panier!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    data = {"nb_article": nb_article}
    db.execute(update(models.Panier).where(models.Panier.id_utilisateur == user_id,
                                           models.Panier.id_article == id_article).values(data))
    db.commit()
    return db_cart

