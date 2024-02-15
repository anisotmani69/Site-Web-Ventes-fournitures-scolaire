<script>
    const url = "http://127.0.0.1:8000/";

    const addProductCart = async (event) => {
        event.preventDefault()
        const id = document.getElementById("item_id").value;
        fetch(url+'panier', {
            method: "POST",
            mode: "cors",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                Authorization: "Bearer " + window.localStorage.getItem("token"),
            },
            body: JSON.stringify(
                {
                    "id_article": id,
                }
            )
        })
        .then(response => response.json())
        .then(data => {
            console.log("ca marche");
            console.log(data);
        })
        .catch(e => {
            console.log("ca marche toujours pas");
            console.log(e);
        })
    };

    const deleteProductCart = () => {
        fetch(url+'panier/', {
            method: "DELETE",
            mode: "cors",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                Authorization: "Bearer " + window.localStorage.getItem("token"),
            },
            body: JSON.stringify(
                {
                    "id_article": id,
                }
            )
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(e => {
            console.log(e);
        })
    }

    const getProductCart = () => {

        fetch(url+'panier/', {
            method: "GET",
            mode: "cors",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                Authorization: "Bearer " + window.localStorage.getItem("token"),
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(e => {
            console.log(e);
        })
    };
</script>

<main>
    <h1>Panier</h1>
    <div>
        <label for="item_id">ID item</label>
        <input type="number" id="item_id" name="item_id" required>
        <button type="button" on:click={addProductCart}>Ajouter un produit</button>
        <button type="button" on:click={getProductCart}>Récuperer le contenu du panier</button>
    </div>
</main>