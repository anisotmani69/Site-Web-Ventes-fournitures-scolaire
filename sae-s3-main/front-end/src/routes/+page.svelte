<script>
    import { onMount } from "svelte";
   import Chargement from "./composants/Chargement.svelte";
   import Tendance from "./composants/tendances.svelte";

    console.log("quoicoubehhhhhhhhhh");
    const produitsId = [1,12,13,8];
    let produits;
    let loaded = false;

    onMount(async () => {
      setTimeout(() => {
      loaded = true;
    }, 100);

        produits = await Promise.all(
            produitsId.map(async (id) => {
                const response = await fetch(`http://127.0.0.1:8000/search?id=${id}`, {
                     method: "GET",
                     mode: "cors",
                     headers: {
                         Accept: "application/json",
                         "Content-Type": "application/json",
                     },
                 });
                 if (response.ok) {
                    const data = await response.json();
                    return data;}
                else{
                    console.error("Erreur lors de la recherche du produit :", searchResponse.statusText);
                    return 0;
                }
            })
        );
            console.log(produits)
            console.log(produits[1][0].titre)
    });
  
  </script>
<div>



<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<main>
<body>
   {#if !loaded}
   <Chargement />
 {:else}

    <h1>Nos produits tendances !</h1>
    <div id="slider">
        <input type="radio" name="slider" id="slide1" checked>
        <input type="radio" name="slider" id="slide2">
        <input type="radio" name="slider" id="slide3">
        <input type="radio" name="slider" id="slide4">
        <div id="slides">
           <div id="overflow">
              <div class="inner">
                 <div class="slide slide_1">
                    <div class="slide-content">
                     <Tendance id={produits[0][0].id} image={produits[0][0].image} description={produits[0][0].description} prix={produits[0][0].prix} note={produits[0][0].note} categorie={produits[0][0].categorie.nom} type={produits[0][0].type.nom} marque={produits[0][0].marque.nom} titre={produits[0][0].titre}/>
                    </div>
                 </div>
                 <div class="slide slide_2">
                    <div class="slide-content">
                     <Tendance id={produits[1][0].id} image={produits[1][0].image} description={produits[1][0].description} prix={produits[1][0].prix} note={produits[1][0].note} categorie={produits[1][0].categorie.nom} type={produits[1][0].type.nom} marque={produits[1][0].marque.nom} titre={produits[1][0].titre}/>
                    </div>
                 </div>
                 <div class="slide slide_3">
                    <div class="slide-content">
                     <Tendance id={produits[2][0].id} image={produits[2][0].image} description={produits[2][0].description} prix={produits[2][0].prix} note={produits[2][0].note} categorie={produits[2][0].categorie.nom} type={produits[2][0].type.nom} marque={produits[2][0].marque.nom} titre={produits[2][0].titre}/>
                    </div>
                 </div>
                 <div class="slide slide_4">
                    <div class="slide-content">
                     <Tendance id={produits[3][0].id} image={produits[3][0].image} description={produits[3][0].description} prix={produits[3][0].prix} note={produits[3][0].note} categorie={produits[3][0].categorie.nom} type={produits[3][0].type.nom} marque={produits[3][0].marque.nom} titre={produits[3][0].titre}/>
                    </div>
                 </div>
              </div>
           </div>
        </div>
        <div id="controls">
           <label for="slide1"></label>
           <label for="slide2"></label>
           <label for="slide3"></label>
           <label for="slide4"></label>
        </div>
        <div id="bullets">
           <label for="slide1"></label>
           <label for="slide2"></label>
           <label for="slide3"></label>
           <label for="slide4"></label>
        </div>
     </div>
   {/if}
   <!-- 
                            <img src="src\img\Stylo.png" alt="produit"/>
                            <div class="slider_content_item">
                              <div class="item item1">{produits[1][0].titre}</div>
                              <div class="item item3"><del>2€</del></div>
                              <div class="item item4">-10%</div>
                              <div class="item item5">{produits[1][0].prix}€</div>
                              <div class="item item6">
                                <img src="src\img\Avis{Math.round(produits[1][0].note)}.png" alt="produit" />
                              </div>  
                            </div>-->
</body>
</main>
<style>
   main {
      margin: 0px;
   }

   h1 {
       margin: 0px;
       margin-bottom: 30px;
       margin-left: 40%;
       color: #ffb13c;
       font-size: 40px;
   }
#slider {
   width: 1250px;
   max-width: 100%;
   text-align: center;
   margin: auto
}
#slider input[type=radio] {
   display: none;
}
#slider label {
   cursor:pointer;
   text-decoration: none;
}
#slides {
   padding: 10px;
   border: 3px solid #ccc;
   background: #fff;
   position: relative;
   z-index: 1;
}
#overflow {
   width: 100%;
   overflow: hidden;
}
#slide1:checked ~ #slides .inner {
   margin-left: 0px;
}
#slide2:checked ~ #slides .inner {
   margin-left: -100%;
}
#slide3:checked ~ #slides .inner {
   margin-left: -200%;
}
#slide4:checked ~ #slides .inner {
   margin-left: -300%;
}
#slides .inner {
   transition: margin-left 800ms cubic-bezier(0.770, 0.000, 0.175, 1.000);
   width: 400%;
   line-height: 0;
   height: 500px;
}
#slides .slide {
   width: 25%;
   float:left;
   display: flex;
   justify-content: center;
   align-items: center;
   height: 100%;
   color: #fff;
}
#slides .slide_1 {
   background: #00171F;
}
#slides .slide_2 {
   background: #003459;
}
#slides .slide_3 {
   background: #007EA7;
}
#slides .slide_4 {
   background: #00A8E8;
}
#controls {
   margin: -280px 0 0 0;
   width: 100%;
   height: 50px;
   z-index: 3;
   position: relative;
}
#controls label {
   transition: opacity 0.2s ease-out;
   display: none;
   width: 35px;
   height: 50px;
   opacity: .4;
}
#controls label:hover {
   opacity: 1;
}
#slide1:checked ~ #controls label:nth-child(2),
#slide2:checked ~ #controls label:nth-child(3),
#slide3:checked ~ #controls label:nth-child(4),
#slide4:checked ~ #controls label:nth-child(1) {
   float:right;
   margin: 0 -50px 0 0;
   display: block;
   background-image: url('src/img/slide_arrow_right.png');
   background-size: 100% 100%;
   
}
#slide1:checked ~ #controls label:nth-last-child(2),
#slide2:checked ~ #controls label:nth-last-child(3),
#slide3:checked ~ #controls label:nth-last-child(4),
#slide4:checked ~ #controls label:nth-last-child(1) {
   float:left;
   margin: 0 0 0 -50px;
   display: block;
   background-image: url('src/img/slide_arrow_left.png');
   background-size: 100% 100%;
}
#bullets {
   margin: 250px 0 0;
   text-align: center;
}
#bullets label {
   display: inline-block;
   width: 10px;
   height: 10px;
   border-radius:100%;
   background: #ccc;
   margin: 0 10px;
}
#slide1:checked ~ #bullets label:nth-child(1),
#slide2:checked ~ #bullets label:nth-child(2),
#slide3:checked ~ #bullets label:nth-child(3),
#slide4:checked ~ #bullets label:nth-child(4) {
   background: #444;
}
@media screen and (max-width: 900px) {
   #slide1:checked ~ #controls label:nth-child(2),
   #slide2:checked ~ #controls label:nth-child(3),
   #slide3:checked ~ #controls label:nth-child(4),
   #slide4:checked ~ #controls label:nth-child(1),
   #slide1:checked ~ #controls label:nth-last-child(2),
   #slide2:checked ~ #controls label:nth-last-child(3),
   #slide3:checked ~ #controls label:nth-last-child(4),
   #slide4:checked ~ #controls label:nth-last-child(1) {
      margin: 0;
   }
   #slides {
      max-width: calc(100% - 140px);
      margin: 0 auto;
   }
}
#offres {
    border: 2px solid black;
    height: 450px;
    width: 800px;
    position: absolute;
    left: 50%;
    transform: translate(-50%, 0);
}

main body{
/*     background: url("src/img/image57.png");
    background-repeat: no-repeat;
    height: 100%;
    margin : 0; */
    background: url('src/img/image57.png') no-repeat center center fixed;
    margin: 0;
    background-size: cover;
    padding: 50px
    
}
body {
   
}
#imgfond {
  width: 100%; 
  display: block;
  z-index:1;
}
#redirects{
    position: relative;
  display: inline-block;
}

.redirect{
    position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
    background-color: #FFB13C;
    color : white;
    border-radius: 60px;
    width: 356px;
    height: 87px;
    font-size: 30px;
    border:0;
    padding:20px 50px;
    display: flex;
    align-items: center;
	text-decoration: none;
    opacity: 1;
      transition: opacity 0.3s ease; 
      cursor: pointer;
}

     button[class = redirect]:hover {
      opacity: 0.8;
      }
</style>
</div>