<script>

  function logout() {
    window.localStorage.removeItem("token");
    window.location.href = "../";
}
</script>

<style>


  .button-container {
    display: flex;
    flex-direction: column;
   margin-top: 80px;
  
  }

  .button {
    border: 1px solid #dddddd;
      text-align: center;
      padding: 8px;
      background-color: white;
      width: 658px;
      border-radius: 10px;
      color: black;
      transition: opacity 0.3s ease;
      height: 50px;
      margin: 4px;
  }

  .button:hover {
    opacity: 0.8;
  }


  .image-section,
  .button-container {
    box-sizing: border-box;
  }

  .image-section img{
    margin-top: 80px;
    margin-left: 300px;
    width:192px ;
    height: 192px;
  }  

  main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 20px;
    background-color: #FAF5F0;
    min-height: 100vh;
  }

  .button-container {
    grid-column: 2;
  }
</style>


<body>

  <main>
    <div class="image-section">
      <img src="../../src/img/LogoAuthentification.png" alt="im" />
    </div>
    <div class="button-container">
      <button class="button" on:click={() => window.location.href = "../historique"}>Historique de mes commandes</button>
      <button class="button"  on:click={() => window.location.href = "../favoris"}>Favoris</button>
      <button class="button" on:click={() => window.location.href = "../compte/securite"}>Connexion & sécurité</button>
      <button class="button"  on:click={logout}>Se deconnecter</button>
    </div>
  </main>
</body>
