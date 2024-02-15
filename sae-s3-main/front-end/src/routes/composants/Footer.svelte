<body>
    <div class="footer-dark">
        <footer>
            <div class="container">
                <div class="row">
                    <div class="col-sm-6 col-md-3 item">
                        <h3>Services</h3>
                        <ul>
                            <li><a href="../pageproduits">Boutique de fournitures</a></li>
                            <li><a href="../panier">Panier</a></li>
                            <li><a href="../historique">Historique de commandes</a></li>
                        </ul>
                    </div>
                    <div class="col-sm-6 col-md-3 item">
                        <h3>Notre équipe</h3>
                        <ul>
                            <li><p class="nom">Jules Vic</p></li>
                            <li><p class="nom">Elouan Reymond</p></li>
                            <li><p class="nom">Anis Otmani</p></li>
                            <li><p class="nom">Thimothée Allais</p></li>
                        </ul>
                    </div>
                    <div class="col-md-6 item text">
                        <h3>Péninsule</h3>
                        <p>Nous sommes heureux de vous accueillir chez Péninsule, le futur leader de la vente de fournitures scolaires. Sur notre boutique en ligne, vous pourrez trouver tout ce que vous souhaitez utiliser pour vos cours afin que votre année se passe au mieux ! De plus, nous sommes heureux de vous présenter notre exceptionnelle particularité : le configurateur de trousse et de cartable ! Grâce à cette feature, qui deviendra bientôt un incoutournable de la vente en ligne, vous pourrez recevoir chez vous votre cartable ou votre trousse déjà rempli(e) avec ce que vous aurez choisi sur notre site !</p>
                    </div>
                </div>
                <p class="copyright">Péninsule © 2023</p>
            </div>
        </footer>
    </div>
</body>

<style>
  
  body {
    margin: 0px;
  }

  p {
    font-size: 13px;
    line-height: 1.5em;
  }

  footer {
    margin : 0px;
  }

.row {
  display : grid;
  grid-template-columns: 1fr 1fr 2fr;
  margin-left: 12%;
  margin-right: 12%;
  padding-left: 50px;
}

li {
    margin : 5px;
}

.footer-dark {
  padding:30px 0;
  color:#000000;
  background-color:#FFEEDD;
}

.footer-dark h3 {
  margin-bottom:20px;
  font-weight:bold;
  font-size:16px;
}

.footer-dark ul {
  padding:0;
  list-style:none;
  line-height:1.6;
  font-size:14px;
  margin-bottom:0;
}

.footer-dark ul a {
  color:inherit;
  text-decoration:none;
  opacity:0.6;
}

.nom{
    color:inherit;
    text-decoration:none;
    opacity:0.6;
    margin : 0px;
} 

.footer-dark ul a:hover {
  opacity:0.8;
}

@media (max-width:767px) {
  .footer-dark .item:not(.social) {
    text-align:center;
    padding-bottom:20px;
  }
}

.footer-dark .item.text {
  margin-bottom:20px;
}

@media (max-width:767px) {
  .footer-dark .item.text {
    margin-bottom:0;
  }
}

.footer-dark .item.text p {
  opacity:0.6;
  margin-bottom:0;
}

.footer-dark .item.social {
  text-align:center;
}

.footer-dark .copyright {
  text-align:center;
  padding-top:10px;
  opacity:0.3;
  font-size:13px;
  margin-bottom:0px;
}
</style>