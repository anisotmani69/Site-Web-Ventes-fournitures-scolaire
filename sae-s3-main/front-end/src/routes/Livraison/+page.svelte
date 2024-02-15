<script>
    import Chargement from "../composants/Chargement.svelte";
    import { onMount } from 'svelte';
    let nomValue;
    let prenomValue;
    let infosSupValue;
    let adresseValue;
    let villeValue;
    let loaded = false;

    onMount(async () => {
    setTimeout(() => {
      loaded = true;
    }, 100);
});

    function valider(){
        if (checkValues()){

        let data = {"nomCommande": nomValue, "prenomCommande": prenomValue, "infosSupp": infosSupValue, "adresseLivraison": adresseValue, "nom_ville": villeValue};
        console.log(data);
        let dataString = JSON.stringify(data);
        console.log(dataString);
        localStorage.setItem("infosLivraison", dataString);

        window.location.href = "../Paiement";
    }
}
function annuler(){
        window.location.href = "../panier";
    }
function checkValues(){
    let res = true;
    if ( document.getElementById("nom").value === ""){
      res = false;
      document.querySelector("#nomerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#nomerr").classList.add("invisible");
    }
    if ( document.getElementById("prenom").value === ""){
      res = false;
      document.querySelector("#prenomerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#prenomerr").classList.add("invisible");
    }
    if ( document.getElementById("adresse").value === ""){
      res = false;
      document.querySelector("#adresseerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#adresseerr").classList.add("invisible");
    }
    if ( document.getElementById("ville").value === ""){
      res = false;
      document.querySelector("#villeerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#villeerr").classList.add("invisible");
    }
    return res;
  }
</script>

<body>
    {#if !loaded}
    <Chargement />
  {:else}
    
    
    <h1>Livraison</h1>
    <main>
        
        <div id="infos">
            <h2>Ajoutez une adresse</h2>
            <label for="nom">Nom</label>
            <input type="text" class="nom" id="nom" bind:value={nomValue} >
            <label for="prenom">Prenom</label>
            <input type="text" class="nom" id="prenom" bind:value={prenomValue}>
            <div id="champ">
            <p class="erreur invisible" id="nomerr">Ce champ est obligatoire</p>
            <p class="erreur invisible" id="prenomerr">Ce champ est obligatoire</p>
            </div>
            <label for="adresse">Adresse</label>
            <input type="text" class="adr" id="adresse" bind:value={adresseValue}>
            <p class="erreur invisible" id="adresseerr">Ce champ est obligatoire</p>
            <label for="infosSup">Infos supplémentaires</label>
            <input type="text" class="adr" id="infosSup" bind:value={infosSupValue}>
            <label for="prenom">Ville</label>
            <input type="text" class="adr"  id="ville" bind:value={villeValue}>
            <p class="erreur invisible" id="villeerr">Ce champ est obligatoire</p>
            <div class="buttons">
                <button id="annuler" on:click={annuler}>Annuler</button>
                <button id="valider" on:click={valider}>Enregistrer ces informations</button>
            </div>
            
            
        </div>
    </main>
    {/if}
</body>
<style>
    h1 {
        margin: 30px;
    }
    #prenomerr {
        margin-left: -10px;
    }
    #champ {
        display: grid;
        grid-template-columns: 1fr 1fr;
    }
 .invisible {
  display: none;
  } 

  p.erreur {
    color: red;
    margin: 0px;
    margin-top: -8px;
    font-size: 12px;
    margin-left: 5px;
  }
  
body {
    display: grid;
    background-color: #faf5f0;
    margin: 0px;
    justify-content: center;
}

#adresse {
    width: 87.25%;
}

#infosSup{
    width: 73%;
}

#ville {
    width: 91.5%;
}
label {
    font-size: 14px;
}

main {
    margin-top: 0px;
    background-color: #faf5f0;
    margin-bottom: 40px;
    border: 2px solid black;
    border-radius: 12px;
    width: 600px;
    padding: 15px;
}

input {
    border-radius: 10px;
    height: 30px;
    padding-left: 5px;
    margin: 5px;
    margin-top: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
}
input.nom {
    width: 39%;
}

input.adr {
    width: 97%;
}

.buttons {
    margin-top: 35px;
    display: flex;
    justify-content: space-around;
}


#valider {
    background-color:orange;
    border: 2px solid orange;
    border-radius:15px;
    font-size: 17px;
    transition: background-color 0.3s;
}

#annuler {
    border: 2px solid orange;
    background-color: #FAF5F0;
    color: orange;
    border-radius: 15px;
    font-size: 17px;
    padding: 8px;
}

#annuler:hover {
    border:3px solid orange;
}

#valider:hover {
    background-color: #feb52f;
}

button {
    width: 242px;
    height: 45px;
}
</style>