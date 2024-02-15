<script>
  import { onMount } from "svelte";
  import Chargement from "../composants/Chargement.svelte";

  let total = 0;
  let nbarticle = 0;

  let produit = [];
  let articles = [];
  let vide = 0;
  let user = [];
  let commande = [];
  let loaded = false;
  let produits = [];
  
  
  


  onMount(async () => {
    setTimeout(() => {
      loaded = true;
    }, 100);
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);
    user = JSON.parse(localStorage.getItem("user"));

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion...",
      );
      window.location.href("../connexion");
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/commande?id_user=${user.id}`,
        {
          method: "GET",
          mode: "cors",
          headers: {
            Accept: "application/json",
          },
        },
      );

      if (response.ok) {
        const cartData = await response.json();
        cartData.reverse();
         produits = cartData;
        

        const allArticlesByProduct = produits.reduce(
          async (accPromise, produit) => {
            const acc = await accPromise;

            let regex = /\[.*?\]/g;
            let tableauxEnChaine = produit.paniers_item.match(regex);
           
            if (tableauxEnChaine) {
              let tableaux = tableauxEnChaine.map((tableau) =>
                JSON.parse(tableau),
                
              );
              tableaux.reverse();

              const productArticles = await tableaux.reduce(
                async (accPromise, product) => {
                  const acc = await accPromise;

                  const searchResponse = await fetch(
                    `http://127.0.0.1:8000/search?id=${product[0]}`,
                    {
                      method: "GET",
                      mode: "cors",
                      headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                      },
                    },
                  );

                  if (searchResponse.ok) {
                    const productDetails = await searchResponse.json();
                    console.log(productDetails[0].image);

                    for (let i = 0; i < productDetails.length; i++) {
                      const imageResponse = await fetch(
                        `http://127.0.0.1:8000/image?filename=${productDetails[0].image}`,
                        {
                          method: "GET",
                          mode: "cors",
                          headers: {
                            Accept: "application/json",
                          },
                        },
                      );

                      if (imageResponse.ok) {
                        const imageData = await imageResponse.blob();
                        productDetails[i].imageUrl =
                          URL.createObjectURL(imageData);
                      } else {
                        console.error(
                          `Erreur lors de la récupération de l'image pour le produit ${produit[i].titre}:`,
                          imageResponse.status,
                        );
                      }
                    }

                    productDetails.nb_article = product[1];

                    productDetails.product = produit;

                    return acc.concat([productDetails]);
                  } else {
                    console.error(
                      "Erreur lors de la recherche du produit :",
                      searchResponse.statusText,
                    );
                    return acc;
                  }
                },
                Promise.resolve([]),
              );
              acc[produit.id] = productArticles;
              console.log(productArticles);

              return acc;
            } else {
              console.warn(
                "Aucun tableau trouvé dans le panier du produit :",
                produit,
              );
              return acc;
            }
          },
          Promise.resolve({}),
        );

        const articlesByProduct = await allArticlesByProduct;
        commande = articlesByProduct;
      
        

        console.log("Articles liés à leur produit correspondant :", commande);
      }
    } catch (e) {
      console.error("Erreur lors de la requête de récupération du panier :", e);
    }
  });

  
  async function facture(numCommande) {
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion...",
      );
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/facture?id=${numCommande}`,
        {
          method: "GET",
          mode: "cors",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
          },
        },
      );

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      window.open(url);
    } catch (e) {
      console.error("Erreur lors de la requête de modification au panier :", e);
    }
  }

  console.log("total", { nbarticle });
</script>

<body>
  {#if !loaded}
    <Chargement />
  {:else}
  <main>
    {#if !produit}
      <div class="panier-vide">
        <div>
          <p>Vous n'avez pas de cartable.</p>
        </div>
        <div>
          <button on:click={() => (window.location.href = "../pageproduits")}
            >Retournez à la boutique</button
          >
        </div>
        <div>
          <img src="src/img/Paniervide.jpg" alt="Image vide" class="panier" />
        </div>
      </div>
    {:else}
      <div class="container">
        <div class="item21">
          <p>Mon historique de commande</p>
        </div>

        {#each Object.entries(commande) as [key, product]}
          <div class="product-item">
            <div class="containers">
              <div class="commande">
                <div class="commande1">
                  Commande effectué le
                  <p>{product[0].product.dateCommande}</p>
                </div>
                <div class="commande2">
                  Livraison chez
                  <p>
                    {product[0].product.nomCommande}
                    {product[0].product.prenomCommande}
                  </p>
                </div>
                <div class="commande3">
                  Adresse de livraison
                  <p>{product[0].product.adresseLivraison}</p>
                </div>
                <div class="facture">
                  <button
                    class="ajout"
                    on:click={() => facture(product[0].product.id)}
                    >Facture</button
                  >
                </div>
              </div>

              <div class="produit">
                <hr id="trait" />
                <div class="prod">
                  {#each product as article}
                    <div class="article">
                      <img
                        src={article[0].imageUrl}
                        alt="produit"
                        class="img"
                      />
                      <div class="infoF">
                        <div class="item1"><p>{article[0].titre}</p></div>

                        <div class="item2"><p>Qté:{article.nb_article}</p></div>
                        <div class="item3">
                          <p>{article.nb_article * article[0].prix}€</p>
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </main>
  {/if}
</body>

<style>
  body {
    background-color: #ffeedd;
    font: 12px Arial;
    margin: 0;
  }

  main {
    max-width: 800px;
    margin: 20px auto;
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .container {
    margin-top: 20px;
  }

  .product-item {
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 20px;
    overflow: hidden;
  }

  .commande {
    padding: 15px;
    display: flex;
    justify-content: space-between;
    background-color: #ffeedd;
    border-bottom: 1px solid #ddd;
  }

  .commande1,
  .commande2,
  .commande3 {
    flex: 1;
    text-align: left;
  }

  .facture {
    flex: 0;
  }

  .produit {
    padding: 15px;
  }

  .prod {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin-top: 20px;
  }

  .article {
    display: flex;
    flex-direction: column;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
  }

  .img {
    width: 100%;
    height: auto;
    border-bottom: 1px solid #ddd;
    flex: 8;
  }

  .infoF {
    padding: 10px;
    text-align: center;
    flex: 2;
  }

  .item1 {
    font-weight: bold;
    margin-bottom: 5px;
  }

  .item2,
  .item3 {
    color: #007185;
    font-weight: bold;
  }

  .panier-vide {
    margin: 50px auto;
    text-align: center;
  }

  .panier-vide p {
    font-weight: bold;
    font-size: 1.2em;
    margin-bottom: 20px;
  }

  .panier-vide button {
    background-color: #f0c14b;
    border: 1px solid #a88734;
    border-radius: 3px;
    height: 30px;
    width: 150px;
    font-weight: bold;
    cursor: pointer;
  }

  .panier-vide button:hover {
    background-color: #d89f32;
  }
</style>
