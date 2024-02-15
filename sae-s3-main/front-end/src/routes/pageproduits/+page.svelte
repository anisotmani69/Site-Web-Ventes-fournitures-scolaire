<script>
  import { onMount } from "svelte";
  import Chargement from "../composants/Chargement.svelte";
  let produitss;
  let produits = [];
  let produit = [];
  let articles = [];
  let article = [];
  let trousse = [];
  let cartable = [];
  let selectedOption = 1;
  let searchValue;
  let urlProducts;
  let vide;
  let slideWidth;
  let indiceDebut = 0;
  const ecart = 5;
  let indiceFin;
  $: indiceFin = indiceDebut + ecart;
  let articless = [];
  let produitts = [];
  let user = [];
  let token = [];
  let loaded = false;

  function comparerAvis(a, b) {
    return b.note - a.note;
  }
  function prixCroissant(a, b) {
    return a.prix - b.prix;
  }
  function prixDecroissant(a, b) {
    return b.prix - a.prix;
  }
  const searchByCategory = async () => {
    const apiUrl = "http://127.0.0.1:8000/search?id_categorie=";
    const selectedCategoryId = JSON.parse(
      localStorage.getItem("selectedCategoryId")
    );
    if (selectedCategoryId == 1) {
      searchValue = "Stylos";
    } else if (selectedCategoryId == 2) {
      searchValue = "Règle";
    } else if (selectedCategoryId == 3) {
      searchValue = "Ciseaux";
    } else if (selectedCategoryId == 4) {
      searchValue = "Crayon";
    } else if (selectedCategoryId == 5) {
      searchValue = "Gomme";
    } else if (selectedCategoryId == 6) {
      searchValue = "Taille-crayon";
    } else if (selectedCategoryId == 7) {
      searchValue = "Cahier";
    } else if (selectedCategoryId == 8) {
      searchValue = "Porte-vues";
    } else if (selectedCategoryId == 9) {
      searchValue = "Trousse";
    } else if (selectedCategoryId == 10) {
      searchValue = "Cartable";
    }
    const selectedTypeId = JSON.parse(localStorage.getItem("selectedTypeId"));
    try {
      if (selectedTypeId == -1) {
        urlProducts = apiUrl + selectedCategoryId;
      } else {
        urlProducts =
          apiUrl + selectedCategoryId + "&id_type=" + selectedTypeId;
      }
      const response = await fetch(urlProducts);
      console.log("urlProducts :" + urlProducts);
      if (response.ok) {
        const productsData = await response.json();
        produit = productsData;
        for (let i = 0; i < produit.length; i++) {
          const imageResponse = await fetch(
            `http://127.0.0.1:8000/image?filename=${produit[i].image}`,
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
            produit[i].imageUrl = URL.createObjectURL(imageData);
            console.log(produit);
          } else {
            console.error(
              `Erreur lors de la récupération de l'image pour le produit ${produit[i].titre}:`,
              imageResponse.status
            );
          }
        }

        console.log("produit", produit);
      } else {
        console.error(
          "Erreur lors de la récupération des produits:",
          response.status
        );
      }
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des produits:",
        error.message
      );
    }
  };

  const searchByTitle = async () => {
    const apiUrl = "http://127.0.0.1:8000/search?titre__like=";
    const titre = localStorage.getItem("recherche");
    searchValue = titre;

    try {
      const response = await fetch(apiUrl + titre);

      if (response.ok) {
        const productsData = await response.json();
        produit = productsData;

        for (let i = 0; i < produit.length; i++) {
          const imageResponse = await fetch(
            `http://127.0.0.1:8000/image?filename=${produit[i].image}`,
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
            produit[i].imageUrl = URL.createObjectURL(imageData);
            console.log(produit);
          } else {
            console.error(
              `Erreur lors de la récupération de l'image pour le produit ${produit[i].titre}:`,
              imageResponse.status
            );
          }
        }
      } else {
        console.error(
          "Erreur lors de la récupération des produits par catégorie:",
          response.status
        );
      }
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des produits par catégorie:",
        error.message
      );
    }
  };

  const choisirFonction = () => {
    const recherche = localStorage.getItem("affichage");
    return recherche === "barre" ? searchByTitle : searchByCategory;
  };

  onMount(async () => {
    setTimeout(() => {
      loaded = true;
    }, 100);

    const selectedSearchFunction = choisirFonction();
    selectedSearchFunction();
    token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion..."
      );
    }
    user = JSON.parse(localStorage.getItem("user"));
    const response = await fetch("http://127.0.0.1:8000/panier?type_id=2", {
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
        vide = 1;
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
          productDetails.nb_article = product.nb_article;
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
    } else {
      console.error(
        "Erreur lors de la récupération du panier :",
        response.statusText
      );
    }

    const responses = await fetch("http://127.0.0.1:8000/panier?type_id=1", {
      method: "GET",
      mode: "cors",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (responses.ok) {
      const cartData = await responses.json();
      produitss = cartData;
      console.log("produits", produitss);
      if (produit.length === 0) {
        console.log("le panier est vide");
        vide = 1;
      }

      const allProducts = produitss.reduce(async (accPromise, product) => {
        const acc = await accPromise;
        const searchResponses = await fetch(
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

        if (searchResponses.ok) {
          const productDetail = await searchResponses.json();
          productDetail.nb_article = product.nb_article;
          return acc.concat([productDetail]);
        } else {
          console.error(
            "Erreur lors de la recherche du produit :",
            searchResponses.statusText
          );
          return acc;
        }
      }, Promise.resolve([]));

      article = await allProducts;

      console.log("Articles récupérés :", article);
    } else {
      console.error(
        "Erreur lors de la récupération du panier :",
        response.statusText
      );
    }

    const responsess = await fetch(
      `http://127.0.0.1:8000/histo?id_user=${user.id}`,
      {
        method: "GET",
        mode: "cors",
        headers: {
          Accept: "application/json",
        },
      }
    );

    if (responsess.ok) {
      const cartData = await responsess.json();
      produitts = cartData;
      console.log("user", produitts);
      if (produit.length === 0) {
        console.log("le panier est vide");
        vide = 1;
      }

      const allProducts = produitts.reduce(async (accPromises, product) => {
        const accs = await accPromises;
        const searchResponses = await fetch(
          `http://127.0.0.1:8000/search?id=${product.id_article}`,
          {
            method: "GET",
            mode: "cors",
            headers: {
              Accept: "application/json",
            },
          }
        );

        if (searchResponses.ok) {
          const productDetailss = await searchResponses.json();
          return accs.concat([productDetailss]);
        } else {
          console.error(
            "Erreur lors de la recherche du produit :",
            searchResponses.statusText
          );
          return accs;
        }
      }, Promise.resolve([]));

      articless = await allProducts;
     
      for (let i = 0; i < articless.length; i++) {
        const imageResponse = await fetch(
          `http://127.0.0.1:8000/image?filename=${articless[i][0].image}`,
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
          articless[i][0].imageUrl = URL.createObjectURL(imageData);
         
          articless.reverse();
        } else {
          console.error(
            `Erreur lors de la récupération de l'image pour le produit ${produit[i].titre}:`,
            imageResponse.status
          );
        }
      }
    }

    try {
      const respons = await fetch(
        "http://127.0.0.1:8000/search?id_categorie=9"
      );

      if (respons.ok) {
        const productsData = await respons.json();
        trousse = productsData;
        console.log("trousse", trousse);
      } else {
        console.error(
          "Erreur lors de la récupération des produits:",
          respons.status
        );
      }
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des produits:",
        error.message
      );
    }

    try {
      const respons = await fetch(
        "http://127.0.0.1:8000/search?id_categorie=10"
      );

      if (respons.ok) {
        const productsData = await respons.json();
        cartable = productsData;
        console.log("trousse", trousse);
      } else {
        console.error(
          "Erreur lors de la récupération des produits:",
          respons.status
        );
      }
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des produits:",
        error.message
      );
    }
  });
  console.log("produit", produit);

  async function handleClick(product) {
    const { id } = product;
    try {
      const response = await fetch("http://127.0.0.1:8000/search?id=" + id);
      const productData = await response.json();
      localStorage.setItem("selectedProduct", JSON.stringify(productData));
      window.location.href = "../fiche_produit";
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des détails du produit:",
        error.message
      );
    }
  }

  async function handleClickHisto(articless) {
    const id = articless.id;

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/search?id=" + articless[0].id
      );
      const productData = await response.json();
      localStorage.setItem("selectedProduct", JSON.stringify(productData));
      window.location.href = "../fiche_produit";
    } catch (error) {
      console.error(
        "Erreur lors de la récupération des détails du produit:",
        error.message
      );
    }
  }

  function choixChange() {
    selectedOption = document.getElementById("product-category").value;
    if (selectedOption === "2") {
      produit = [...produit].sort((a, b) => a.prix - b.prix);
    } else if (selectedOption === "3") {
      produit = [...produit].sort((a, b) => b.prix - a.prix);
    } else if (selectedOption === "4") {
      produit = [...produit].sort((a, b) => b.note - a.note);
    }
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function next() {
    for (let i = 0; i < ecart ; i++) {
      if (indiceFin < articless.length - 1) {
        indiceDebut++;
        await sleep(75);
      }
    }
  }
  async function preced() {
    for (let i = 0; i < ecart ; i++) {
      if (indiceDebut > 0) {
        indiceDebut--;
        await sleep(75);
      }
    }
  }

  async function ajoutCartable() {
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion..."
      );
      return;
    }
    for (const article of articles) {
      const data = {
        id_article: article[0].id,
        type: 6,
        nb_article: article.nb_article,
        datePanier: "14/01/2024",
      };

      const response = await fetch("http://127.0.0.1:8000/panier", {
        method: "POST",
        mode: "cors",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Produit ajouté au panier :", result);
        deleteToCart(article[0].id, 2);
      } else {
        console.error(
          "Erreur lors de l'ajout au panier :",
          response.statusText
        );
      }
    }
    for (const articles of article) {
      const data = {
        id_article: articles[0].id,
        type: 5,
        nb_article: articles.nb_article,
        datePanier: "14/01/2024",
      };

      const response = await fetch("http://127.0.0.1:8000/panier", {
        method: "POST",
        mode: "cors",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Produit ajouté au panier :", result);
        deleteToCart(articles[0].id, 1);
      } else {
        console.error(

          "Erreur lors de l'ajout au panier :",
          response.statusText
        );
      }
    }
  }

  async function deleteToCart(product, type) {
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion..."
      );
      return;
    }

    try {
      console.log("id", product);
      const response = await fetch(
        `http://127.0.0.1:8000/panier?article_id=${product}&type_id=${type}`,
        {
          method: "DELETE",
          mode: "cors",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const result = await response.json();
        console.log("Produit supprime du panier :", result);
        location.reload();
      } else {
        console.error(
          "Erreur lors de la suppression de l'article :",
          response.statusText
        );
      }
    } catch (e) {
      console.error("Erreur lors de la requête d'ajout au panier :", e);
    }
  }
</script>

<main>
  {#if !loaded}
    <Chargement />
  {:else}
    <div class="form-group">
      <p>Plus de {produit.length} résultats pour <b>"{searchValue}"</b></p>
      <select
        id="product-category"
        name="product-category"
        on:change={choixChange}
      >
        <option value="1">Trier par : </option>
        <option value="2">Prix : par ordre croissant</option>
        <option value="3">Prix : par ordre decroissant</option>
        <option value="4">Note : par ordre decroissant</option>
      </select>
    </div>

    <section>
      <div class="table-section">
        {#if articles.length > 0}
          <table>
            <thead>
              <tr>
                <th colspan="2">Trousse</th>
              </tr>
            </thead>
            <tbody>
              {#each articles as trousses}
                {#if trousses[0].categorie.id == 9}
                  <tr>
                    <td>{trousses[0].titre}</td>
                    <td>{trousses[0].prix}€</td>
                  </tr>
                {/if}
              {/each}
            </tbody>
          </table>

          <table>
            <thead>
              <tr>
                <th>Article</th>
                <th>Qté</th>
                <th>P/u</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {#each articles as stylo}
                {#if stylo[0].categorie.id !== 9}
                  <tr>
                    <td>{stylo[0].titre}</td>
                    <td>{stylo.nb_article}</td>
                    <td>{stylo[0].prix}</td>
                    <td>{stylo.nb_article * stylo[0].prix}</td>
                  </tr>
                {/if}
              {/each}
            </tbody>
          </table>
        {:else}
          <thead>
            <tr>
              <th id="not" colspan="2">Vous n'avez pas de trousse !</th>
            </tr>
          </thead>
        {/if}
        {#if article.length > 0}
          <table>
            <thead>
              <tr>
                <th colspan="2">Cartable</th>
              </tr>
            </thead>
            <tbody>
              {#each article as trousses}
                {#if trousses[0].categorie.id == 10}
                  <tr>
                    <td>{trousses[0].titre}</td>
                    <td>{trousses[0].prix}€</td>
                  </tr>
                {/if}
              {/each}
            </tbody>
          </table>
          <table>
            <thead>
              <tr>
                <th>Nom</th>
                <th>Qté</th>
                <th>P/u</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {#each article as stylo}
                {#if stylo[0].categorie.id !== 10}
                  <tr>
                    <td>{stylo[0].titre}</td>
                    <td>{stylo.nb_article}</td>
                    <td>{stylo[0].prix}</td>
                    <td>{stylo.nb_article * stylo[0].prix}</td>
                  </tr>
                {/if}
              {/each}
            </tbody>
          </table>
        {:else}
          <thead>
            <tr>
              <th id="not" colspan="2">Vous n'avez pas de cartable !</th>
            </tr>
          </thead>
        {/if}
        <button class="button1" on:click={ajoutCartable}
          >Ajouter au panier</button
        >
      </div>

      <hr id="vert" />
      <div class="products-section">
        {#each produit as product}
          <div class="product-item" on:click={() => handleClick(product)}>
            <img class="img" src={product.imageUrl} alt="produit" />
            <div class="container">
              <div class="item item1">{product.titre}</div>
              <div class="item item5">{product.prix}€</div>
              <div class="item item6">
                <img
                  src="src\img\Avis{Math.round(product.note)}.png"
                  alt="produit"
                />
              </div>
            </div>
          </div>
        {/each}
      </div>
    </section>
    {#if token}
      <h1>Votre historique de navigation</h1>
      <hr />
      <div class="slider">
        <button id="buttonslide" on:click={() => preced()}> &lt; </button>
        {#each articless.slice(indiceDebut, indiceFin) as product}
        <div class="product-items" on:click={() => handleClickHisto(product)}>
          <img class="img" src={product[0].imageUrl} alt="produit" />
          <div class="container">
            <div class="item item1">{product[0].titre}</div>
            <div class="item item5">{product[0].prix}€</div>
            <div class="item item6">
              <img
                src="src\img\Avis{Math.round(product[0].note)}.png"
                alt="produit"
              />
            </div>
          </div>
          </div>
        {/each}
        <button id="buttonslides" on:click={() => next()}>></button>
      </div>
    {/if}
  {/if}
</main>

<style>
  table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 10px;
    border-radius: 10px;
  }

  th,
  td {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
    text-align: center;
    opacity: 0.8;
  }

  th {
    background-color: orange;
  }

  td {
    background-color: #ffeedd;
  }

  td:nth-child(2) {
    background-color: white;
  }

  section {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }

  .table-section {
    flex: 0 0 20%;
  }

  .products-section {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    margin-top: 20px;
  }

  #vert {
    margin: 15px;
    min-height: 100vh;
  }

  div {
    text-align: center;
  }

  .img {
    width: 200px;
    height: 200px;
  }

  
  .container {
    display: grid;
  }

  .product-item {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border-radius: 10px;
    transition: transform 0.3s ease;
  }

  .product-item:hover {
    transform: scale(1.05);
  }

  .product-items {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border-radius: 10px;
    transition: transform 0.3s ease;
    margin-left: 35px;

  }

  .product-items:hover {
    transform: scale(1.05);
  }

  .item {
    background-color: white;
    padding: 10px;
    text-align: center;
    font-size: 14px;
  }

  .item1 {
    grid-column: 1 / 4;
    background-color: white;
  }

  .item5 {
    grid-column: 1 / 2;
    color: rgb(0, 255, 221);
  }

  .item6 {
    grid-column: 2 / 4;
    color: rgb(99, 255, 47);
  }

  main {
    background-color: #faf5f0;
    font-family: Arial, Helvetica, sans-serif;
    min-height: 100vh;
  }

  .form-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    padding-bottom: 10px;
    margin-bottom: 20px;
    height: 30px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .form-group::before {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background-color: #ccc;
  }

  select {
    border-radius: 7px;
    width: auto;
    height: 23px;
    background-color: orange;
    border-radius: 15px;
    padding-left: 5px;
    border: none;
  }

  select:hover {
    background-color: #feb52f;
  }

  b {
    color: rgb(255, 89, 0);
  }

  #not {
    display: flex;
    margin-left: 30px;
    margin-top: 30px;
    height: 35px;
    width: 200px;
    align-items: center;
    text-align: center;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .slider {
    margin-left: 38px;
    overflow: hidden;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.5s ease;
  }

  .content-slider {
    min-width: 200px;
    box-sizing: border-box;
    padding: 0 10px;
  }

  .content-slider img {
    object-fit: cover;
  }

  #buttonslide {
    margin-top: 150px;
    border-radius: 50px;
    width: 30px;
    height: 30px;
    border: 1px solid black;
    margin-left: 50px;
  }

  #buttonslides {
    margin-top: 150px;
    border-radius: 50px;
    width: 30px;
    height: 30px;
    border: 1px solid black;
    margin-left: 50px;
  }

  .button1 {
    height: 60px;
    width: 200px;
    margin-top: 30px;
    margin-left: 25px;
    background-color: orange;
    cursor: pointer;
    border-radius: 5px;
  }
</style>
