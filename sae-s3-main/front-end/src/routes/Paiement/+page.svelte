<script>
    import { onMount } from "svelte";
    import Chargement from "../composants/Chargement.svelte";
	import Item from "../composants/Item_avis.svelte";
    let data;
    let articles = [];
    let cartable = [];
    let trousse = [];
    let type = 0;
    let typeT = 6;
    let typeC = 5;
    let loaded = false;

    onMount(async () => {

        setTimeout(() => {
        loaded = true;
      }, 100);

        data = JSON.parse(localStorage.getItem("infosLivraison"));
        
        console.log("Articles récupérés :", articles);  
    });

    function getDate(){
        var dateActuelle = new Date();

        var jour = dateActuelle.getDate();
        var mois = dateActuelle.getMonth() + 1; 
        var annee = dateActuelle.getFullYear();

        var jourFormat = (jour < 10) ? '0' + jour : jour;
        var moisFormat = (mois < 10) ? '0' + mois : mois;

        var dateFormatee = jourFormat + '/' + moisFormat + '/' + annee;
        console.log("date formatee : " + dateFormatee);
        return dateFormatee;

    }

    function getToken(){
        const token = window.localStorage.getItem("token");
        console.log("Token:", token);

        if (!token) {
            console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
            window.location.href = "../connexion";
        }
        return token;
    }

    
  async function passeCommande(){
    const token = getToken();
     
     data.dateCommande = getDate();
     console.log(data)
     const responses = await fetch("http://127.0.0.1:8000/panier?type_id=5", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (responses.ok) {
            const cartDatas = await responses.json();
             cartable = cartDatas;
             console.log("trousse", cartable);
             for(const article of cartable){
                const datass = {
                    id_article: article.id_article,
                    type: 0,
                    nb_article: article.nb_article,
                    datePanier : "14/01/2024",
                };

                const responsea = await fetch("http://127.0.0.1:8000/panier", {
                    method: "POST",
                    mode: "cors",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify(datass),
                });
                if (responsea.ok) {
                    const resulta = await responsea.json();
                    console.log("Produit ajouté au panier :", resulta);
                    deleteToCart(article.id_article, typeC);
                    
                    }
                   
                    }
            }

            const responsess = await fetch("http://127.0.0.1:8000/panier?type_id=6", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (responsess.ok) {
            const cartDatass = await responsess.json();
             trousse = cartDatass;
             console.log("trousse", trousse);
             for(const article of trousse){
                const datas = {
                    id_article: article.id_article,
                    type: 0,
                    nb_article: article.nb_article,
                    datePanier : "14/01/2024",
                };
            

                const responseb = await fetch("http://127.0.0.1:8000/panier", {
                    method: "POST",
                    mode: "cors",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify(datas),
                });
                if (responseb.ok) {
                    const resultb = await responseb.json();
                    console.log("Produit ajouté au panier :", resultb);
                    deleteToCart(article.id_article, typeT);
                    
                    }

             }
                const response = await fetch("http://127.0.0.1:8000/commande", {
                    method: "POST",
                    mode: "cors",
                    headers: {
                        Accept: "application/json",
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log("Commande passee :", result);
                    console.log("type", articles)
                    articles = await getPanier();
                    for(const article of articles){
                    deleteToCart(article[0].id, type);
                    }
                   
                } else {
                    console.error("Erreur lors de la creation de la commande:", response.statusText);
                }    
               
           window.location.href="../historique";
 }
}

 async function getPanier(){
    const token = getToken();
    try {
        const response = await fetch("http://127.0.0.1:8000/panier?type_id=0", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.ok) {
            const cartData = await response.json();
            let produit = cartData;
            console.log("produits", produit)
            if(produit.length === 0){
              console.log("le panier est vide");
            }

              const allProducts = produit.reduce(async (accPromise, product) => {
                  const acc = await accPromise;
                  const searchResponse = await fetch(`http://127.0.0.1:8000/search?id=${product.id_article}`, {
                      method: "GET",
                      mode: "cors",
                      headers: {
                          Accept: "application/json",
                          "Content-Type": "application/json",
                          Authorization: `Bearer ${token}`,
                      },
                  });
        
                  if (searchResponse.ok) {
                      const productDetails = await searchResponse.json();
                      productDetails.nb_article = product.nb_article;
                      return acc.concat([productDetails]);
                  } else {
                      console.error("Erreur lors de la recherche du produit :", searchResponse.statusText);
                      return acc; 
                  }
              }, Promise.resolve([]));

              const res = await allProducts;
                  
              return res;

        } else {
            console.error("Erreur lors de la récupération du panier :", response.statusText);
        }
    } catch (e) {
        console.error("Erreur lors de la requête de récupération du panier :", e);
    }

 }

 async function deleteToCart(product, type) {
      const token = getToken();

    try {
      console.log('id', product);
      const response = await fetch(`http://127.0.0.1:8000/panier?article_id=${product}&type_id=${type}`, {
        method: "DELETE",
        mode: "cors",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Produit supprime du panier :", result);
      } else {
        console.error("Erreur lors de la suppression de l'article :", response.statusText);
      }
    } catch (e) {
      console.error("Erreur lors de la requête d'ajout au panier :", e);
    }
  }

function retour(){
    window.location.href = "../Livraison";
}
</script>

<body>
    {#if !loaded}
    <Chargement />
  {:else}
    
    <h1>Paiement</h1>
    <main>
        
        <div id="infos">
            <h2>Informations bancaires</h2>
            <label for="">Numero de carte</label>
            <input type="text" id="numcarte">
            <label for="">Date d'expiration</label>
            <input type="text" id="dateExpi">
            <label for="">Cryptogramme visuel</label>
            <input type="text" id="crypto">
            
        </div>
        <div class="buttons">
            <button id="annuler" on:click={retour}>Retour</button>
        <button id="valider" on:click={passeCommande}>Valider le paiement</button>
        </div>
    </main>
{/if}
</body>

<style>
    .buttons {
        margin-top: 30px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-around;
    }
    h1 {
        margin: 30px;
    }
    body {
        display: grid;
        background-color: #faf5f0;
        margin: 0px;
        justify-content: center;
    }

    main {
        margin-top: 10px;
        background-color: #faf5f0;
        margin-bottom: 40px;
        border: 2px solid black;
        border-radius: 12px;
        width: 600px;
        padding: 15px;
    }

    #valider {
    background-color:orange;
    border: 2px solid orange;
    border-radius:15px;
    font-size: 17px;
    transition: background-color 0.3s;
}

#annuler {
    border: 2px solid orange;
    background-color: #FAF5F0;
    color: orange;
    border-radius: 15px;
    font-size: 17px;
}
    input {
    border-radius: 10px;
    height: 30px;
    padding-left: 5px;
    margin: 5px;
    margin-top: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
}

    label {
    font-size: 14px;;
}

#annuler:hover {
    border: 3px solid orange;
}

#valider:hover {
    background-color: #feb52f;
}

button {
    width: 242px;
    height: 45px;
}
</style>