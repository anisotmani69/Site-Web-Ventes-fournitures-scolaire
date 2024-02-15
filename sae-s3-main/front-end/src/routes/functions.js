
function search(id){
    fetch("http://127.0.0.1:8000/search?id="+id)
	.then(res => res.json())
	.then(data => {
		console.log(data);
        return data;
	})
    
}

function createArticle(id_marque, id_categorie, id_vendeur, id_type, id_couleur, titre, description, prix, image){
fetch("http://127.0.0.1:8000/createarticle", {
        method: "POST",
        mode: "cors",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify(
            {
                "id_marque": `${id_marque}`,//int
                "id_categorie": `${id_categorie}`,//int
                "id_vendeur": `${id_vendeur}`,//int
                "id_type": `${id_type}`,//int
                "id_couleur": `${id_couleur}`,//int
                "titre": `${titre}`,//string
                "description": `${description}`,//string
                "prix": `${prix}`,//float
                "image": `${image}`//string
            }
        )
        
    })
    .then(response => response.json())
    .then(data => {
        console.log("ca marche");
        console.log(data);
        console.log("nigger : " + image + " nigger2 " + `${image}`)
        
        return data;
    })
    .catch(e => {
        console.log("ca marche toujours pas");
        console.log(e);
    })

    }
    export {search, createArticle}