<style>
     body {
        font-family: Arial, sans-serif;
        background-color: #faf5f0;
        font-size: 10px;
        display: grid;
        justify-content: center;
        margin: 0px;
        padding-top: 50px;
        padding-bottom: 50px; 
    }

    .container {
        padding: 60px;
        display: grid;
        border: 1px solid black;
        border-radius: 9px;
        margin-top: 0px;
        width: 400px;
        place-items: center; 
        margin-bottom: 50px;
    }

    .supp{
        display: grid;
        margin-top: 50px;
    }

    .form-group label {
        white-space: nowrap;
        
    }

    .form-group button {
        padding: 20px;
        width: 200px;
        color: white;
        border: none;
        cursor: pointer;
        border-radius: 20px;
        height: 30px;
        text-align: center;
    }

    button[type = "button"]{
        margin-left: 70px;
        background-color: #FFB13C;
        width: 250px;
        margin-top: 50px
    }

    
    button{
      border : none;
      border-radius : 6px;
      height: 30px;
      width: 300px;
      opacity: 1;
      transition: opacity 0.3s ease; 
      cursor: pointer;
     }

     button:hover {
      opacity: 0.8;
      }

  
      .form-group {
        margin-bottom: 20px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
    }

input[type = "text"]{
  
    border : 1px solid black;
}

input[type="number"] {
        border-radius: 5px;
        width: 200px;
        border: 1px solid black;
    }

p{
    color : #FFB13C;
    font-size: 40px;
    white-space: nowrap;
    text-align: center;
    margin-top: 0px;
}


select[id="product-category"]{
    width:200px ;
    border-radius: 5px;   
}

select[id="product-couleur"]{
    width:200px ;
    border-radius: 5px;   
}

input[id="product-description"]{
    border-radius: 10px;   
    height: 50px;
}

</style>

<script>
    import { onMount } from 'svelte';

     let id_marque= 0;
     let id_categorie= 0;
     let id_type =2;
     let id_couleur= 0;
     let titre= "";
     let description= "";
     let prix= 0;
    let image= "";
    let id=0;
    let user = [];
    let images = "";

    let file = null;
    let fileTmp = "";

    onMount(() => {
	let selectedProduct;
    user = JSON.parse(localStorage.getItem("user"));
	const storedProductString = localStorage.getItem("selectedProductVendeur");

	if (storedProductString) {
 		 selectedProduct = JSON.parse(storedProductString);
  		console.log("Données du produit récupérées :", selectedProduct);
 		 console.log("titre :",selectedProduct[0].titre );
         id = selectedProduct[0].id;
          titre = selectedProduct[0].titre;
          id_marque = selectedProduct[0].marque.nom;
 		prix = selectedProduct[0].prix;
		 id_categorie = selectedProduct[0].categorie.id;
         id_couleur = selectedProduct[0].couleur.id;
         description =  selectedProduct[0].description;
		
	} else {
  		console.log("Aucune donnée de produit trouvée dans le stockage local.");
	}
    
  });

  async function uploadImage() {
            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch("http://127.0.0.1:8000/image", {
                    method: "POST",
                    body: formData,
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log(data.message);
                } else {
                    console.error("Upload failed");
                    console.error(response);
                }
            } catch (error) {
                console.error(error);
            }
        }

        function handleFileChange(event) {
        file = event.target.files[0];
    }



    const modification = async () => {
         id_categorie = parseInt(document.getElementById("product-category").value, 10);
         id_couleur = parseInt(document.getElementById("product-couleur").value, 10);
         fileTmp = file.name.replace(/\..+$/, "");
        const data = {
            id_marque: id_marque,
      id_categorie:id_categorie,
      id_vendeur: user.id,
      id_type :id_type,
      id_couleur: id_couleur,
      titre: titre,
      description: description,
      prix: prix,
     image:fileTmp,
};

                console.log(data);

                const response = await fetch(`http://127.0.0.1:8000/article?article_id=${id}`, {
            method: "PATCH",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            uploadImage();
            window.location.href="../annonce";
        }
        else{
            console.log("ça marche pas");
            const errorData = await response.json();
    console.error("Erreur lors de la requête :", response.status, response.statusText, errorData);

        }
    };

  




</script>

<body>
    <p>Modifier votre annonce</p>
<div class="container">
    
    <form action="/submit-annonce" method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label for="product-photo">Photo du produit:</label>
            <input
            type="file"
            id="product-photo"
            name="product-photo"
            accept=".png"
            on:change={handleFileChange}
        />
        </div>
        <div class="form-group">
            <label for="product-name">Nom du produit:</label>
            <input bind:value={titre} type="text" id="product-name" name="product-name" >
        </div>
        <div class="form-group">
            <label for="product-brand">Marque du produit:</label>
            <select
                bind:value={id_marque}
                id="product-brand"
                name="product-brand"
            >
                <option value="1">Bic</option>
                <option value="2">Staedtler</option>
                <option value="3">Faber-Castell</option>
                <option value="4">Pilot</option>
                <option value="5">Crayola</option>
                <option value="6">Sharpie</option>
                <option value="7">Moleskine</option>
                <option value="8">Maped</option>
                <option value="9">Tombow</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="product-price">Prix du produit:</label>
            <input  bind:value={prix} type="number" id="product-price" name="product-price"  >
        </div>
        <div class="form-group">
            <label for="product-category">Catégorie du produit:</label>
            <select bind:value={id_categorie} id="product-category" name="product-category" >
                <option value=1>Stylo</option>
                <option value=2>Règle</option>
                <option value=3>Ciseaux</option>
                <option value=4>Crayon</option>
                <option value=5>Gomme</option>
                <option value=6>Taille-crayon</option>
                <option value=7>Cahier</option>
                <option value=8>Portes-vues</option>
                <option value=9>Trousse</option>
            </select>
        </div>
        <div class="form-group">
            <label for="product-couleur">Couleur du produit:</label>
            <select bind:value={id_couleur} id="product-couleur" name="product-category" >
                <option value=1>Rouge</option>
                <option value=2>Bleu</option>
                <option value=3>Noir</option>
            </select>
        </div>
        <div class="form-group">
            <label for="product-description">Description du produit:</label>
            <textarea
                bind:value={description}
                type="text"
                id="product-description"
                name="product-price"
            ></textarea>
        </div>
        <div class="form-group">
            <button type="button" on:click={modification}>Modifier mon annonce</button>         
        </div>
        
    </form>
</div>
</body>

