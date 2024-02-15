<script>
	import { onMount } from 'svelte';
	import Item from "../composants/Item_avis.svelte";
    import Chargement from "../composants/Chargement.svelte";
	import { afterUpdate } from 'svelte';

	let countPanier = 1;
	let countTrousse = 1;
    let nbarticle = 0;
    let selectedOption = 1;
	function handleClickPlusPanier(){		
		countPanier++;
	}
	function handleClickMoinsPanier(){
		if (countPanier>0){ 
			countPanier--;}
	}
	function handleClickPlusTrousse(){		
		countTrousse++;
	}
	function handleClickMoinsTrousse(){		
		if (countTrousse>0){
			countTrousse--;
		}
	}
	function updateCountPanier(e){
		countPanier = e.target.value;
	}
	function updateCountTrousse(e){
		countTrousse = e.target.value;
	}
	function laisserAvis(){
		window.location.href = "./laisser_avis";
	}
	function incrementerAvis(){
		countAvis=countAvis+3;
	}

	
	let titreProduit = "re";
	let avis;
	let productId = 0;
	let aviss = []
	let countAvis = 3;
	let marque = "BIC";
	let reference = "XXXXX-XXXX";
	let prix = "2€";
    let description = "";
	let imageProduit = "";
	let productType = 0;
	let categorie = "";
    let articles = [];
	let produits = [];
    let trousseFound = [];
    let id;
    let user;
    let token = [];
    let loaded = false;
    let tableauAvisTriDate = [];

  onMount(async () => {
    setTimeout(() => {
      loaded = true;
    }, 100);
    user = JSON.parse(localStorage.getItem("user"));
    console.log("user", user.id);
	let selectedProduct;
	const storedProductString = localStorage.getItem("selectedProduct");

	if (storedProductString) {
 		 selectedProduct = JSON.parse(storedProductString);
  		console.log("Données du produit récupérées :", selectedProduct);
 		 console.log("titre :",selectedProduct[0].titre );
 		titreProduit = selectedProduct[0].titre;
		 marque = selectedProduct[0].marque.nom;
 		prix = selectedProduct[0].prix;
		 productType = selectedProduct[0].type.id;
		productId = selectedProduct[0].id;
		avis =  selectedProduct[0].note;
		aviss = selectedProduct[0].avis.reverse();
        tableauAvisTriDate = aviss;
        id = selectedProduct[0].id;
		categorie = selectedProduct[0].categorie.id;
        imageProduit = selectedProduct[0].image;
        description = selectedProduct[0].description;
        
	} else {
  		console.log("Aucune donnée de produit trouvée dans le stockage local.");
	}

    addHisto();

    

    const imageResponse = await fetch(`http://127.0.0.1:8000/image?filename=${imageProduit}`, {
            method: "GET",
             mode: "cors",
             headers: {
                 Accept: "application/json",
             },
         });
          
          if (imageResponse.ok) {
            const imageData = await imageResponse.blob();
            imageProduit = URL.createObjectURL(imageData);
          } else {
            console.error(`Erreur lors de la récupération de l'image pour le produit :`, imageResponse.status);
          }

   

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
             console.log("produits", produits)
             if(produits.length === 0){
               console.log("le panier est vide");
               
             }
 
             const allProducts = produits.reduce(async (accPromise, product) => {
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
         } else {
             console.error("Erreur lors de la récupération du panier :", response.statusText);
         }
         


         articles.forEach((product) => {
  if (product[0].categorie.id == 9 ) {
    trousseFound = 1;
  }
  
});
console.log("yg",trousseFound);


  });

  async function addHisto(){
    token = window.localStorage.getItem("token");
     console.log("Token:", token);

     
     const datas = {
                    id_utilisateur: user.id,
                    id_article: id,              
                };
                console.log("data", datas)
                try {
      
      const responses =  fetch(`http://127.0.0.1:8000/histo`, {
        method: "POST",
        mode: "cors",
        headers: {
          Accept: "application/json",
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(datas),
      });

      if (responses.ok) {
        const results =  responses.json();
        console.log("Produit modifié a l'historique :", results);
      }
    } catch (e) {
      console.error("Erreur lors de la requête de modification au panier :", e);
    }

  }


  async function addToCart(productId, productType) {
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);
    nbarticle = countPanier;

    if (!token) {
        console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
        const emplacementActuel = encodeURIComponent(window.location.pathname);
        window.location.href = `../connexion?retour=${emplacementActuel}`;
        return;
    }

    try {
        const checkResponse = await fetch("http://127.0.0.1:8000/panier?type_id=0", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (checkResponse.ok) {
            const existingProducts = await checkResponse.json();
            const existingProduct = existingProducts.find((product) => product.id_article === productId);

            if (existingProduct) {
        
                const updatedResponse = await fetch(`http://127.0.0.1:8000/panier?id_article=${existingProduct.id_article}&nb_article=${existingProduct.nb_article + countPanier}`, {
                    method: "PUT",
                    mode: "cors",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (updatedResponse.ok) {
                    console.log("Panier mis à jour avec succès.");
					ouvrirFenetre();
                } else {
                    console.error("Erreur lors de la mise à jour du panier :", updatedResponse.statusText);
                }
            } else {
                const data = {
                    id_article: productId,
                    type: 0,
                    nb_article: countPanier,  
                    datePanier : "14/01/2024",              
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
					ouvrirFenetre();
					
                } else {
                    console.error("Erreur lors de l'ajout au panier :", response.statusText);
                }
            }
        } else {
            console.error("Erreur lors de la vérification du panier :", checkResponse.statusText);
        }
    } catch (e) {
        console.error("Erreur lors de la requête d'ajout au panier :", e);
    }
}

async function addToCartable(productId, productType) {
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);
    nbarticle = countTrousse;

    if (!token) {
        console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
        const emplacementActuel = encodeURIComponent(window.location.pathname);
        window.location.href = `../connexion?retour=${emplacementActuel}`;
        return;
    }

    try {
        const checkResponse = await fetch("http://127.0.0.1:8000/panier?type_id=1", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (checkResponse.ok) {
            const existingProducts = await checkResponse.json();
            const existingProduct = existingProducts.find((product) => product.id_article === productId);

            if (existingProduct) {
        
                const updatedResponse = await fetch(`http://127.0.0.1:8000/panier?id_article=${existingProduct.id_article}&nb_article=${existingProduct.nb_article + countTrousse}`, {
                    method: "PUT",
                    mode: "cors",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (updatedResponse.ok) {
					const resultat = await updatedResponse.json();
                    console.log("Panier mis à jour avec succès.", resultat);
                    ouvrirFenetreCartable("Cartable");
                } else {
                    console.error("Erreur lors de la mise à jour du panier :", updatedResponse.statusText);
                }
            } else {
                const data = {
                    id_article: productId,
                    type: 1,
                    nb_article: countTrousse,
                    datePanier : "14/01/2024",
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
					ouvrirFenetre();
					
                } else {
                    console.error("Erreur lors de l'ajout au panier :", response.statusText);
                }
            }
        } else {
            console.error("Erreur lors de la vérification du panier :", checkResponse.statusText);
        }
    } catch (e) {
        console.error("Erreur lors de la requête d'ajout au panier :", e);
    }
}

async function addToTrousse(productId, productType) {
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);
    nbarticle = countTrousse;

    if (!token) {
        console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
        const emplacementActuel = encodeURIComponent(window.location.pathname);
        window.location.href = `../connexion?retour=${emplacementActuel}`;
        return;
    }

    try {
        const checkResponse = await fetch("http://127.0.0.1:8000/panier?type_id=2", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (checkResponse.ok) {
            const existingProducts = await checkResponse.json();
            const existingProduct = existingProducts.find((product) => product.id_article === productId);

            if (existingProduct) {
        
                const updatedResponse = await fetch(`http://127.0.0.1:8000/panier?id_article=${existingProduct.id_article}&nb_article=${existingProduct.nb_article + countTrousse}`, {
                    method: "PUT",
                    mode: "cors",
                    headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (updatedResponse.ok) {
					const resultat = await updatedResponse.json();
                    console.log("Panier mis à jour avec succès.", resultat);
                    ouvrirFenetreCartable("Trousse");
                } else {
                    console.error("Erreur lors de la mise à jour du panier :", updatedResponse.statusText);
                }
            } else {
                const data = {
                    id_article: productId,
                    type: 2,
                    nb_article: countTrousse,
                    datePanier : "14/01/2024",
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
					ouvrirFenetre();
					
                } else {
                    console.error("Erreur lors de l'ajout au panier :", response.statusText);
                }
            }
        } else {
            console.error("Erreur lors de la vérification du panier :", checkResponse.statusText);
        }
    } catch (e) {
        console.error("Erreur lors de la requête d'ajout au panier :", e);
    }
}


function ouvrirFenetre() {
    var overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '139.5px';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = '999'; 

    var main = document.querySelector('main');

    var fenetre = document.createElement('div');
    fenetre.className = 'fenetre';
    fenetre.style.position = 'fixed';
    fenetre.style.top = '36.2%';
    fenetre.style.right = '30%';
    fenetre.style.transform = 'translate(-50%, -50%)';
    fenetre.style.backgroundColor = '#fff';
    fenetre.style.border = '1px solid #ccc';
   
    fenetre.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
    fenetre.style.zIndex = '1000';
    fenetre.style.width = '400px';
    fenetre.style.height = '250px';

    fenetre.innerHTML = `
   <div style="display: flex; margin-botton : 0px;">
    <img src="../../src/img/validation.png" alt="Image produit" style="max-width: 18px; height: 18px; margin-right: 10px; margin-top: 8px;">
    <p style="margin-right: 10px; padding: none;">Ajouté au panier</p>
    <img src="../../src/img/cancel.png" alt="Image produit" id= "croix" style="max-width: 20px; height: 20px; margin-left: auto; margin-top: 6px; margin-right : 15px; cursor: pointer;">
</div>
   
        <div id="display" style="display: flex; align-items: center;">
            <img src="${imageProduit}" alt="Image produit" style="width: 150px; height: 150px; margin-right: 10px;">
            <div>
                <strong>${titreProduit}</strong>
                <br>Qté : ${nbarticle}<br>
                <br>Prix : ${prix * nbarticle}<br>
               
            </div>
            
        </div>
        <div class="links">
                    <a href="../panier" class="link" >Aller au panier</a>
                    <a href="../pageproduits" class="link" >Continuer mes achats</a>
                </div>
        <style>
            img[alt = "Image produit"]{
                width: 130px;
                height: 130px
            }    

            #display{
                margin-top:20px;
            }

          

        .links {
            
          display: flex;
          justify-content: space-around;
          height : 30px;
          align-item : center;
         
          
        }
        .link {
          padding : 10px;
          border : 1px solid #000;
          color: #000;
          text-decoration: none;
          border-radius: 5px;
        }

            
        </style>
    `;

    main.appendChild(overlay);
    main.appendChild(fenetre);
    window.scrollTo(0, 0);

    
    overlay.addEventListener('click', function() {
        main.removeChild(overlay);
        main.removeChild(fenetre);
    });


var votreImage = document.getElementById('croix');


votreImage.addEventListener('click', function() {
    main.removeChild(overlay);
    main.removeChild(fenetre);
});


    setTimeout(function() {
        main.removeChild(overlay);
        main.removeChild(fenetre);
    }, 5000);
}

function ouvrirFenetreCartable(type) {
    var overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '139.5px';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = '999'; 

    var main = document.querySelector('main');

    var fenetre = document.createElement('div');
    fenetre.className = 'fenetre';
    fenetre.style.position = 'fixed';
    fenetre.style.top = '36.2%';
    fenetre.style.right = '30%';
    fenetre.style.transform = 'translate(-50%, -50%)';
    fenetre.style.backgroundColor = '#fff';
    fenetre.style.border = '1px solid #ccc';
   
    fenetre.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
    fenetre.style.zIndex = '1000';
    fenetre.style.width = '400px';
    fenetre.style.height = '250px';

    fenetre.innerHTML = `
   <div style="display: flex; margin-botton : 0px;">
    <img src="../../src/img/cancel.png" alt="Image produit" id= "croix" style="max-width: 20px; height: 20px; margin-left: auto; margin-top: 6px; margin-right : 15px; cursor: pointer;">
   
</div>
<h2 style="margin-left: 30px;">Votre produit a été ajouté au ${type} !</h2>
   
        
       
        <style>
            img[alt = "Image produit"]{
                width: 130px;
                height: 130px
            }    

            #display{
                margin-top:20px;
            }

            
        </style>
    `;

    main.appendChild(overlay);
    main.appendChild(fenetre);
    window.scrollTo(0, 0);

    
    overlay.addEventListener('click', function() {
        main.removeChild(overlay);
        main.removeChild(fenetre);
    });


var votreImage = document.getElementById('croix');


votreImage.addEventListener('click', function() {
    main.removeChild(overlay);
    main.removeChild(fenetre);
});


    setTimeout(function() {
        main.removeChild(overlay);
        main.removeChild(fenetre);
    }, 5000);
}

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


   let etoile;
    let fav = false;

    async function supprimerFav(){
        const id_article = JSON.parse((localStorage.getItem("selectedProduct")))[0].id;
        const token = window.localStorage.getItem("token");
        console.log("Token:", token);

    if (!token) {
        console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
        return;
    }

    try {
      console.log(id_article);
      const response = await fetch(`http://127.0.0.1:8000/panier?article_id=${id_article}&type_id=3`, {
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
    

    async function ajouterFav(){
        const id_article = JSON.parse((localStorage.getItem("selectedProduct")))[0].id;
        const token = window.localStorage.getItem("token");
        console.log("Token:", token);

        if (!token) {
            console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
            const emplacementActuel = encodeURIComponent(window.location.pathname);
            window.location.href = `../connexion?retour=${emplacementActuel}`;
            return;
        }

    try {
        const checkResponse = await fetch("http://127.0.0.1:8000/panier?type_id=3", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (checkResponse.ok) {
            const existingProducts = await checkResponse.json();
            const existingProduct = existingProducts.find((product) => product.id_article === id_article);

            if (!existingProduct) { 
                const data = {
                    id_article: id_article,
                    type: 3,
                    nb_article: 1,
                    datePanier : getDate(),
                };
                console.log("data envoyé : "+JSON.stringify(data));

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
                    console.log("data reçu : ", result);
					
                } else {
                    console.error("Erreur lors de l'ajout au panier :", response.statusText);
                }
            }
        } else {
            console.error("Erreur lors de la vérification du panier :", checkResponse.statusText);
        }
    } catch (e) {
        console.error("Erreur lors de la requête d'ajout au panier :", e);
    }
}
    

    function clicEtoile(){
        if (fav){
            fav = false;
            etoile.src="src/img/heart_no.png";
            supprimerFav();
        }
        else{
            fav = true;
            etoile.src="src/img/heart_yes.png";
            ajouterFav();
        }
    }

    function hoverEtoile(){
        etoile.src="src/img/heart_hover.png"
    }

    function outEtoile(){
        if (fav === true){
            etoile.src="src/img/heart_yes.png";
        }
        else{
            etoile.src="src/img/heart_no.png";
        }
    }
    
    function choixChange() {
    
    selectedOption = document.getElementById('tri-category').value;
    console.log("avis", aviss.note);
     if (selectedOption === '1') {
         aviss = tableauAvisTriDate;
     } else if (selectedOption === '2') {
         aviss = [...aviss].sort((a, b) => b.note - a.note);
       }
       else if (selectedOption === '3') {
         aviss = [...aviss].sort((a, b) => a.note - b.note);
       }
   }

</script>

<main>
    {#if !loaded}
    <Chargement />
  {:else}
	<body>
        {#if token}
            <div id="fav">
                <img bind:this={etoile} on:click={clicEtoile} on:mouseover={hoverEtoile} on:mouseout={outEtoile} id = "etoile" src="src/img/heart_no.png" alt="etoile">
            </div>
        {/if}
		<div id="central_col">
		    <div     id="product">
                <div id="left">
                    <img src={imageProduit} id="photo_produit" alt="photo_stylo">
                </div>

		        <div class = "infos">
			        <p   id="titre_produit">{titreProduit}</p>
			        <div     id="variables">
                        <p class="var">Marque</p>
                        <p class="var">{marque}</p>
                        <p class="var">Référence</p>
                        <p class="var">{reference}</p>
                        <p class="var">Prix</p>
                        <p   id="prix">{prix} €</p>
                        <p class="var">Note globale</p>
                        <img src="src/img/Avis{Math.round(avis)}.png" alt="Note" id="noteProduit">
                        <p class="var">Description</p>
                        <p class="var">{description}</p>
						<div class = "compteurs">
							<button class="moins" on:click={handleClickMoinsPanier}>-</button>
							<input type="number" class="cpt" value={countPanier} on:change={updateCountPanier}>
							<button class="plus" on:click={handleClickPlusPanier}>+</button></div>
                        <button class="ajout" on:click={() => addToCart(productId, productType)}>Ajouter au panier</button>

						
						<div class = "compteurs">
							<button class="moins" on:click={handleClickMoinsTrousse}>-</button>
							<input type="number" class="cpt" value={countTrousse} on:change={updateCountTrousse}>
							<button class="plus" on:click={handleClickPlusTrousse}>+</button></div>
							{#if categorie < 7}
                        <button class="ajout" on:click={() => addToTrousse(productId, productType)}>Ajouter à la trousse</button>
						{:else if  categorie == 9}
						<button class="ajout" on:click={() => addToTrousse(productId, productType)}>Creer ma trousse</button>
                        {:else if categorie == 10}
                        <button class="ajout" on:click={() => addToCartable(productId, productType)}>Creer mon cartable</button>
                        {:else}
                        <button class="ajout" on:click={() => addToCartable(productId, productType)}>Ajouter a mon cartable</button>
						{/if}
			      		  </div>
							
			
		        </div>
		    </div>
            <div id="enteteAvis">
                <div id=avis_title>
                    <p id="avis_texte">Avis</p>
                </div>
                <select  id="tri-category" name="tri-category"  on:change={choixChange}>
                    <option value="1">Les plus récents</option>
                    <option value="2">Tri par note décroissant</option>
                    <option value="3">Tri par note croissant</option>
                </select>
            </div>
            
            
						
			{#if aviss.length > 0}
				{#each aviss.slice(0, countAvis) as { text, note, dateAvis }}
					<Item commentaire={text} note={note} date={dateAvis}/>
					<hr style="margin: 10px 0; border-top: 2px solid orange;">
				{/each}
			{:else}
				<p>Soyez le premier à donner votre avis</p>
			{/if}
			
		    <div id="buttons">
                
                <button class="but_avis" on:click={incrementerAvis}>Afficher plus</button>
                {#if token}
                <button class="but_avis" on:click={laisserAvis}>Laisser un avis</button>
                {/if}
            </div>
        </div>
	</body>
{/if}
</main>

<style>
    #buttons{
        margin-bottom: 50px;
    }
    #left {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    #fav {
        position: absolute;
        top: 20px;
        right: 20px;
    }
	#noteProduit{
		justify-self: left;
		align-self: center;
	}
	.compteurs{
		display:flex;
		align-items: center;
		min-width: 100%;
	}
	.plus{
		background-color: orange;
		border-top-right-radius: 15px;
		border-bottom-right-radius: 15px;
		height:50px;
		width: 54px;
		border: none;
		font-size: 40px;
		padding: none;
		margin:none;
	}
	.moins{
		background-color: orange;
		border-top-left-radius: 15px;
		border-bottom-left-radius: 15px;
		height:50px;
		width: 54px;
		border:none;
		font-size: 40px;
		padding: none;
		margin:none;
	}
	#central_col{
		width:70%;
		justify-self: center;
	}
	#photo_produit{
		border-radius:10px;
		max-width:80%;
        max-height: 500px;
        height: auto;
        width: 80%;
        margin: 10%;
        margin-top: 10%;
        margin-right: 15%;
	}
    button, select {
        transition: background-color 0.3s;
    }
	button:hover, select:hover{
        background-color: #feb52f;
	}
	
	main{
		background-color : #FAF5F0;
        min-height: 100vh;
	}
    #enteteAvis {
        display: flex;
        margin-top: 30px;
    }
	#avis_title{
		background-color:orange;
		border-radius:15px;
		font-size:30px;
		width:98%;
        height:50px;
        display : flex;
        align-items: center;
        margin-right: 0px;
	}
    select {
        width: 47%;
        height: 50px;
        margin-left: 10px;
        background-color: orange;
        border-radius: 15px;
        border: none;
        padding: 10px;
        font-size: 25px;
        align-self: center;
    }
    option {
        font-size: 16px;
        padding: 2px;
        
    }
	#avis_texte{
		margin-left:30px;
	}
	.cpt{
		margin:none;
		width:80px;
		height:47px;
		font-size:25px;
		color:rgba(0,0,0,0.8);
		border-width:0.2px;
		padding: none;
		text-align: center;
	}
	.ajout{
		background-color:orange;
		height:50px;
		width:100%;
		border-radius:15px;
		border:none;
		font-size:25px;
		margin : 10px;
	}
	.but_avis{
		width:242px;
		height:50px;
		background-color:orange;
		border-radius: 15px;
		border:none;
		font-size:25px;
		margin : 10px;
	}
	#titre_produit{
		font-size:40px;
	}
	.var{
        font-size:25px;
		color:rgba(0,0,0,0.8)
	}
	#prix{
		color:orange;
		font-size:30px;
	}
	body{
        position: relative;
		margin: 0px;
		padding: 0px;
		display : grid;
        font-family :Arial, Helvetica, sans-serif;
	}
	.infos{
		
		justify-content : center;
	}
	#variables{
		display : grid;
		grid-template-columns : 1fr 2fr;
	}
	#product{
		display:grid;
		grid-template-columns:1fr 1fr;
	}
</style>
