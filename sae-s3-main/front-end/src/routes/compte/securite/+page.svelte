<script>
    import { onMount } from 'svelte';
    let user = [];
    let nom ;
    let prenom;
    let adresse;
    let showDiv = false;
    let modification;
    
    onMount(async() => {
        
        const token = window.localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
        console.log("L'utilisateur n'est pas connecté. Redirection vers la page de connexion...");
        window.location.href("../connexion");
    }
        try{
            const respons = await fetch("http://127.0.0.1:8000/user/me/", {
            method: "GET",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });
    
    if (respons.ok) {
      const productsData = await respons.json();
      user = productsData;
      localStorage.setItem("user", JSON.stringify(productsData));
      console.log("user", user);
    } else {
      console.error('Erreur lors de la récupération des produits:', respons.status);
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des produits:', error.message);
  }


  });

  const modifications = async (user, field) => {
    const token = window.localStorage.getItem("token");
    console.log("Token:", token);
        const data = {
            nom_utilisateur: user.nom_utilisateur,
            nom:user.nom,
            prenom: user.prenom,
            email :user.adresse,
            adresse: user.adresse,
            ville: user.ville,
            telephone: user.telephone,
};
console.log("dde",data);

            console.log("ded",data);
             const response = await fetch(`http://127.0.0.1:8000/user/me`, {
            method: "PUT",
            mode: "cors",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(data),
        })
        if (response.ok) {
            const data = await response.json();
            console.log(data);
        }
        else{
            console.log("ça marche pas");
            const errorData = await response.json();
    console.error("Erreur lors de la requête :", response.status, response.statusText, errorData);

        }
        showDiv = true;
        console.log(`La modification pour ${field}`);
        console.log("text", text);
        modification = text;
    };


</script>


<body>
    <main>
        <div class = "debut">
    <a href="../compte">Votre compte ></a>
    Connexion & sécurité
</div>
{#if showDiv}
    <div class="notification">
        <div class ="vide"></div>
        Cordonnés mis à jour.
    </div>
{/if}
    <p id = "text">Connexion & sécurité</p>
    <div class = "container">
        <div class = "info">
            <div>
            <label for="product-name">Nom</label>
        </div>
            <input bind:value={user.nom} type="text" id="product-name" name="product-name" >
            {#if user.nom===""}
            <button on:click={() => modifications(user, "Nom")}>Ajouter </button>
            {:else}
                <button on:click={() => modifications(user)}>Modifier</button>
            
            {/if}
        </div>
        <div class = "info">
            <div>
            <label for="product-name">Prenom</label>
        </div>

            <input bind:value={user.prenom} type="text" id="product-name" name="product-name" >
            {#if user.prenom===""}
            <button on:click={() => modifications(user)}>Ajouter</button>
            {:else}
                <button on:click={() => modifications(user)}>Modifier</button>
            
            {/if}
        </div>
        <div class = "info">
            <div>
            <label for="product-name">Adresse</label>
        </div>
            <input bind:value={user.adresse} type="text" id="product-name" name="product-name" >
            {#if user.adresse===""}
            <button on:click={() => modifications(user)}>Ajouter</button>
            {:else}
                <button on:click={() => modifications(user)}>Modifier</button>
            
            {/if}
        </div>
        <div class = "info">
            <div>
            <label for="product-name">Telephone</label>
        </div>
            <input bind:value={user.telephone} type="text" id="product-name" name="product-name" >
            {#if user.telephone===""}
            <button on:click={() => modifications(user)}>Ajouter</button>
            {:else}
                <button on:click={() => modifications(user)}>Modifier</button>
            
            {/if}
        </div>
        <div class = "info">
            <div>
            <label for="product-name">E-mail</label>
        </div>
            <input bind:value={user.email} type="text" id="product-name" name="product-name" >
            {#if user.email===""}
            <button on:click={() => modifications(user)}>Ajouter</button>
            {:else}
                <button on:click={() => modifications(user)}>Modifier</button>
            
            {/if}
        </div>
    </div>
</main>
</body>

<style>
    body{
        display: grid;
        padding: 0px;
        margin: 0px;
        background-color: #FAF5F0;
        align-items: center;
        justify-self: center;
    }

    .notification {
        margin-top: 14px;
        display: grid;
       
        height: 30px;
        width: 300px;
       align-items: center;
        border-radius: 5px;
        text-align: left;
        border: 1.5px solid #067d62;
        align-items: center;
        justify-self: center;
    }
    .vide{
        background-color: #067d62;
        height: 100%;
        margin-right: 10px;
    }

   

    .debut{
       
     color: rgb(216, 73, 11);
        
    }

    .debut a{
        text-decoration: none;
    }

    .container{
     
        border-radius: 5px;
      
        width: 600px;
        height: 500px;
        margin-bottom: 20px;
    }

    .info{
        border : 0.5px solid rgb(190, 188, 188);
        padding: 30px;
    }
    .info:first-child{
        border-top-right-radius: 5px;
        border-top-left-radius: 5px;
    }

    .info:last-child{
        border-bottom-right-radius: 5px;
        border-bottom-left-radius: 5px;
    }

    .info button{
        margin-left: 150px;
        
        width: 120px;
        height: 30px;
        border-radius: 5px;
        border : 0.5px solid rgb(190, 188, 188);
        background-color: white;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        cursor: pointer;

    }

    label[for="product-name"]{
        
        display: block;          
        font-size: 20px;
    }

    input{
        margin-top: 10px;
       
    }
    
    #text{
        font-size: 30px;
    }

    main {
        display: grid;
        align-self: center;
        justify-content: center;
        margin-bottom: 150px;
    }
</style>
