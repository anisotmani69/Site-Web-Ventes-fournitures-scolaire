<script>
  import { onMount } from "svelte";

  export let id;
  export let image;
  export let description;
  export let prix;
  export let note;
  export let categorie;
  export let type;
  export let marque;
  export let titre;
  let url;

  onMount( async () => {
      const imageResponse = await fetch(
          `http://127.0.0.1:8000/image?filename=${image}`,
          {
            method: "GET",
            mode: "cors",
            headers: {
              Accept: "application/json",
            },
          }
        );

        if (imageResponse.ok) {
          const imageData = await imageResponse.blob();
          url = URL.createObjectURL(imageData);
          console.log("url : " + url);
        } else {
          console.error(
            `Erreur lors de la récupération de l'image pour le produit ${titre}:`,
            imageResponse.status
          );
        }
  });

  async function handleClick(){
      try {
    const response = await fetch("http://127.0.0.1:8000/search?id=" +id);
    const productData = await response.json();  
    localStorage.setItem("selectedProduct", JSON.stringify(productData));
    window.location.href = "../fiche_produit";
  } catch (error) {
    console.error('Erreur lors de la récupération des détails du produit:', error.message);
  }
  }

        

</script>

<body on:click={() => handleClick()}>
  <div class="container">
      <div class="left">
          <img class = "img" src={url} alt="image_produit">
      </div>
      
      <div class="infos">
          <h1>{titre}</h1>
          <p>{categorie} {type}</p>
          <p>{marque}</p>
          <h1>{prix} €</h1>
          <img src="src/img/Avis{Math.round(note)}.png" alt="{note}/5">
          <p>{description}</p>
      </div>
  </div>
</body>

<style>
  body{
      height: 500px;
      width: 1225px;
      background: #faf5f0;
      opacity: 100%;
      margin: 0px;
      padding: 0px;
      color: black;
  }
  .container {
      display: grid;
      grid-template-columns: 1fr 1fr;
  }
  .container .left {
      margin-left: 10%;
      height: 500px;
      display: flex;
      align-items: center;
      overflow: hidden;
  }
  .infos {
      height: 500px;
      padding-top: 10%;
  }
  .left img {
      max-width: 100%;
      height:auto;
      border-radius: 10px;
  }

  h1 {
      margin: 40px;
      font-size: 30px;
  }
  p {
      margin: 40px;
      font-size: 18px;
  }

  .img{
    width: 400px;
    height: 400px;
  }
</style>