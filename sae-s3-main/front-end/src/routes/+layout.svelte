<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import HeaderUser from "./composants/HeaderUser.svelte";
    import HeaderSeller from "./composants/HeaderConnexion.svelte";
    import Footer from "./composants/Footer.svelte";
    
    
    let currentUrl = "";
    onMount(() => {
        currentUrl = window.location.href;
        console.log(currentUrl);
    });
</script>

<header>
    {#if currentUrl.indexOf("connexion") == -1}
        <HeaderUser />
    {:else}
        <HeaderSeller />
    {/if}
</header>

<slot />

<footer>
    <Footer />
</footer>
