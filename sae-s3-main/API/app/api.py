from datetime import timedelta, datetime
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from pathlib import Path
from app import crudImage

from fastapi_filter import FilterDepends, with_prefix

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.pdfgenerator import render_template

from app import models, schemas, crudUser, crudArticle, crudPanier
from app.get_db import get_db
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    description="API pour le projet de SAE",
    title="API SAE",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

factureId = 1


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/signup", response_model=schemas.UserData, tags=["users"])
async def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    try:
        user: schemas.UserInDb = crudUser.create_user(db=db, user=user)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email ou le nom d'utilisateur éxiste déjà!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/signup/vendeur", response_model=schemas.VendeurData, tags=["vendeur"])
async def create_user(
        vendeur: schemas.VendeurCreate,
        db: Session = Depends(get_db)
):
    try:
        vendeur: schemas.VendeurData = crudUser.create_vendeur(db=db, vendeur=vendeur)
        return vendeur
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email ou le nom d'utilisateur éxiste déjà!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/token", response_model=schemas.Token, tags=["users"])
# TODO : add a refresh token
async def get_token_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)):
    user = crudUser.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Le nom d'utilisateur ou le mot de passe est incorrect!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(crudUser.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = crudUser.create_access_token(
        data={"sub": user.nom_utilisateur}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user/me/", response_model=schemas.UserData, tags=["users"])
async def read_users_me(
        current_user: schemas.UserData = Depends(crudUser.get_current_user)
):
    return current_user


@app.put("/user/me", response_model=bool, tags=["users"])
async def update_user(
        data: schemas.User,
        user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db)
):
    return crudUser.update_user(db=db, data=data, user_id=user.id)


@app.delete("/user/me/", response_model=schemas.UserData, tags=["users"])
async def delete_user_me(
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db)
):
    return crudUser.delete_user(db=db, id=current_user.id)


@app.post("/createarticle", response_model=schemas.ArticleData, tags=["Produit"])
async def createarticle(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    try:
        article: schemas.ArticleData = crudArticle.create_article(db=db, article=article)
        return article
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="produit existe déjà!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/panier", response_model=list[schemas.Panier], tags=["Panier"])
async def get_cart(
        type_id: int,
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db),
):
    return crudPanier.get_cart(db=db, type_id=type_id, user_id=current_user.id)


@app.post("/panier", response_model=schemas.Panier, tags=["Panier"])
async def add_cart(
        article: schemas.Panier,
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db),
):
    return crudPanier.add_cart(db=db, article=article, user=current_user.id)


@app.put("/panier", response_model=schemas.Panier, tags=["Panier"])
async def put_cart(
        id_article: int,
        nb_article: int,
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db),
):
    return crudPanier.put_cart(db=db, id_article=id_article, nb_article=nb_article, user_id=current_user.id)


@app.delete("/panier", response_model=schemas.Panier, tags=["Panier"])
async def remove_cart(
        article_id: int,
        type_id: int,
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db),
):
    return crudPanier.remove_cart(db=db, article_id=article_id, type_id=type_id, current_user=current_user)


@app.get("/search", response_model=list[schemas.ArticleData], tags=["Produit"])
async def search_article(
        filters: schemas.ArticleFilter = FilterDepends(schemas.ArticleFilter, by_alias=True),
        db: Session = Depends(get_db),
):
    query = select(models.Article)

    query = filters.filter(query)
    query = filters.sort(query)
    result = db.execute(query)
    result = result.scalars().all()
    # print(result[0].marque.nom)
    return result


@app.patch("/article", response_model=schemas.ArticleData, tags=["Produit"])
async def update_article(article_id: int, article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    return crudArticle.update_article(db=db, article_id=article_id, article=article)


@app.delete("/article", response_model=schemas.ArticleData, tags=["Produit"])
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    return crudArticle.del_article(db=db, id=article_id)


@app.get("/article", response_model=schemas.ArticleData, tags=["Produit"])
async def get_article(article_id: int, db: Session = Depends(get_db)):
    return crudArticle.get_article_by_id(db=db, id=article_id)


@app.post("/categorie", response_model=schemas.CategorieData, tags=["Attribut"])
async def create_categorie(categorie: schemas.Categorie, db: Session = Depends(get_db)):
    return crudArticle.create_categorie(db=db, categorie=categorie)


@app.delete("/categorie", response_model=schemas.CategorieData, tags=["Attribut"])
async def delete_categorie(id: int, db: Session = Depends(get_db)):
    return crudArticle.del_categorie(db=db, id=id)


@app.get("/categorie", response_model=list[schemas.CategorieData], tags=["Attribut"])
async def get_all_categorie(db: Session = Depends(get_db)):
    return crudArticle.get_all_categorie(db=db)


@app.post("/type", response_model=schemas.TypeData, tags=["Attribut"])
async def create_type(type: schemas.Type, db: Session = Depends(get_db)):
    return crudArticle.create_type(db=db, type=type)


@app.get("/type", response_model=list[schemas.TypeData], tags=["Attribut"])
async def get_all_type(db: Session = Depends(get_db)):
    return crudArticle.get_all_type(db=db)


@app.delete("/type", response_model=schemas.CategorieData, tags=["Attribut"])
async def delete_type(id: int, db: Session = Depends(get_db)):
    return crudArticle.del_type(db=db, id=id)


@app.post("/marque", response_model=schemas.MarqueData, tags=["Attribut"])
async def create_marque(marque: schemas.Marque, db: Session = Depends(get_db)):
    return crudArticle.create_marque(db=db, marque=marque)


@app.delete("/marque", response_model=schemas.CategorieData, tags=["Attribut"])
async def delete_marque(id: int, db: Session = Depends(get_db)):
    return crudArticle.del_marque(db=db, id=id)


@app.post("/couleur", response_model=schemas.CouleurData, tags=["Attribut"])
async def create_couleur(couleur: schemas.Couleur, db: Session = Depends(get_db)):
    return crudArticle.create_couleur(db=db, couleur=couleur)


@app.delete("/couleur", response_model=schemas.CategorieData, tags=["Attribut"])
async def delete_couleur(id: int, db: Session = Depends(get_db)):
    return crudArticle.del_couleur(db=db, id=id)


# @app.get("/avis/all", response_model=list[schemas.AvisData], tags=["Avis"])
# async def all_products(
#         article_id: id,
#         db: Session = Depends(get_db)
# ):
#     return crudArticle.get_avis_by_article_id(db=db, id_article=article_id)


@app.post("/avis", response_model=schemas.AvisData, tags=['Avis'])
async def create_Avis(
        avis: schemas.Avis,
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db)
):
    return crudArticle.create_avis(db=db, avis=avis, user_id=current_user.id)


@app.put("/avis", response_model=bool, tags=['Avis'])
async def edit_Avis(
        data: schemas.Avis_modification,
        avis_id: int,
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db)
):
    return crudArticle.edit_avis(db=db, avis_id=avis_id, user_id=current_user.id, data=data)


@app.delete("/avis", response_model=schemas.AvisData, tags=['Avis'])
async def delete_Avis(
        avis_id: int,
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db)
):
    return crudArticle.delete_avis(db=db, avis_id=avis_id, user_id=current_user.id)


@app.get("/facture", tags=['Facture'])
async def get_pdf(
    id: int,
    current_user: schemas.UserData = Depends(crudUser.get_current_user),
    db: Session = Depends(get_db)
):
    global factureId
    headers = {
        "Content-Disposition": repr("Facture; filename=facture{factureId}.pdf")
    }

    commande: schemas.Commande = crudArticle.get_commande(db=db, id=id)
    if commande.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous ne pouvez pas récupérer une factre qui n'est pas la votre",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(commande)
    articles_list = []
    soustotal = 0

    tmp = commande.paniers_item.split()

    for i in tmp:
        i = i.split(",")
        art = i[0][1:]
        nb = int(i[1][:1])
        
        article: schemas.Article = crudArticle.get_article_by_id(db, art)
        articles_list.append({
            "nom": article.titre,
            "quantite": nb,
            "prix": article.prix,
            "total": nb * article.prix,
        })
        soustotal += nb * article.prix

    impots = soustotal * 1.15 - soustotal
    total = soustotal + impots

    impots = round(impots, 2)
    total = round(total, 2)

    context = {
        "date": datetime.today().strftime("%Y-%m-%d"),
        "nofacture": factureId,
        "prenom": commande.prenomCommande,
        "nom": commande.nomCommande,
        "telephone": current_user.telephone,
        "adresse": commande.adresseLivraison,
        "ville": commande.ville,
        "infos_supp": commande.infosSupp,
        "email": current_user.email,
        "articles": articles_list,
        "sousTotal": soustotal,
        "impots": impots,
        "total": total
    }

    html_content = render_template("facture.html", context, factureId)
    response = FileResponse(f"public/factures/{html_content}", media_type="application/pdf", headers=headers)

    factureId += 1

    return response


@app.post("/histo", response_model=schemas.Historique, tags=['User'])
async def create_historique(
        historique: schemas.Historique,
        db: Session = Depends(get_db)

):
    return crudArticle.create_historique(db=db, histo=historique)


@app.get("/histo", response_model=list[schemas.Historique], tags=['User'])
async def get_historique(
        id_user: int,
        db: Session = Depends(get_db)
):
    return crudArticle.get_histo(db=db, id_utilisateur=id_user)

@app.post("/commande", response_model=schemas.Commande, tags=['Panier'])
async def create_commande(
        commande: schemas.CreateCommande,
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db),

):
    return crudArticle.create_commande(db=db, commande=commande, user_id=current_user.id, user=current_user)



@app.get("/commande", response_model=list[schemas.Commande], tags=['Panier'])
async def get_histo_commande(
        id_user:int,
        db: Session = Depends(get_db)
):
    return crudArticle.get_histo_commande(db=db, id_user=id_user)

image_folder = Path("./public/img")

@app.post("/image", tags=['image'])
async def upload_photo(file: UploadFile):
    image_folder.mkdir(parents=True, exist_ok=True)

    file_extension = file.filename.split(".")[-1]

    if file_extension != "png":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seulement les fichier png sont acceptés",
            headers={"WWW-Authenticate": "Bearer"},
        )

    file_path = image_folder / f"{file.filename}"

    if file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom du fichier existe déjà",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with file_path.open("wb") as image:
        image.write(file.file.read())

    return {"message": "Succes upload"}

@app.get("/image", tags=['image'])
async def get_photo(filename: str):
    filename_with_extension = f"{filename}.png"
    file_path = image_folder / filename_with_extension

    print(file_path)

    if file_path.exists():
        return FileResponse(path=str(file_path), media_type="image/png")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Le fichier n'a pas pu etre trouvé",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/user/reduction", tags=["User"])
async def change_reduction(
        current_user: schemas.UserData = Depends(crudUser.get_current_user),
        db: Session = Depends(get_db)

):
    if current_user.reduction == 0:
        return crudUser.change_reduction(db=db, user=current_user)