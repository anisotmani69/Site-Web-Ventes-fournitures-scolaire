<script>
   
    let username = "";
    let password = "";
   

    const login = async () => {
    
    if (checkValues()){
    const formData = new FormData();
    formData.append("username", document.getElementById("username").value);
    formData.append("password", document.getElementById("password").value);

    try {
        const response = await fetch("http://127.0.0.1:8000/token", {
            method: "POST",
            mode: "cors",
            headers: {
                Accept: "application/json",
            },
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            window.localStorage.setItem("token", data.access_token);           
           window.location.href="../../annonce";
            console.log("ça marche");
        } else {
            console.error("La requête a échoué");
            document.querySelector("#incorrect").classList.remove("invisible")
        }
    } catch (e) {
        console.error(e);
    }}
};

function checkValues(){
    let res = true;
    if ( document.getElementById("username").value === ""){
      res = false;
      document.querySelector("#iderr").classList.remove("invisible");
    }
    else {
      document.querySelector("#iderr").classList.add("invisible");
    }
    if ( document.getElementById("password").value === ""){
      res = false;
      document.querySelector("#pswerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#pswerr").classList.add("invisible");
    }
    return res;
  }

</script>

<main>
    <section class="container">
        <div class="social-login">
            <h2>Bonjour !</h2>
            <p>Connectez-vous pour acceder a vos articles</p>
        </div>
        <form class="login-form">
            <label for="username">Nom d'utilisateur</label>
            <input
                bind:value={username}
                type="username"
                id="username"
                name="username"
                required
            />
            <p class="invisible erreur" id="iderr">Ce champ est obligatoire</p>
            <label for="password">Mot de passe</label>
            <input
                bind:value={password}
                type="password"
                id="password"
                name="password"
                required
            />
            <p class="invisible erreur" id="pswerr">Ce champ est obligatoire</p>
        </form>
        <div class="button-container">
            <button type="button" on:click={login}>Valider</button>
             
        </div>
        <p class="invisible erreur" id="incorrect">L'identifiant ou le mot de passe est incorrect ou vous ne pouvez pas vous connecter en tant que vendeur</p> 
        <div class="creation">
            <p>Pas encore de compte ?</p>
            <a href="/connexion/fournisseur/connexion">
                <p>Créer un compte</p>
            </a>
        </div>
    </section>
</main>

<style>
    #incorrect {
    margin-top:1px;
    justify-self: center;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
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
  
    .social-login{
        margin-bottom: 30px;
    }

    .creation{
        font-size: 100px;
    }

    main {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: white;
        height: 100vh; 
        font-size: 18px;
        background-color: #FAF5F0;
    }

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        border: 2px solid #ddd; 
        border-radius: 10px; 
        padding: 30px; 
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
        height: 420px;
        width: 450px;
        background-color: white;
    }

    button {
        background-color: orange;
        border-radius: 7px;
        width:400px ;
        height: 30px;
        border: none;
        transition: background-color 0.3s;
        cursor: pointer;
    }

    button:hover {
    background-color: #feb52f; 
  }

    label {
        display: block;
        text-align: left;
        color: black;
        margin-bottom: 10px;
    }

    label:hover {
        border-color: black; 
    }

    input[type="username"],
    input[type="password"] {
        border-radius: 10px;
        background-color: white;
        width:400px ;
        height: 30px;
        margin-bottom: 10px; 
        border: 1px solid #ccc; 
        cursor: pointer;
       
        transition: border-color 0.3s; 
    }

    input[type="username"]:hover,
    input[type="password"]:hover {
        border-color: black; 
    }

    .button-container {
        margin-top: 25px; 
    }

    .creation {
        display: flex;
        align-items: center;
        white-space: nowrap;
        font-size: 14px;
    }
</style>
