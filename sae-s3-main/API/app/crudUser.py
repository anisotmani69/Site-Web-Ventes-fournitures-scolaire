from datetime import timedelta, datetime
from typing import Union, Annotated
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import update

from sqlalchemy.orm import Session

from app import schemas, models
from app.get_db import get_db

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY_JWT")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SEL = os.getenv("SEL")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_username(db: Session, nom_utilisateur: str):
    return db.query(models.User).filter(models.User.nom_utilisateur == nom_utilisateur).first()


def get_vendeur_by_username(db: Session, nom_utilisateur: str):
    return db.query(models.Vendeur).filter(models.Vendeur.nom_utilisateur == nom_utilisateur).first()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password + SEL, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password + SEL)


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def verify_format_email(email: str):
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        print(str(e))
        return False


def create_user(db: Session, user: schemas.UserCreate):
    if not verify_format_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email n'est pas dans un format valide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = get_password_hash(user.mot_de_passe)
    db_user = models.User(
        nom_utilisateur=user.nom_utilisateur,
        mdp_hash=hashed_password,
        nom="",
        prenom="",
        email=user.email,
        adresse="",
        ville="",
        telephone="",
        
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, data: schemas.User, user_id: int):
    data = data.dict(exclude_unset=True)
    # data_to_update = {
    #     "nom_utilisateur": data.nom_utilisateur,
    #     "nom": data.nom,
    #     "prenom": data.prenom,
    #     "email": data.email,
    #     "adresse": data.adresse,
    #     "ville": data.ville,
    #     "telephone": data.telephone
    # }
    db.execute(update(models.User).where(models.User.id == user_id).values(data))
    db.commit()
    return True


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        user = get_vendeur_by_username(db, username)
        if not user:
            return False
        if not verify_password(password, user.mdp_hash):
            return False
        return user
    if not verify_password(password, user.mdp_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db=db, nom_utilisateur=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def delete_user(db: Session, id: int):
    db_user = get_user_by_id(db=db, id=id)
    db.delete(db_user)
    db.commit()
    return db_user


def change_password(db: Session, password: str, user: schemas.UserInDb):
    password_hash = get_password_hash(password)
    data = {"mdp_hash": password_hash}
    db.execute(update(models.User).where(models.User.email == user.email).values(data))
    db.commit()

def change_reduction(db: Session, user: schemas.User):
    nv_reduc = 0
    if user.reduction == 0:
        nv_reduc = 1
    elif user.reduction == 1:
        nv_reduc = 2
    data = {"reduction": nv_reduc}
    db.execute(update(models.User).where(models.User.email == user.email).values(data))
    db.commit()

# ==========================================partie vendeur===================================


def create_vendeur(db: Session, vendeur: schemas.VendeurCreate):
    user = get_user_by_username(db=db, nom_utilisateur=vendeur.nom_utilisateur)
    print(user)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom d'utilisateur existe déjà",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_format_email(vendeur.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email n'est pas dans un format valide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = get_password_hash(vendeur.mot_de_passe)
    db_vendeur = models.Vendeur(
        nom_utilisateur=vendeur.nom_utilisateur,
        mdp_hash=hashed_password,
        nom_vendeur="",
        email=vendeur.email,
        adresse="",
        ville="",
        telephone="",
    )
    db.add(db_vendeur)
    db.commit()
    db.refresh(db_vendeur)
    return db_vendeur
