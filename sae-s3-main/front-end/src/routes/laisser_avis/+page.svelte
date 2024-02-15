<script>
    import { onMount } from "svelte";

    let avisInput;
    let note;
    let user = [];
    let id_article = 0;
    let token;
    let avis = "";
    let selectedProduct;
    let imageProduit ;
    
    console.log(id_article)
    
    function ficheProduit(e){
        window.location.href = "./fiche_produit";
    }

    function defaultNoteImg(){
        var stars = document.getElementById("stars");
        if (stars.childElementCount===0){
            

            var aclique = false;
            for (let i = 0; i < 5; i++){
                let img = document.createElement("img");
                img.id = "star"+i;
                img.width = "23";
                img.height = "25";
                if (i === 0){
                    img.src = "src/img/star_yes.png";}
                else{
                    img.src = "src/img/star_no.png";}
                stars.appendChild(img);
            }
            note = 1;
            console.log("note = " + note)

            var tabstar = [];//initialise un tableau contenant les src de toutes les images de stars
            for (let i = 0; i < 5; i++){
                tabstar[i] = stars.getElementsByTagName("img")[i].src;
            }

            for(let i = 0; i < 5; i++){
                let img = stars.querySelectorAll("img")[i];
                img.addEventListener("click", ()=>{
                    let id=img.id;
                    let number = parseInt(id.charAt(id.length - 1), 10);
                    for(let j = 0; j<=number;j++){
                        stars.querySelectorAll("img")[j].src="src/img/star_yes.png";
                    }
                    for(let k = number+1; k<=4;k++){
                        stars.querySelectorAll("img")[k].src="src/img/star_no.png";
                    }
                    for (let m = 0; m < 5; m++){
                        tabstar[m] = stars.querySelectorAll("img")[m].src;
                    }
                    aclique = true;
                    note = number + 1;
                    console.log("note = " + note)
                });

                img.addEventListener("mouseover", ()=>{
                    let id=img.id;
                    let number=id.charAt(id.length - 1);
                    for(let j = 0; j<=number;j++){
                        stars.querySelectorAll("img")[j].src="src/img/star_hover.png";
                    }
                });

                img.addEventListener("mouseout", ()=>{
                    if (aclique === true){
                        aclique = false;
                    }
                    else{
                        for(let n=0;n<5;n++){
                            stars.querySelectorAll("img")[n].src=tabstar[n];
                        }
                    }
                });
            }
        }
    }

    onMount(async () => {
        defaultNoteImg();
        user = JSON.parse(localStorage.getItem("user"));
        token = window.localStorage.getItem("token");
        console.log(token)
        id_article = JSON.parse((localStorage.getItem("selectedProduct")))[0].id;
        const storedProductString = localStorage.getItem("selectedProduct");

	if (storedProductString) {
 		 selectedProduct = JSON.parse(storedProductString);
  		console.log("Données du produit récupérées :", selectedProduct);
          const imageResponse = await fetch(`http://127.0.0.1:8000/image?filename=${selectedProduct[0].image}`, {
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
		
	} else {
  		console.log("Aucune donnée de produit trouvée dans le stockage local.");
	}

        /*const checkResponse = await fetch("http://127.0.0.1:8000/user/me/", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });
        if (checkResponse.ok) {
            id_utilisateur = await checkResponse.json();}
        else {
            console.error("Erreur lors de la vérification du panier :", checkResponse.statusText);
        }
    */});

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

    const sendAvis = async () => {
        const data = {
            id_utilisateur: user.id,
            id_article: id_article,
            note: note,
            text: avisInput,
            dateAvis: getDate(),
        };

        console.log(data)
            const response = await fetch("http://127.0.0.1:8000/avis", {
            method: "POST",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(data),
        });
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            console.log("ça a marché");
            selectedProduct[0].avis.push(data);
            localStorage.setItem("selectedProduct", JSON.stringify(selectedProduct));
            window.location.href = "./fiche_produit";
        }
        else{
            console.log("ça marche pas");
            const errorData = await response.json();
            console.error("Erreur lors de la requête :", response.status, response.statusText, errorData);
        }

    };

</script>
<body>
    <div class="gridcontainer">
        <img src={imageProduit} alt="image_produit" id="photo_produit" >
        <div id="rightCol">
            <h1>Votre avis nous intéresse !</h1>
            <div id="note">
                <p id="note_label">Note du produit :</p>
                <div id="stars"></div>
            </div>
            <form id="msg">
                <p>Avis : </p>
                <textarea bind:value={avisInput}></textarea>
            </form>
        </div>
    </div>
    <div class="buttons">
        <button id="annuler" on:click={ficheProduit}>Annuler</button>
        <button id="valider" on:click={sendAvis}>Valider</button>
    </div>
</body>

<style>

    form {
        margin-bottom: 0px;
    }
    #stars{
        align-self: center;
    }
    h1{
        font-size: 40px;
        font-weight: normal;
        margin-bottom: 20px;
    }
    #valider{
        border: none;
        background-color: orange;
        margin-left: 15%;
    }
    #valider:hover{
        background-color: #feb52f;
    }
    #annuler{
        border: 2px solid orange;
        font-weight:300;
        background-color: #FAF5F0;
        color: orange;
        margin-right: 15%;
    }
    #annuler:hover{
        border:3px solid orange;
    }
    #photo_produit{
		border-radius:10px;
		justify-self: right;
        margin-right: 10%;
        margin-left: 20%;
		align-self: center;
        width: 60%;
        height: auto;
        max-height: 60%
	}
    button:hover{
        border : 0.5px solid black;
        font-size: 25px;
    }
    button{
        width:75%;
        max-width: 242px;
        height: 57px;
        border-radius: 15px;
        font-size: 25px;
        margin-top: 20px;
        transition: background-color 0.3s;
    }
    textarea {
    height: 208px;
    width: 500px;
    border-radius: 15px;
    border: 0.5px solid black;
    font-size: 25px;
    line-height: 1;
    text-align: left;
    padding: 10px;
    }

    #note{
        display:grid;
        grid-template-columns: 1fr 1fr;
    }
    body{
        margin: 0px;
        font-family :Arial, Helvetica, sans-serif;
        width:100%;
        font-size: 25px;
        background-color : #FAF5F0;
        min-height: 100vh;
    }
    .gridcontainer {
        display:grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto;
    }
    .buttons {
        margin-top: 80px;
        display: flex;
        justify-content: center;
    }
    #rightCol {
        margin-left: 10%;
    }
</style>