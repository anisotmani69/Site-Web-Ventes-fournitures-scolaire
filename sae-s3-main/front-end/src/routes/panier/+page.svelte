<script>
  import { onMount } from "svelte";
  import Chargement from "../composants/Chargement.svelte";

  let total = 0;
  let nbarticle = 0;
  let nbarticleT = 0;
  let nbarticleC = 0;
  let totalT = 0;
  let totalC = 0;

  let produit = [];
  let articles = [];
  let vide = 0;
  let loaded = false;
  let articless = [];
  let trousse = [];
  let trousses = [];
  let cartable = [];
  let cartables = [];
  let typeP = 0;
  let typeC = 6;
  let typeT = 5;
  let showTrousse = 0;
  let showCartable =0;
  let user = [];

  onMount(async () => {
    setTimeout(() => {
      loaded = true;
    }, 100);
    const token = window.localStorage.getItem("token");
    user = JSON.parse(window.localStorage.getItem("user"));
    console.log("user:", user);

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion..."
      );
      window.location.href("../connexion");
    }

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
        produit = cartData;
        console.log("produits", produit);
        if (produit.length === 0) {
          console.log("le panier est vide");
          vide = 1;
        }

        const allProducts = produit.reduce(async (accPromise, product) => {
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

        articles.forEach((produit) => {
          total += produit[0].prix * produit.nb_article;
        });
        articles.forEach((produit) => {
          nbarticle += produit.nb_article;
        });
       

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

        console.log("Nombre d'articles :", nbarticle);
      } else {
        console.error(
          "Erreur lors de la récupération du panier :",
          response.statusText
        );
      }
    } catch (e) {
      console.error("Erreur lors de la requête de récupération du panier :", e);
    }


    const response = await fetch("http://127.0.0.1:8000/panier?type_id=5", {
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
             trousse = cartData;
             console.log("produits", trousse)
             
 
             const allProducts = trousse.reduce(async (accPromise, product) => {
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
 
             trousses = await allProducts;

             trousses.forEach((produit) => {
          total += produit[0].prix * produit.nb_article;
        });
        trousses.forEach((produit) => {
          nbarticle += produit.nb_article;
        });
       
             for (let i = 0; i < trousses.length; i++) {

const imageResponses = await fetch(
  `http://127.0.0.1:8000/image?filename=${trousses[i][0].image}`,
  {
    method: "GET",
    mode: "cors",
    headers: {
      Accept: "application/json",
    },
  }
);

if (imageResponses.ok) {
  const imageData = await imageResponses.blob();
  trousses[i][0].imageUrl = URL.createObjectURL(imageData);
  console.log(articles);
} else {
  console.error(
    `Erreur lors de la récupération de l'image pour le produit ${trousses[i].titre}:`,
    imageResponses.status
  );
}
}
             console.log("Articles trousse récupérés :", trousses);
         } else {
             console.error("Erreur lors de la récupération du panier :", response.statusText);
         }
    

     
         const responses = await fetch("http://127.0.0.1:8000/panier?type_id=6", {
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
             cartable = cartData;
             console.log("produits", cartable)
             
 
             const allProductss = cartable.reduce(async (accPromise, product) => {
                 const acc = await accPromise;
                 const searchResponses = await fetch(`http://127.0.0.1:8000/search?id=${product.id_article}`, {
                     method: "GET",
                     mode: "cors",
                     headers: {
                         Accept: "application/json",
                         "Content-Type": "application/json",
                         Authorization: `Bearer ${token}`,
                     },
                 });
        
                 if (searchResponses.ok) {
                     const productDetail = await searchResponses.json();
                     productDetail.nb_article = product.nb_article;
                     return acc.concat([productDetail]);
                 } else {
                     console.error("Erreur lors de la recherche du produit :", searchResponses.statusText);
                     return acc; 
                 }
             }, Promise.resolve([]));
 
             cartables = await allProductss;

             cartables.forEach((produit) => {
          total += produit[0].prix * produit.nb_article;
        });
        cartables.forEach((produit) => {
          nbarticle += produit.nb_article;
        });

             for (let i = 0; i < cartables.length; i++) {

const imageResponse = await fetch(
  `http://127.0.0.1:8000/image?filename=${cartables[i][0].image}`,
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
  cartables[i][0].imageUrl = URL.createObjectURL(imageData);
  console.log("dsds",cartables);
} else {
  console.log("quoicoubeh")
  console.error(
    `Erreur lors de la récupération de l'image pour le produit ${cartables[i].titre}:`,
    imageResponse.status
  );
}
}
             
             console.log("Articles cartable récupérés :", cartables);
            }

  });

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

  async function passeCommande() {
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion..."
      );
      return;
    }

    window.location.href = "../Livraison";
  }

  async function update(product, nb) {
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
        `http://127.0.0.1:8000/panier?id_article=${product[0].id}&nb_article=${nb}`,
        {
          method: "PUT",
          mode: "cors",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const result = await response.json();
        console.log("Produit modifié au panier :", result);
        location.reload();
      } else {
        console.error(
          "Erreur lors de la modification de l'article :",
          response.statusText
        );
      }
    } catch (e) {
      console.error("Erreur lors de la requête de modification au panier :", e);
    }
  }

  async function showTrousseP(){
    if (showTrousse ==1){
      showTrousse =0;
    }
    else{
      showTrousse=1
    }
  }

  async function showCartableP(){
    if (showCartable ==1){
      showCartable =0;
    }
    else{
      showCartable=1
    }
  }

  let panierVide = nbarticle === 0;
  console.log("total", { nbarticle });
</script>

<body>
  {#if !loaded}
    <Chargement />
  {:else}
    <main>
      {#if !nbarticle && trousses.length === 0 && cartables.length ===0}
        <div class="panier-vide">
          <div>
            <p>Votre panier est vide.</p>
          </div>
          <div>
            <button on:click={() => (window.location.href = "../pageproduits")}
              >Retournez à la boutique</button
            >
          </div>
          <div>
            <img src="src/img/Paniervide.jpg" alt="Image vide" />
          </div>
        </div>
      {:else}
        <div class="container">
          <div class="item1">
            <p style="margin-right: 80px;">
              {#if user.reduction ==1}
              Total ({nbarticle} articles) :<strike>{total} </strike> {total * 0.95}€
              {:else}
              Total ({nbarticle} articles) : {total}€
              {/if}
            </p>
            <button class="button1" on:click={passeCommande}
              >Passer la commande</button
            >
          </div>

          <div class="item2">
            <p>Mon panier</p>
          </div>

          <div class = "produits-panier">
            {#each articles as product}
              <div class="product-item">
                <div class="product-image">
                  <img class="img" src={product[0].imageUrl} alt="produit" />
                </div>
                <div class="containers">
                  <div>{product[0].titre}</div>
                  <div>{product[0].prix}€</div>
                 
                </div>
                <div class="poubelle">
                  <button on:click={() => deleteToCart(product[0].id, typeP)}>
                    <img
                      src="src/img/Poubelle.png"
                      alt="Logo Recherche"
                      style="width: 20px; height: 20px;"
                    />
                  </button>
                </div>
                <div class="form-group">
                  <select
                    id="product-couleur"
                    name="product-category"
                    on:change={(event) => update(product, event.target.value)}
                  >
                  <option value="1" selected={product.nb_article === 1}
                  >Quantite: 1</option
                >
                <option value="2" selected={product.nb_article === 2}
                  >Quantite: 2</option
                >
                <option value="3" selected={product.nb_article === 3}
                  >Quantite: 3</option
                >
                <option value="4" selected={product.nb_article === 4}
                  >Quantite: 4</option
                >
                <option value="5" selected={product.nb_article === 5}
                  >Quantite: 5</option
                >
                <option value="6" selected={product.nb_article === 6}
                  >Quantite: 6</option
                >
                <option value="7" selected={product.nb_article === 7}
                  >Quantite: 7</option
                >
                <option value="8" selected={product.nb_article === 8}
                  >Quantite: 8</option
                >
                <option value="9" selected={product.nb_article === 9}
                  >Quantite: 9</option
                >
                  </select>
                </div>
              </div>
            {/each}
          </div>
          {#if cartables.length !==0}
          <div class = "produits-cartable">
            <h1>Trousse</h1>
            <div class="cartables">
              
              {#each cartables as product}
              {#if product[0].categorie.id ==9}
              <div class="product-item">
                <div class="product-image">
                  <img class="img" src={product[0].imageUrl} alt="produit" />
                </div>
                <div class="containers">
                  <div>{product[0].titre}</div>
                  <div>{product[0].prix}€</div>
                  
                </div>
                <div class="poubelle">
                  <button on:click={() => deleteToCart(product[0].id, typeC)}>
                    <img
                      src="src/img/Poubelle.png"
                      alt="Logo Recherche"
                      style="width: 20px; height: 20px;"
                    />
                  </button>
                </div>
                <div class="form-group">
                 
                  <select
                    id="product-couleur"
                    name="product-category"
                    on:change={(event) => update(product, event.target.value)}
                  >
                  <option value="1" selected={product.nb_article === 1}
                  >Quantite: 1</option
                >
                <option value="2" selected={product.nb_article === 2}
                  >Quantite: 2</option
                >
                <option value="3" selected={product.nb_article === 3}
                  >Quantite: 3</option
                >
                <option value="4" selected={product.nb_article === 4}
                  >Quantite: 4</option
                >
                <option value="5" selected={product.nb_article === 5}
                  >Quantite: 5</option
                >
                <option value="6" selected={product.nb_article === 6}
                  >Quantite: 6</option
                >
                <option value="7" selected={product.nb_article === 7}
                  >Quantite: 7</option
                >
                <option value="8" selected={product.nb_article === 8}
                  >Quantite: 8</option
                >
                <option value="9" selected={product.nb_article === 9}
                  >Quantite: 9</option
                >
                  </select>
                </div>
              </div>
              {/if}
            {/each}
            
            </div>
            {#if showCartable==1}
            <div class="cartables-produit">
              {#each cartables as product}
              {#if product[0].categorie.id !==9}
              <div class="product-items">
                <div class="product-image">
                  <img class="img" src={product[0].imageUrl} alt="produit" />
                </div>
                <div class="containers">
                  <div>{product[0].titre}</div>
                  <div>{product[0].prix}€</div>
                
                </div>
                <div class="poubelle">
                  <button on:click={() => deleteToCart(product[0].id, typeC)}>
                    <img
                      src="src/img/Poubelle.png"
                      alt="Logo Recherche"
                      style="width: 20px; height: 20px;"
                    />
                  </button>
                </div>
                <div class="form-group">
                  
                  <select
                    id="product-couleur"
                    name="product-category"
                    on:change={(event) => update(product, event.target.value)}
                  >
                    <option value="1" selected={product.nb_article === 1}
                      >Quantite: 1</option
                    >
                    <option value="2" selected={product.nb_article === 2}
                      >Quantite: 2</option
                    >
                    <option value="3" selected={product.nb_article === 3}
                      >Quantite: 3</option
                    >
                    <option value="4" selected={product.nb_article === 4}
                      >Quantite: 4</option
                    >
                    <option value="5" selected={product.nb_article === 5}
                      >Quantite: 5</option
                    >
                    <option value="6" selected={product.nb_article === 6}
                      >Quantite: 6</option
                    >
                    <option value="7" selected={product.nb_article === 7}
                      >Quantite: 7</option
                    >
                    <option value="8" selected={product.nb_article === 8}
                      >Quantite: 8</option
                    >
                    <option value="9" selected={product.nb_article === 9}
                      >Quantite: 9</option
                    >
                  </select>
                </div>
              </div>
              {/if}
            {/each}
            </div> 
            {/if}
            {#if showCartable==0}
              <div><button button class = "img" on:click={showCartableP}> &darr;</button></div>
              {:else}
              <div><button button class = "img" on:click={showCartableP}> &uarr;</button></div>
              {/if}
            
          </div>
          {/if}



          {#if trousses.length !==0}

          <div class = "produits-trousse">
           
             <div class="trousses">
              <h1>Cartable</h1>
              {#each trousses as product}
              {#if product[0].categorie.id == 10}
              <div class="product-item">
                <div class="product-image">
                  <img class="img" src={product[0].imageUrl} alt="produit" />
                </div>
                <div class="containers">
                  <div>{product[0].titre}</div>
                  <div>{product[0].prix}€</div>
                  
                </div>
                <div class="poubelle">
                  <button on:click={() => deleteToCart(product[0].id, typeT)}>
                    <img
                      src="src/img/Poubelle.png"
                      alt="Logo Recherche"
                      style="width: 20px; height: 20px;"
                    />
                  </button>
                </div>
                <div class="form-group">
    
                  <select
                    id="product-couleur"
                    name="product-category"
                    on:change={(event) => update(product, event.target.value)}
                  >
                  <option value="1" selected={product.nb_article === 1}
                  >Quantite: 1</option
                >
                <option value="2" selected={product.nb_article === 2}
                  >Quantite: 2</option
                >
                <option value="3" selected={product.nb_article === 3}
                  >Quantite: 3</option
                >
                <option value="4" selected={product.nb_article === 4}
                  >Quantite: 4</option
                >
                <option value="5" selected={product.nb_article === 5}
                  >Quantite: 5</option
                >
                <option value="6" selected={product.nb_article === 6}
                  >Quantite: 6</option
                >
                <option value="7" selected={product.nb_article === 7}
                  >Quantite: 7</option
                >
                <option value="8" selected={product.nb_article === 8}
                  >Quantite: 8</option
                >
                <option value="9" selected={product.nb_article === 9}
                  >Quantite: 9</option
                >
                  </select>
                </div>
              </div>
              {/if}
            {/each}
            
            </div>
            {#if showTrousse ==1}
            <div class="trousses-produit">
              {#each trousses as product}
              {#if product[0].categorie.id !==10}
              <div class="product-items">
                <div class="product-image">
                  <img class="img" src={product[0].imageUrl} alt="produit" />
                </div>
                <div class="containers">
                  <div>{product[0].titre}</div>
                  <div>{product[0].prix}€</div>
                 
                </div>
                <div class="poubelle">
                  <button on:click={() => deleteToCart(product[0].id, typeT)}>
                    <img
                      src="src/img/Poubelle.png"
                      alt="Logo Recherche"
                      style="width: 20px; height: 20px;"
                    />
                  </button>
                </div>
                <div class="form-group">
                 
                  <select
                    id="product-couleur"
                    name="product-category"
                    on:change={(event) => update(product, event.target.value)}
                  >
                  <option value="1" selected={product.nb_article === 1}
                  >Quantite: 1</option
                >
                <option value="2" selected={product.nb_article === 2}
                  >Quantite: 2</option
                >
                <option value="3" selected={product.nb_article === 3}
                  >Quantite: 3</option
                >
                <option value="4" selected={product.nb_article === 4}
                  >Quantite: 4</option
                >
                <option value="5" selected={product.nb_article === 5}
                  >Quantite: 5</option
                >
                <option value="6" selected={product.nb_article === 6}
                  >Quantite: 6</option
                >
                <option value="7" selected={product.nb_article === 7}
                  >Quantite: 7</option
                >
                <option value="8" selected={product.nb_article === 8}
                  >Quantite: 8</option
                >
                <option value="9" selected={product.nb_article === 9}
                  >Quantite: 9</option
                >
                  </select>
                </div>
              </div>
             {/if}
            {/each}
            </div>
             
            {/if}
            {#if showTrousse ==0}
            <button  on:click={showTrousseP}> &darr;</button>
            {:else}
            <button button  on:click={showTrousseP}> &uarr;</button>
            {/if}
            </div>
            {/if}
        </div>
         
      {/if}
    </main>
  {/if}
</body>

<style>

select {
    border-radius: 5px;
    width: auto;
    height: 35px;
    background-color:  orange; 
    cursor: pointer;
    border: 0;
    padding-left: 10px;
    padding-right: 10px;
    transition: 0.3s ease;
    }

    select:hover {
      background-color: #feb52f; 
    }
  main {
    min-width: 100vh;
    font-size: 14px;
  }

  .trousses-produit{
    margin-left: 80px;
    width: 550px;
  }

  .produits-trousse{
    border: 2px solid black;
    margin-top: 50px;
    border-radius: 5px;
  }

  .produits-trousse h1{
    margin-left: 600px;
  }

  .produits-trousse button{
    width: 100%;
    background-color: #FFB13C;
    border: none;
    height: 23px;
    opacity: 1;
    transition: opacity 0.3s ease;
    cursor: pointer;
    font-size: 19px;
  }

  .produits-trousse button:hover{
    opacity: 0.8;
  }

  .produits-cartable{
    border: 2px solid black;
    border-radius: 5px;
   
  }

  .produits-cartable h1{
    margin-left: 600px;
  }

  .produits-cartable button{
   padding: 0;
   margin:0;
    width: 100%;
    background-color: #FFB13C;
    border: none;
    height: 23px;
    opacity: 1;
    transition: opacity 0.3s ease;
    cursor: pointer;
    font-size: 19px;
  }

  .produits-cartable button:hover{
    opacity: 0.8;
  }

  .cartables-produit{
    margin-left: 80px;
    width: 550px;
  }

  .form-group {
    margin-left: 50px;
    width: 90px;
    color: red;
  }
  .product-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    margin-left: 250px;
    width: 900px;
    background-color: #ffeedd;
    border-radius: 5px;
    height: 250px;
  }

  .product-items {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    margin-left: 250px;
    width: 820px;
    background-color: #ffeedd;
    border-radius: 5px;
    height: 250px;
  }
  .poubelle {
    margin-left: 100px;
    
  }

  .poubelle button {
    background-color: #ffeedd;
    cursor: pointer;
  }

  .product-image {
    margin-right: 10px;
    
  }

  .item1 {
    background-color: #ffeedd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
  }

  .item1 p {
    margin-left: 100px;
  }

  .item2 {
    background-color: #ffeedd;
    text-align: center;
    color: #5bc3eb;
    font-size: 22px;
  }

  .container {
    margin-top: 0;
    margin-right: 50px;
    margin-left: 50px;
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

  .panier-vide p {
    font-weight: bold;
    font-size: 1.7em;
    margin-left: 70px;
  }

  img {
    width: 400px;
    height: 400px;
    border-radius: 10px;
  }

  .img {
    width: 230px;
    height: 230px;
    margin-left: 10px;
  }

  .button1 {
    background-color: orange;
    border: none;
    border-radius: 6px;
    height: 35px;
    width: 150px;
    opacity: 1;
    transition: opacity 0.3s ease;
    cursor: pointer;
  }

  .button1:hover {
    opacity: 0.8;
  }

  body {
    background-color: #faf5f0;
    padding-top: 25px;
    margin: 0;
  }
</style>
