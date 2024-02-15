<script>
     import Recherche from './Recherche.svelte';
     import { onMount } from 'svelte';
    
     function selectCategory(categoryId, typeId) {
      localStorage.setItem('selectedCategoryId', categoryId);
      localStorage.setItem('selectedTypeId', typeId);
      localStorage.setItem('affichage', "categorie");
      location.reload(); 
      console.log("stylo");
      window.location.href = "../pageproduits";
    }
    let lien = "../connexion";
    let liens ="";
    let lienss = "";
    onMount(() => {

    const token = localStorage.getItem('token'); 
    if (!token) {
      lien = '../connexion';
      liens = '../connexion'
      lienss = '../connexion'
    } else {
      lien = '../compte';
      liens = '../panier';
      lienss = '../cartable';
    }
  });

   
  </script>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<header>
    <headerGauche>
        <a href="../"><img src="/src/img/LogoDemo.png"  alt="logo" width="300" height="85"></a>
    </headerGauche>
    <Recherche />
    <headerDroite>
        <a href = {liens}><img src="/src/img/LogoPanier.png" alt="logo" width="69" height="69"></a>
        <a href = {lien}><img src="/src/img/LogoAuthentification.png" alt="logo" width="69" height="69"></a>
        
    </headerDroite>
    
</header>
<!-- <menu>
    <button on:click={() => selectCategory(1)} class="categorie">
        Stylos
        
    </button><button on:click={() => selectCategory(2)} class="categorie">
        Règle
    </button><button on:click={() => selectCategory(3)} class="categorie">
        Ciseaux
    </button><button on:click={() => selectCategory(4)} class="categorie">
        Crayon
    </button><button on:click={() => selectCategory(5)} class="categorie">
        Gomme
    </button><button on:click={() => selectCategory(6)} class="categorie">
        Taille-crayon
    </button>
    <button on:click={() => selectCategory(7)} class="categorie">
        Cahier
    </button>
    <button on:click={() => selectCategory(8)} class="categorie">
        Porte-vues
    </button>
    <button on:click={() => selectCategory(9)} class="categorie">
        Trousse
    </button>
    <button on:click={() => selectCategory(10)} class="categorie">
        Cartable
    </button>
</menu> -->

<body>
    <ul class="menu">
      
        <li><button on:click={() => selectCategory(1, -1)} class="categorie">Stylo</button>
            <ul class="sousmenu">
                <li class="ssmenu"><button on:click={() => selectCategory(1,1)} class="type">Stylo à bille</button></li>
                <li class="ssmenu"><button on:click={() => selectCategory(1,2)} class="type">Stylo plume</button></li>
              
            </ul>
        </li>
        <li><button on:click={() => selectCategory(2, -1)} class="categorie">Règle</button>
            <ul class="sousmenu">
                <li class="ssmenu"><button on:click={() => selectCategory(2,4)} class="type">Règle flexible</button></li>
                <li class="ssmenu"><button on:click={() => selectCategory(2,5)} class="type">Règle petite</button></li>
            </ul>
        </li>
        <li><button on:click={() => selectCategory(3, -1)} class="categorie">Ciseaux</button>
            
        </li>
        <li><button on:click={() => selectCategory(4, -1)} class="categorie">Crayon</button>
            <ul class="sousmenu">
                <li class="ssmenu"><button on:click={() => selectCategory(4,7)} class="type">Crayon a papier</button></li>
                <li class="ssmenu"><button on:click={() => selectCategory(4,8)} class="type">Crayons de couleur</button></li>
            </ul>
        </li>
        <li><button on:click={() => selectCategory(5, -1)} class="categorie">Gomme</button>
        </li>
        <li><button on:click={() => selectCategory(6, -1)} class="categorie">Taille-crayon</button>
            <ul class="sousmenu">
                <li class="ssmenu"><button on:click={() => selectCategory(6,9)} class="type">Avec réservoir</button></li>
                <li class="ssmenu"><button on:click={() => selectCategory(6,10)} class="type">Sans réservoir</button></li>
            </ul>
        </li>
        <li><button on:click={() => selectCategory(7, -1)} class="categorie">Cahier</button>
            <ul class="sousmenu">
                <li class="ssmenu"><button on:click={() => selectCategory(7,11)} class="type">Grands carreaux</button></li>
                <li class="ssmenu"><button on:click={() => selectCategory(7,12)} class="type">Petits carreaux</button></li>
            </ul>
        </li>
        <li><button on:click={() => selectCategory(8, -1)} class="categorie">Porte-vues</button>
        </li>
        <li><button on:click={() => selectCategory(9, -1)} class="categorie">Trousse</button>
        </li>
        <li><button on:click={() => selectCategory(10, -1)} class="categorie">Cartable</button>
            <ul class="sousmenu">
                <li class="ssmenu"><button on:click={() => window.location.href = "../Jeu"} class="type">Jeu</button></li>
            </ul>
        </li>
    </ul>
  </body> 
<style>

body {
    margin: 0;
    padding: 0;
    font: 12px Arial;
}

.menu {
    display: grid;
    grid-auto-flow: column;
    padding: 0;
    margin: 0px;
    height: 50px;
    list-style: none;
}

.menu li {
    float: left;
    position: relative;
    position: relative;
}

.menu li button.type:link,
.menu li button.type:visited {
    display: block;
    color: #FFF;
    background: #FFB13C;
   
    border-right: 1px solid #FFF;
    text-align: center;
    text-decoration: none;
}

.menu .sousmenu {
    list-style-type: none;
    display: none;
    padding: 0;
    margin: 0;
    position: absolute;
    width: 100%;
    top: 100%;
    left: 0;
    z-index: 1;
}

.menu .sousmenu li {
    float: none;
    margin: 0;
    padding: 0;
    border-right: 1px solid transparent;
  
}

.menu .sousmenu li button {
    display: block;
    color: #FFF;
    text-decoration: none;
    background-color: #FFEEDD;
    font-family :Arial, Helvetica, sans-serif;
    color : rgba(0, 0, 0, 0.4);
    width:100%;
    border: none;
    height:25px;
}

.menu .sousmenu li button.type:hover {
    background-color: #FFB13C;
}

.menu li:hover .sousmenu {
    display: block;
}






header{
    background-color: #FFEEDD;
    padding : 0;
    margin : 0;
    display : grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: auto;
    align-items: center;
}

input{
    border-radius: 20px;
    border-width: 0.2px;
}

headerGauche{
    justify-self: center;
}

headerDroite{
    display:flex;
    justify-content: space-evenly;

}



#navbar{
    width : 100%;
    height : 35px;
}

menu{
    display : grid;
    grid-auto-flow: column;
    padding : 0;
    margin : 0;
    height: 50px;
}

.categorie{
    background-color : #FFEEDD;
    height : 100%;
    width : 100%;
    display : flex;
    align-items: center;
    justify-content: center;
    border: none;
    font-size: 20px;
    font-family :Arial, Helvetica, sans-serif;
    color : rgba(0, 0, 0, 0.4);
}

.categorie:hover{
    background-color: #FFB13C;
}


</style>