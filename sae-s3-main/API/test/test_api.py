from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/signup",
        json={
            "nom_utilisateur": "testuser",
            "nom": "test",
            "prenom": "user",
            "email": "testuser@gmail.com",
            "adresse": "test address",
            "ville": "test city",
            "telephone": "0123456789",
            "mot_de_passe": "testpassword",
        },
    )
    assert response.status_code == 200
    assert response.json()["nom_utilisateur"] == "testuser"
    assert response.json()["email"] == "testuser@gmail.com"


def test_get_token_user():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_read_users_me():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response.json()["access_token"]

    response = client.get(
        "/user/me/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["nom_utilisateur"] == "testuser"
    assert response.json()["email"] == "testuser@gmail.com"

# def test_get_cart():
#     response = client.post(
#         "/token",
#         data={
#             "username": "testuser",
#             "password": "testpassword",
#         },
#     )
#     token = response.json()["access_token"]
#
#     response = client.get(
#         "/panier",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#
#     assert response.status_code == 200
#     assert response.json()
#
#
# def test_add_product_to_cart():
#     product_id = 1
#     response = client.post(
#         "/panier",
#         json={"product_id": product_id}
#     )
#
#     assert response.status_code == 401
#
#     response = client.post(
#         "/token",
#         data={
#             "username": "testuser",
#             "password": "testpassword",
#         },
#     )
#     token = response.json()["access_token"]
#
#     response = client.post(
#         "/panier",
#         json={"product_id": product_id},
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#
#     assert response.json()
#     assert response.status_code == 422
#     assert "id" in response.json()
#


def test_create_attribut():


    print("test")
    response = client.post(
        "/categorie",
        json={
            "nom": "oui1",
        }
    )
    assert response.status_code == 200
    print(response.json()["id"])
    response = client.post(
        "/type",
        json={
            "nom": "oui1",
        }
    )
    assert response.status_code == 200
    print(response.json()["id"])
    response = client.post(
        "/marque",
        json={
            "nom": "oui1",
        }
    )
    assert response.status_code == 200
    print(response.json()["id"])
    response = client.post(
        "/couleur",
        json={
            "nom": "oui1",
        }
    )
    print(response.json()["id"])
    assert response.status_code == 200


def test_create_article():

    print("test")
    response = client.post(
        "/createarticle",
        json={
            "id_marque": 1,
            "id_categorie": 1,
            "id_vendeur": 1,
            "id_type": 1,
            "id_couleur": 1,
            "titre": "oui",
            "description": "strzdweing",
            "prix": 0,
            "image": "stringaaaaaaaaa"
        }
    )
    print(response.status_code)
    assert response.status_code == 200
    assert response.json()["marque"]["id"] == 1
    assert response.json()["titre"] == "oui"

def test_delete_user_me():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = response.json()["access_token"]

    response = client.delete(
        "/user/me/",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )
    print(response.json()["id"])
    assert response.status_code == 200
    assert response.json()["nom_utilisateur"] == "testuser"
    assert response.json()["email"] == "testuser@gmail.com"

def test_update_article():
    response = client.get(
        "/search",
        params={
            "titre__like": "oui"
        }
    )

    id_article = response.json()[0]["id"]

    response = client.patch(
        "/article",
        params={
            "article_id": id_article
        },
        json={
            "description": "ouioui"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == id_article
    assert response.json()["description"] == "ouioui"


def test_search():
    response = client.get(
        "/search",
        params={
            "titre__like": "oui"
        }

    )

    assert response.status_code == 200


def test_delete_article():
    response = client.get(
        "/search",
        params={
            "titre__like": "oui"
        }
    )

    id_article = response.json()[0]["id"]
    response = client.delete(
        "/article",
        params={
            "article_id": id_article
        }
    )
    assert response.status_code == 200
    assert response.json()["marque"]["id"] == 1
    assert response.json()["titre"] == "oui"



def test_delete_attribut():
    response = client.get(
        "/type",

    )
    print(response.json()[0]["id"])

    response = client.delete(
        "/categorie",
        params={
            "id":1,
        }
    )
    assert response.status_code == 200
    response = client.delete(
        "/type",
        params={
            "id": 1,
        }
    )

    assert response.status_code == 200
    response = client.delete(
        "/marque",
        params={
            "id": 1,
        }
    )
    print(response.json()["id"])
    assert response.status_code == 200
    response = client.delete(
        "/couleur",
        params={
            "id": 1,
        }
    )
    assert response.status_code == 200
