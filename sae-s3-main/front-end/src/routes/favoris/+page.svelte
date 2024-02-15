<script>
  import Item from "../composants/Item_favoris.svelte";
  import { onMount } from "svelte";
  import Chargement from "../composants/Chargement.svelte";

  let prod = {
    image: "src/img/Rectangle149.png",
    titre: "image de stylo",
    prix: 12,
    id: 1,
  };

  let articles = [];
  let produits = [];
  let vide = false;
  let loaded = false;

  onMount(async () => {
    setTimeout(() => {
      loaded = true;
    }, 100);
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion..."
      );
      window.location.href("../connexion");
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/panier?type_id=3", {
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
        produits = cartData;
        console.log("produits", produits);
        if (produits.length === 0) {
          console.log("le panier est vide");
          vide = true;
        }

        const allProducts = produits.reduce(async (accPromise, product) => {
          const acc = await accPromise;
          const searchResponse = await fetch(
            `http://127.0.0.1:8000/search?id=${product.id_article}`,
            {
              method: "GET",
              mode: "cors",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            }
          );

          if (searchResponse.ok) {
            const productDetails = await searchResponse.json();
            return acc.concat([productDetails]);
          } else {
            console.error(
              "Erreur lors de la recherche du produit :",
              searchResponse.statusText
            );
            return acc;
          }
        }, Promise.resolve([]));

        articles = await allProducts;
        console.log("Articles récupérés :", articles);

        for (let i = 0; i < articles.length; i++) {
          const imageResponse = await fetch(
            `http://127.0.0.1:8000/image?filename=${articles[i][0].image}`,
            {
              method: "GET",
              mode: "cors",
              headers: {
                Accept: "application/json",
              },
            }
          );

          if (imageResponse.ok) {
            const imageData = await imageResponse.blob();
            articles[i][0].imageUrl = URL.createObjectURL(imageData);
            console.log(articles);
          } else {
            console.error(
              `Erreur lors de la récupération de l'image pour le produit ${articles[i].titre}:`,
              imageResponse.status
            );
          }
        }
      } else {
        console.error(
          "Erreur lors de la récupération du panier :",
          response.statusText
        );
      }
    } catch (e) {
      console.error("Erreur lors de la requête de récupération du panier :", e);
    }
    console.log(articles);
  });
</script>

<main>
  {#if !loaded}
    <Chargement />
  {:else}
    <body>
      <div class="empty"></div>
      <div class="center">
        {#if articles.length > 0}
          <div id="favTitle">Mes favoris</div>
          {#each articles as article}
            <Item
              image={article[0].imageUrl}
              titre={article[0].titre}
              prix={article[0].prix}
              id={article[0].id}
            />
          {/each}
        {:else}
          <div class="panier-vide">
            <div>
              <p>Vous n'avez pas de favoris.</p>
            </div>
            <div>
              <button
                on:click={() => (window.location.href = "../pageproduits")}
                >Retournez à la boutique</button
              >
            </div>
            <div>
              <img src="src/img/Paniervide.jpg" alt="Image vide" />
            </div>
          </div>
        {/if}
      </div>
      <div class="empty"></div>
    </body>
  {/if}
</main>

<style>
  main {
    background-color: #faf5f0;
    min-height: 100vh;
    padding-top: 17px;
  }
  /*
    body{
    display : grid;
    grid-template-columns: 1fr 4fr 1fr;
    }
    */
  #favTitle {
    border-radius: 10px;
    background-color: #ffeedd;
    font-size: 40px;
    color: #5bc3eb99;
    padding: 10px;
    display: flex;
    justify-content: center;
    font-family: Arial, Helvetica, sans-serif;
  }

  .fav_produit {
    display: grid;
    grid-template-columns: 2fr 5fr 1fr;
    padding: 10px;
    margin: 15px;
    background-color: #ffeedd;
    border-radius: 10px;
    height: 100px;
  }

  .etoile {
    max-width: 60%;
    max-height: 60%;
  }

  .panier-vide button {
    background-color: orange;
    border: none;
    margin-left: 100px;
    border-radius: 6px;
    height: 30px;
    width: 150px;
    opacity: 1;
    transition: opacity 0.3s ease;
    cursor: pointer;
  }

  .panier-vide button:hover {
    opacity: 0.8;
  }

  .panier-vide {
    margin-top: 50px;
    margin-right: 50px;
    margin-left: 500px;
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: 20px;
    justify-content: center;
    align-items: center;
  }

  .panier-vide img {
    width: 400px;
    height: 400px;
    border-radius: 10px;
  }

  .panier-vide p {
    font-weight: bold;
    font-size: 1.7em;
    margin-left: 70px;
  }
</style>
