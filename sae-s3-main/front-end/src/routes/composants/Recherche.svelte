
<script>
     export let mot = '';
    
  const handleSearch = () => {
    localStorage.setItem('recherche', mot);
    localStorage.setItem('affichage', "barre");
    location.reload(); 
    window.location.href = "../pageproduits";
  };
  </script>
  
  <style>
    div {
      display: flex;
      align-items: center;
      width: 300px; 
      height: 100px;
    }
  
    input {
      padding: 8px;
      font-size: 16px;
      border: 1px solid #ccc; 
      border-top-left-radius: 10px;
      border-bottom-left-radius: 10px; 
      flex: 1; 
      height: 30px;
    
    }
  
    button {
      padding: 8px 16px;
      font-size: 16px;
      border: 1px solid #ccc; 
      border-top-right-radius: 10px;
      border-bottom-right-radius: 10px; 
      margin-left: -1px; 
      cursor: pointer;
      width: 10px;
      height: 47px;
      align-items: center;
      justify-content: center;
      display: flex;
      transition: background-color 0.3s;
    }
    button img {
    width: 18px; 
    height: 20px; 
  
  }

  button:hover {
    background-color: #ddd; 
  }

  .recherche{
    width:650px;
    
  }

  </style>
  
  <div class = "recherche">
    <input bind:value={mot} placeholder="Recherche..." />
    <button on:click={handleSearch}>
      <img src="../src/img/BarreDeRecherche.png" alt="Logo Recherche" />
      </button>
  </div>
  
  