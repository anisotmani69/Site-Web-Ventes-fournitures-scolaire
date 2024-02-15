<script>
    let id_marque = 0;
    let id_categorie = 0;
    let id_type = 2;
    let id_couleur = 0;
    let titre = "";
    let description = "";
    let prix = 0;
    let image = "";
    let user = [];
    let images = "";

    let file = null;
    let fileTmp = "";


    const creation = async () => {
        if (!checkValues()){
            return;
        }
        user = JSON.parse(localStorage.getItem("user"));
        console.log("test", user);
        id_categorie = parseInt(
            document.getElementById("product-category").value,
            10,
        );
        id_couleur = parseInt(
            document.getElementById("product-couleur").value,
            10,
        );
        images = image.replace(/\..+$/, "");
        image = image.split("\\").pop();
        fileTmp = file.name.replace(/\..+$/, "");
        console.log(fileTmp);
        const data = {
            id_marque: id_marque,
            id_categorie: id_categorie,
            id_vendeur: user.id,
            id_type: id_type,
            id_couleur: id_couleur,
            titre: titre,
            description: description,
            prix: prix,
            image: fileTmp,
        };
        console.log(data);
        const response = await fetch("http://127.0.0.1:8000/createarticle", {
            method: "POST",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            uploadImage();
            window.location.href="../annonce";
        } else {
            console.log("ça marche pas");
            const errorData = await response.json();
            console.error(
                "Erreur lors de la requête :",
                response.status,
                response.statusText,
                errorData,
            );
 /*            if (errorData.detail === "L'email n'est pas dans un format valide"){
        document.querySelector("#mailformaterr").classList.remove("invisible");
      } */
        }

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
    };

    function handleFileChange(event) {
        file = event.target.files[0];
    }

    function checkValues(){
    let res = true;
    if (!file){
        res = false;
        document.querySelector("#imgerr").classList.remove("invisible");
    }
    if ( document.getElementById("product-name").value === ""){
      res = false;
      document.querySelector("#nomerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#nomerr").classList.add("invisible");
    }
    if ( document.getElementById("product-price").value === ""){
      res = false;
      document.querySelector("#prixerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#prixerr").classList.add("invisible");
    }
    if ( document.getElementById("product-description").value === ""){
      res = false;
      document.querySelector("#descriptionerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#descriptionerr").classList.add("invisible");
    }
    if ( document.getElementById("product-brand").value === ""){
      res = false;
      document.querySelector("#marqueerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#marqueerr").classList.add("invisible");
    }
    if ( document.getElementById("product-couleur").value === ""){
      res = false;
      document.querySelector("#couleurerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#couleurerr").classList.add("invisible");
    }
    if ( document.getElementById("product-category").value === ""){
      res = false;
      document.querySelector("#categorieerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#categorieerr").classList.add("invisible");
    }
    return res;
  }
</script>

<body>
    <p>Nouvelle annonce</p>
    <div class="container">
        <form
            action="/submit-annonce"
            method="post"
            enctype="multipart/form-data"
        >
            <input
                type="file"
                id="product-photo"
                name="product-photo"
                accept=".png"
                on:change={handleFileChange}
            />
            <p class="invisible erreur" id="imgerr">Ce champ est obligatoire</p>
            <div class="form-group">
                <label for="product-name">Nom du produit:</label>
                <input
                    bind:value={titre}
                    type="text"
                    id="product-name"
                    name="product-name"
                />
                <p class="invisible erreur" id="nomerr">Ce champ est obligatoire</p>
            </div>
            <div class="form-group">
                <label for="product-brand">Marque du produit:</label>
                <select
                    bind:value={id_marque}
                    type="number"
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
            <p class="invisible erreur" id="marqueerr">Ce champ est obligatoire</p>
            </div>
            <div class="form-group">
                <label for="product-price">Prix du produit:</label>
                <input
                    bind:value={prix}
                    type="number"
                    id="product-price"
                    name="product-price"
                />
                <p class="invisible erreur" id="prixerr">Ce champ est obligatoire</p>
            </div>
            <div class="form-group">
                <label for="product-category">Catégorie du produit:</label>
                <select
                    bind:value={id_categorie}
                    id="product-category"
                    name="product-category"
                >
                    <option value="1">Stylo</option>
                    <option value="2">Règle</option>
                    <option value="3">Ciseaux</option>
                    <option value="4">Crayon</option>
                    <option value="5">Gomme</option>
                    <option value="6">Taille-crayon</option>
                    <option value="7">Cahier</option>
                    <option value="8">Portes-vues</option>
                    <option value="9">Trousse</option>
                    <option value="10">Cartable</option>
                </select>
                <p class="invisible erreur" id="categorieerr">Ce champ est obligatoire</p>
            </div>
            <div class="form-group">
                <label for="product-couleur">Couleur du produit:</label>
                <select
                    bind:value={id_couleur}
                    id="product-couleur"
                    name="product-category"
                >
                    <option value="1">Rouge</option>
                    <option value="2">Bleu</option>
                    <option value="3">Noir</option>
                </select>
                <p class="invisible erreur" id="couleurerr">Ce champ est obligatoire</p>
            </div>
            <div class="form-group">
                <label for="product-description">Description du produit:</label>
                <textarea
                    bind:value={description}
                    type="text"
                    id="product-description"
                    name="product-price"
                ></textarea>
                <p class="invisible erreur" id="descriptionerr">Ce champ est obligatoire</p>
            </div>
            <div class="form-group">
                <button type="reset">Annuler</button>
                <button type="button" on:click={creation}>Valider</button>
            </div>
        </form>
    </div>
</body>

<style>
    #imgerr {
        align-self: left;
        margin-top: -10px;
        margin-bottom: 10px;
        margin-left: -50%;
    }
    select, input[type="text"], textarea {
        width: 200px;
        border-radius: 5px;
    }
    .invisible {
  display: none;
  } 

  p.erreur {
    color: red;
    margin: 0px;
    font-size: 12px;
    margin-left: 0px;
  }
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
        width: 500px;
        place-items: center; 
        margin-bottom: 50px;
    }

    .form-group label {
        white-space: nowrap;
    }

    .form-group button {
        padding: 20px;
        width: 150px;
        color: white;
        border: none;
        cursor: pointer;
        border-radius: 20px;
        height: 30px;
        text-align: center;
    }

    button[type="button"] {
        background-color: #ffb13c;
    }

    button[type="reset"] {
        color: #ffb13c;
        border: 1px solid #ffb13c;
        background-color: #faf5f0;
    }
    button {
        border: none;
        border-radius: 6px;
        height: 30px;
        width: 150px;
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

    input[type="text"] {
        border: 1px solid black;
    }

    input[type="number"] {
        border-radius: 5px;
        width: 200px;
        border: 1px solid black;
    }

    p {
        color: #ffb13c;
        font-size: 40px;
        margin-top: 0px;
        text-align: center;
    }

    select[id="product-category"] {
        border-radius: 5px;
    }

    select[id="product-couleur"] {
        border-radius: 5px;
    }

    textarea[id="product-description"] {
        border-radius: 10px;
        height: 50px;
        border-radius: 5px;
        border: 1px solid black;
    }
    #product-photo {
        margin-bottom: 15px;
    }
    label {
        font-size: 14px;
    }
</style>
