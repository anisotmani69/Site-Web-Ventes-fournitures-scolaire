<script>

    import { onMount } from 'svelte';

    onMount(() => {
      ouvrirFenetre();

      window.addEventListener('message', (event) => {
        if (event.data === 'godot-game-loaded') {
          const iframe = document.getElementById('godot-iframe');
         
        }
        }

      );
    });

    function ouvrirFenetre() {
    var overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = '999'; 

    var body = document.querySelector('body');

    var fenetre = document.createElement('div');
    fenetre.className = 'fenetre';
    fenetre.style.position = 'fixed';
    fenetre.style.top = '60%';
    fenetre.style.right = '24%';
    fenetre.style.transform = 'translate(-50%, -50%)';
    fenetre.style.backgroundColor = '#fff';
    fenetre.style.border = '1px solid #ccc';
   
    fenetre.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
    fenetre.style.zIndex = '1000';
    fenetre.style.width = '400px';
    fenetre.style.height = '250px';

    fenetre.innerHTML = `
   <div style="display: flex; margin-botton : 0px;">
    <img src="../../src/img/cancel.png" alt="Image produit" id= "croix" style="max-width: 20px; height: 20px; margin-left: auto; margin-top: 6px; margin-right : 15px; cursor: pointer;">
   
</div>
<h2 style="margin-left: 30px;">Bienvenue dans notre jeu secret !</h2>
   
        <div id="display" style="display: flex; align-items: center;">
            <p style="margin-left: 30px;">Gagner la partie pour avoir une réduction sur votre première commande</p>             
            </div>           
        </div>
       
        <style>
            img[alt = "Image produit"]{
                width: 130px;
                height: 130px
            }    

            #display{
                margin-top:20px;
            }

            
        </style>
    `;

    body.appendChild(overlay);
    body.appendChild(fenetre);
    window.scrollTo(0, 0);

    
    overlay.addEventListener('click', function() {
      body.removeChild(overlay);
      body.removeChild(fenetre);
    });

    var votreImage = document.getElementById('croix');


votreImage.addEventListener('click', function() {
    body.removeChild(overlay);
    body.removeChild(fenetre);
});


    setTimeout(function() {
        body.removeChild(overlay);
        body.removeChild(fenetre);
    }, 10000);

}

function gagne() {
    var overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = '999'; 

    var body = document.querySelector('body');

    var fenetre = document.createElement('div');
    fenetre.className = 'fenetre';
    fenetre.style.position = 'fixed';
    fenetre.style.top = '60%';
    fenetre.style.right = '24%';
    fenetre.style.transform = 'translate(-50%, -50%)';
    fenetre.style.backgroundColor = '#fff';
    fenetre.style.border = '1px solid #ccc';
   
    fenetre.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
    fenetre.style.zIndex = '1000';
    fenetre.style.width = '400px';
    fenetre.style.height = '250px';

    fenetre.innerHTML = `
   <div style="display: flex; margin-botton : 0px;">
    <img src="../../src/img/cancel.png" alt="Image produit" id= "croix" style="max-width: 20px; height: 20px; margin-left: auto; margin-top: 6px; margin-right : 15px; cursor: pointer;">
   
</div>
<h2 style="margin-left: 30px;">Vous avez gagne !</h2>
   
        <div id="display" style="display: flex; align-items: center;">
            <p style="margin-left: 30px;">Vous avez maintenant une reduction de 5% sur votre première commande</p>             
            </div>           
        </div>
       
        <style>
            img[alt = "Image produit"]{
                width: 130px;
                height: 130px
            }    

            #display{
                margin-top:20px;
            }

            
        </style>
    `;

    body.appendChild(overlay);
    body.appendChild(fenetre);
    window.scrollTo(0, 0);

    
    overlay.addEventListener('click', function() {
      body.removeChild(overlay);
      body.removeChild(fenetre);
    });

    var votreImage = document.getElementById('croix');


votreImage.addEventListener('click', function() {
    body.removeChild(overlay);
    body.removeChild(fenetre);
});


    setTimeout(function() {
        body.removeChild(overlay);
        body.removeChild(fenetre);
    }, 10000);

}


  </script>

  <style>
    /* Ajoutez du style selon vos besoins */
    #godot-iframe {
      
      display: block;
      border: none;
      margin: auto;
    }
    
  </style>

  
<body>
  <div>
    
    <iframe
    
    width="1024"
    height="600"
    title="oui"
      id="godot-iframe"
      src="/breakouthtml/breakout.html"



    ></iframe>
  </div>
</body>
