<script>
    let username = "";
    let password = "";
    let email = "";
    const signup = async () => {
      if (checkValues()){
      event.preventDefault();
      const formData = new FormData();
      formData.append("username", document.getElementById("username").value);
      formData.append("password", document.getElementById("password").value);
  
      if (
        document.getElementById("password").value !==
        document.getElementById("passwordConfirm").value
      ) {
        document.querySelector("#pswcorres").classList.remove("invisible");
        return;
      }
  
      console.log(document.getElementById("username").value);
      const data = {
        nom_utilisateur: username,
        email: email,
        mot_de_passe: password,
      };
  
      const response = await fetch("http://127.0.0.1:8000/signup/vendeur", {
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
        window.location.href = "../fournisseur";
        console.log(data);
      } else {
        console.log("ça marche pas");
        const errorData = await response.json();
        console.error(
          "Erreur lors de la requête :",
          response.status,
          response.statusText,
          errorData
        );
        if (errorData.detail === "L'email n'est pas dans un format valide"){
        document.querySelector("#mailformaterr").classList.remove("invisible");
      }
      }}
    };

    function checkValues(){
    let res = true;
    document.querySelector("#mailformaterr").classList.add("invisible");
    document.querySelector("#pswcorres").classList.add("invisible");
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
    if ( document.getElementById("passwordConfirm").value === ""){
      res = false;
      document.querySelector("#psw2err").classList.remove("invisible");
    }
    else {
      document.querySelector("#psw2err").classList.add("invisible");
    }
    if ( document.getElementById("email").value === ""){
      res = false;
      document.querySelector("#mailerr").classList.remove("invisible");
    }
    else {
      document.querySelector("#mailerr").classList.add("invisible");
    }
    return res;
  }
  </script>
  
  <main>
    <section class="container">
      <div class="social-login">
        <h2>Bonjour !</h2>
        <p>Créer votre compte en tant que vendeur pour pouvoir vendre vos produits !</p>
      </div>
      <form>
        <label for="username">Nom d'utilisateur</label>
        <input
          bind:value={username}
          type="text"
          id="username"
          name="username"
          required
        />
        <p class="erreur invisible" id="iderr">Ce champ est obligatoire</p>
        <label for="password">Password</label>
        <input
          bind:value={password}
          type="password"
          id="password"
          name="password"
          required
        />
        <p class="erreur invisible" id="pswerr">Ce champ est obligatoire</p>
        <label for="passwordConfirm">Confirmation du password</label>
        <input
          type="password"
          id="passwordConfirm"
          name="passwordConfirm"
          required
        />
        <p class="erreur invisible" id="psw2err">Ce champ est obligatoire</p>
        <p class="erreur invisible" id="pswcorres">Les mots de passe ne correspondent pas</p>
        <label for="email">Email</label>
        <input bind:value={email} type="email" id="email" name="email" required />
        <p class="erreur invisible" id="mailerr">Ce champ est obligatoire</p>
        <p class="erreur invisible" id="mailformaterr">L'email n'est pas dans un format valide</p>
      </form>
      <div>
        <input
          type="submit"
          name="connexion_submit"
          value="Valider"
          on:click={signup}
        />
        <p class="erreur invisible" id="incorrect">Le nom d'utilisateur ou le mail est déjà utilisé</p>
      </div>
    </section>
  </main>
  
  <style>
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

  #incorrect {
    margin-top: 1px;
  }
  
    input[name="connexion_submit"] {
      background-color: orange;
      border-radius: 7px;
      width: 190px;
      height: 25px;
      border: none;
      transition: background-color 0.3s;
      cursor: pointer;
    }
  
    .social-login {
      margin-bottom: 30px;
    }
  
    input[name="connexion_submit"]:hover {
      background-color: #feb52f;
    }
    input[name="connexion_submit"] {
      background-color: orange;
      border-radius: 10px;
      align-items: center;
      margin-top: 10px;
      width: 190px;
    }
    label {
      display: block;
      text-align: left;
      color: black;
      margin-bottom: 10px;
    }
    input[type="email"],
    input[type="text"],
    input[type="password"] {
      border-radius: 10px;
      background-color: white;
      width: 400px;
      height: 30px;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      cursor: pointer;
  
      transition: border-color 0.3s;
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
  
    div {
      display: block;
    }
  
    .container {
      display: flex;
      flex-direction: column;
      align-items: center;
      border: 2px solid #ddd;
      border-radius: 10px;
      padding: 30px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      height: 490px;
      width: 450px;
      background-color: white;
    }
  </style>
  