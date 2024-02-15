<script>
    import { onMount } from "svelte";
 
    let total = 0;
     let nbarticle = 0;
 
     let produit = [];
     let articles = []; 
     let vide = 0;
 
 onMount(async () => {
     const token = window.localStorage.getItem("token");
     console.log("Token:", token);
 
     if (!token) {
         console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
         window.location.href("../connexion");
     }
 
     try {
         const response = await fetch("http://127.0.0.1:8000/panier?type_id=1", {
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
             console.log("produits", produit)
             if(produit.length === 0){
               console.log("le panier est vide");
               vide = 1;
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
 
             articles = await allProducts;
             console.log("Articles récupérés :", articles);
             articles.forEach((produit) => {
                     total += produit[0].prix * produit.nb_article;
             });
             articles.forEach((produit) => {
               nbarticle += produit.nb_article;
             });
            
             console.log("Nombre d'articles :", nbarticle);
         } else {
             console.error("Erreur lors de la récupération du panier :", response.statusText);
         }
     } catch (e) {
         console.error("Erreur lors de la requête de récupération du panier :", e);
     }
 });

 async function ajoutPanier(){
    const token = window.localStorage.getItem("token");
     console.log("Token:", token);
 
     if (!token) {
         console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
         return;
     }
     for(const article of articles){
        const data = {
                    id_article: article[0].id,
                    type: 0,
                    nb_article: article.nb_article,
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
                    console.log("Produit ajouté au panier :", result);;
                    deleteToCart(article[0].id);
					
                } else {
                    console.error("Erreur lors de l'ajout au panier :", response.statusText);
                }
            }
 }
 
    async function deleteToCart(product) {
       const token = window.localStorage.getItem("token");
     console.log("Token:", token);
 
     if (!token) {
         console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
         return;
     }
 
     try {
       console.log('id', product);
       const response = await fetch(`http://127.0.0.1:8000/panier?article_id=${product}&type_id=1`, {
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
         location.reload();
       } else {
         console.error("Erreur lors de la suppression de l'article :", response.statusText);
       }
     } catch (e) {
       console.error("Erreur lors de la requête d'ajout au panier :", e);
     }
   }
 
   async function update(product, nb) {
       const token = window.localStorage.getItem("token");
     console.log("Token:", token);
 
     if (!token) {
         console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
         return;
     }
 
     try {
       console.log('id', product);
       const response = await fetch(`http://127.0.0.1:8000/panier?id_article=${product[0].id}&nb_article=${nb}`, {
         method: "PUT",
         mode: "cors",
         headers: {
           Accept: "application/json",
           Authorization: `Bearer ${token}`,
         },
       });
 
       if (response.ok) {
         const result = await response.json();
         console.log("Produit modifié au panier :", result);
         location.reload();
       } else {
         console.error("Erreur lors de la modification de l'article :", response.statusText);
       }
     } catch (e) {
       console.error("Erreur lors de la requête de modification au panier :", e);
     }
   }
 
   console.log("total", {nbarticle});
  
  
 
    </script>
 
 <body>
 <main>
 
 {#if {nbarticle}===0 || !nbarticle}
 <div class="panier-vide">
   <div>
     <p>Vous n'avez pas de cartable.</p>
   </div>
   <div>
     <button on:click={() => window.location.href = "../pageproduits"}>Retournez à la boutique</button>
   </div>
  <div>
   <img src="src/img/Paniervide.jpg" alt="Image vide" />
  </div>
  
 
 </div>
 {:else}
   <div class = "container">
    
    <div class = "item1">
     <p style="margin-right: 80px;">Total ({nbarticle} articles) : {total}€</p>
        <button class = "button1" on:click={ajoutPanier}>Ajouter au panier</button>
    </div>
    
    <div class = "item2">
        <p>Mon cartable</p>
    </div>
    
    <div>
         
        {#each articles as product, index}
        
          <div class="product-item {index === 0 ? 'first-product' : ''}">
            <div class="product-image">
              <img src="src\img\Stylo.png" alt="produit" />
            </div>
            <div class="containers">
              <div >{product[0].titre}</div>
              <div>{product[0].prix}€</div>
              <div><button> Quantite</button></div>
            </div>
            <div class = "poubelle">
             <button on:click={() => deleteToCart(product[0].id)}>
               <img src="src/img/Poubelle.png" alt="Logo Recherche" style="width: 20px; height: 20px;" />
             </button>
            </div>
            <div class="form-group">
             <label for="product-couleur">Quantite:</label>
             <select  id="product-couleur" name="product-category" on:change={(event) => update(product,event.target.value)}>
                 <option value=1 selected={product.nb_article === 1}>1</option>
                 <option value=2  selected={product.nb_article === 2}>2</option>
                 <option value=3  selected={product.nb_article === 3}>3</option>
                 <option value=4  selected={product.nb_article === 4}>4</option>
                 <option value=5  selected={product.nb_article === 5}>5</option>
                 <option value=6  selected={product.nb_article === 6}>6</option>
                 <option value=7  selected={product.nb_article === 7}>7</option>
             </select>
         </div>
          </div>
        
         {/each}
    </div>
   </div>
   {/if}
 </main>
 </body>
    
    <style>
 
     .form-group{
       margin-left: 50px;
       width: 90px;
       color : red;
     }
      .product-item:not(:first-child) {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        margin-left : 100px;
        height: 200px;
        background-color: #FFEEDD;       
      }

      .product-item:not(:first-child)::before {
        
    content: "";
    position: absolute;    
    left : 100px;
    width: 7px;
    height: 220px; 
    background-color: black; 
   
}



.product-item:not(:first-child)::after {
    content: "";
    position: absolute;
   left: 106px;
    width: 73px;
    height: 5px; 
    background-color: black;
   
}



      .poubelle {
     margin-left: 100px; 
   }
  
    
      .product-image {
        margin-right: 10px;
      }

      .first-product {
        display: flex;
        align-items: center;
        height: 200px;
        margin-bottom: 10px; 
        background-color: #FFEEDD;
  }
 
      .item1{
         background-color: #FFEEDD;
         display: flex;
         align-items: center;     
       }
 
       .item1 p{
         margin-left: 100px;
       }
 
      .item2{
         background-color: #FFEEDD;
         text-align: center;
         color : #5BC3EB;
         font-size: 22px;
      }
 
      .container{
         margin-top: 50px;
         margin-right: 50px;
         margin-left: 50px;
         
      }
 
      .panier-vide button{
       background-color : orange;
       border : none;
       border-radius : 6px;
       height: 30px;
       width: 150px;
       opacity: 1;
       transition: opacity 0.3s ease; 
       cursor: pointer;
      }
 
      .panier-vide button:hover {
       opacity: 0.8;
       }
 
      .panier-vide{
       margin-top: 50px;
         margin-right: 50px;
         margin-left: 300px;
         display: grid;
        grid-template-columns: 1fr ;
        grid-gap: 20px;
        justify-content: center;
        align-items: center;
      }
 
      .panier-vide p {
   font-weight: bold;
   font-size: 1.2em; 
 }
 
 
      img{
       width: 200px;
       height: 200px;
       border-radius: 10px;
      }
 
      
      
      .button1{
       background-color : orange;
       border : none;
       border-radius : 6px;
       height: 30px;
       width: 150px;
       opacity: 1;
       transition: opacity 0.3s ease; 
       cursor: pointer;
      }
 
      .button1:hover {
       opacity: 0.8;
       }
 
      body{
         background-color: #FAF5F0;
         
      }
 
     
 
 
    </style>
    