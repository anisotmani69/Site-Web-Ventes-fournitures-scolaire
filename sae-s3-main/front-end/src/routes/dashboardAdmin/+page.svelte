<script>
    import Login from "../connexion/Login.svelte";
    import Facture from "./Facture.svelte";
    import Panier from "./Panier.svelte";
    import Upload from "./Upload.svelte";
    
    let test = '';

    const teeest = async () => {
        console.log('test');
        const url = 'http://127.0.0.1:8000';
        fetch(url)
            .then(
                (response) => response.json()
            )
            .then((data) => {
                console.log(data);
                test = data.message;
            });
    }

</script>

<div>
    <h1>Dashboard Admin</h1>
    <p>Ce bouton est fait pour tester l'api</p>
    <textarea bind:value={test}></textarea>
    <button type="button" on:click={teeest}>Test</button>
    <Login />
    <Panier />
    <Upload />
    <Facture />
</div>