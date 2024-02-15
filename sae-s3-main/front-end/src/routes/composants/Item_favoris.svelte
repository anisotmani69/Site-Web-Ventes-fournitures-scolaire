<script>
    export let image;
    export let titre;
    export let prix;
	export let id;

    let etoile;
    let fav = true;

    async function supprimerFav(){
        
        const id_article = id;
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
        const id_article = id;
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
                    datePanier: "22/01/2024",
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



</script>

<body>
    <div id = "fav_produit">
        <img class = "imgproduit" src={image} alt="imgproduit">
        <div id = "infos">
            <p id = "titre">{titre}</p>
            <p id = "prix">{prix}€</p>
        </div>
        
   <img bind:this={etoile} on:click={clicEtoile} on:mouseover={hoverEtoile} on:mouseout={outEtoile} id = "etoile" src="src/img/heart_yes.png" alt="etoile">

    </div>

</body>

<style>
    body {
        margin: 0px;
    }
    .imgproduit{
        max-width: fit-content;
        max-height: 200px;
        border-radius: 10px;
        margin-right: 10px;
    }

    #fav_produit{
        display : grid;
        grid-template-columns: 2fr 5fr 1fr;
        padding : 10px;
        margin-top : 10px;
        background-color: #FFEEDD;
        border-radius: 10px;
        height : 200px;
        align-items : center;
        
    }

    p{
        font-family :Arial, Helvetica, sans-serif;
    }
    #titre{
        font-size: 25px;
        color: rgba(0,0,0,50%);
    }
    #prix{
        font-size: 30px;
        color: #5bc3eb;
    }
    #etoile{
        max-height:100%;
    }

</style>