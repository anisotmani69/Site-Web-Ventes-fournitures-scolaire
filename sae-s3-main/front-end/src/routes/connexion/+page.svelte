<script>
  import { onMount } from "svelte";
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
        const params = new URLSearchParams(window.location.search);
        const emplacementRetour = params.get("retour");

        if (emplacementRetour) {
          window.location.href = emplacementRetour;
        } else {
          window.location.href = "../";
          console.log("ça marche");
        }
      } else {
        console.error("La requête a échoué");
      }
    } catch (e) {
      console.error(e);
    }
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      console.log(
        "L'utilisateur n'est pas connecté. Redirection vers la page de connexion..."
      );
    }

    const responses = await fetch("http://127.0.0.1:8000/user/me/", {
      method: "GET",
      mode: "cors",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (responses.ok) {
      const datas = await responses.json();
      localStorage.setItem("user", JSON.stringify(datas));
      console.log(datas);
    }
    else{
      document.querySelector("#incorrect").classList.remove("invisible");
    }
  }
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
      <p>Connectez-vous pour découvrir toutes nos fonctionnalités</p>
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
      <p class="invisible erreur" id="incorrect">L'identifiant ou le mot de passe est incorrect</p>
    </div>
    <div class="creation">
      <div class="connexion">
        <p>Envie de nous rejoindre ?</p>
        <a href="/connexion/createAcount">
          <p>Créer un compte</p>
        </a>
      </div>
      <div class="connexion">
        <p>Vous êtes un vendeur ?</p>
        <a href="/connexion/fournisseur">
          <p>Connectez-vous !</p>
        </a>
      </div>
    </div>
  </section>
</main>

<style>
  #incorrect {
    margin-top:1px;
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
  .social-login {
    margin-bottom: 30px;
  }

  .connexion {
    display: flex;
  }
  .creation {
    font-size: 100px;
  }

  main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #FAF5F0;
    height: 100vh;
    font-size: 18px;
  }

  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    height: 440px;
    width: 450px;
    background-color: white;
  }

  button {
    background-color: orange;
    border-radius: 7px;
    width: 400px;
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
    width: 400px;
    height: 30px;
    border: 1px solid #ccc;
    cursor: pointer;
    margin-bottom: 10px;
    transition: border-color 0.3s;
  }



  input[type="username"]:hover,
  input[type="password"]:hover {
    border-color: black;
  }

  .button-container {
    margin-top: 15px;
    margin-bottom: 5px;
  }

  .creation {
    font-size: 14px;
  }
</style>
