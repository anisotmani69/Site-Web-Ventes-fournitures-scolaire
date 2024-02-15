<script>
import { onMount } from "svelte";
import Chargement from "../composants/Chargement.svelte";
let produit = [];
let user = [];
let loaded = false;


  onMount(async() => {
    setTimeout(() => {
      loaded = true;
    }, 100);
     user = JSON.parse(localStorage.getItem("user"));
    console.log("d",user.id);
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
        console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
        window.location.href("../connexion");
    }

    const apiUrl = "http://127.0.0.1:8000/search?id_vendeur=";
  const titre = user.id;


  try {
    const response = await fetch(apiUrl + titre);
    
    if (response.ok) {
      const productsData = await response.json();
      produit = productsData;
      for (let i = 0; i < produit.length; i++) {
          const imageResponse = await fetch(`http://127.0.0.1:8000/image?filename=${produit[i].image}`, {
            method: "GET",
             mode: "cors",
             headers: {
                 Accept: "application/json",
             },
         });
          
          if (imageResponse.ok) {
            const imageData = await imageResponse.blob();
            produit[i].imageUrl = URL.createObjectURL(imageData);
            console.log(produit);
          } else {
            console.error(`Erreur lors de la récupération de l'image pour le produit ${produit[i].titre}:`, imageResponse.status);
          }
        }
    } else {
      console.error('Erreur lors de la récupération des produits par catégorie:', response.status);
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des produits par catégorie:', error.message);
  }

  });

  
  
  
  async function handleClick(event, product) {
    event.stopPropagation();
    const { id } = product;
    try {
      const response = await fetch("http://127.0.0.1:8000/search?id=" +id);
      const productData = await response.json();  
      localStorage.setItem("selectedProductVendeur", JSON.stringify(productData));
      window.location.href = "../modification";
    } catch (error) {
      console.error('Erreur lors de la récupération des détails du produit:', error.message);
    }
  }

  const supprimer = async ( product) => {
   
   const response = await fetch(`http://127.0.0.1:8000/article?article_id=${product.id}`, {
   method: "DELETE",
   mode: "cors",
   headers: {
      Accept: "application/json",
   },
   
   })
   if (response.ok) {
   const data = await response.json();
   console.log(data);
   window.location.href= "../annonce";
   }
   else{
   console.log("ça marche pas");
   const errorData = await response.json();
   console.error("Erreur lors de la requête :", response.status, response.statusText, errorData);
   
   }
   };
  

   
  </script>
  
  <style>

    section {
      display: flex;
      justify-content: space-between;
    
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


    div {
      text-align: center;
    }

  
  
    img {
      max-width: 100%;
      height: auto;
    }

    #imageProduit {
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

.item3 {
    grid-column: 1 / 2;
    color : rgb(0, 255, 221);
    
}

.item5 {
    grid-column: 1 / 2;
    color : rgb(0, 255, 221);
    
}

.item4 {
    grid-column: 2 / 4;
    color : rgb(99, 255, 47);
}

.item6 {
    grid-column: 2 / 4;
    color : rgb(99, 255, 47);
}

main{
  margin-top: 0px;
  background-color: #FAF5F0;
  font-family :Arial, Helvetica, sans-serif;
  min-height: 100vh;
}

hr{
  margin: 15px;
  min-height: 100vh;

}

button{
  border-radius: 20px;
  background-color: #FFB13C;
  margin-top: 20px;
      border : none;
      height: 30px;
      width: 150px;
      opacity: 1;
      transition: opacity 0.3s ease; 
      cursor: pointer;
     }

     button:hover {
      opacity: 0.8;
      }

      .panier-vide{
      margin-top: 50px;
       margin-left: 500px;
        
        display: grid;
       grid-template-columns: 1fr ;
       grid-gap: 20px;
       justify-content: center;
       align-items: center;
     }

     .panier-vide p {
  font-weight: bold;
  font-size: 1.7em; 
  margin-left: 40px;
}

.panier-vide img{
      width: 400px;
      height: 400px;
      border-radius: 10px;
     }

     .overlay-image {
      position: absolute;
     background-color: white;
     z-index: 1;
     cursor: pointer;
     margin-left: 10px;
    }

  </style>
  
  <main>
    {#if !loaded}
    <Chargement />
  {:else}
    <section>
      {#if produit.length !=0}
      <div class="table-section">

  <button id ="ajouter" on:click={() => window.location.href = "../vendeur"}>
      Nouvelle annonce
    
    
  </button>
      </div>
      
      <hr>   
      <div class="products-section">
        {#each produit as product}
          <div class="product-item" on:click={() => handleClick(e, product)}>
            <img on:click={() => supprimer(product)} class="overlay-image" src="src/img/Poubelle.png" alt="Logo Recherche" style="width: 20px; height: 20px;" />
            <img src={product.imageUrl} alt="produit" id="imageProduit"/>
            <div class="container">
              <div class="item item1">{product.titre}</div>
              <div class="item item5">{product.prix}€</div>
              <div class="item item6">
                <img src="src\img\Avis{Math.round(product.note)}.png" alt="produit" /></div>             
            </div>
          </div>
        {/each}
      </div>
      {:else}
      <div class="panier-vide">
        <div>
          <p>Vous n'avez aucune annonce.</p>
        </div>
        <div>
          <button on:click={() => window.location.href = "../vendeur"}>Créer une annonce</button>
        </div>
       <div>
        <img src="src/img/Paniervide.jpg" alt="Image vide" />
       </div>
      </div>
       {/if}
    </section>
   {/if}
  </main>
  