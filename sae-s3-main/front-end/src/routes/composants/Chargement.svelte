
<script>
    import { onMount } from 'svelte';
  
    let loaded = false;
  
    onMount(() => {
      // Mettez à jour la variable loaded après un certain délai (par exemple, 2 secondes)
      setTimeout(() => {
        loaded = true;
      }, 100);
    });
  </script>
  





<main>
    {#if !loaded}
    <div class="loading">
      <img src="../src/img/Spinner.gif" alt="">
  </div>
  {/if}
</main>

<style>
      .loading {
        
        position: fixed;
            
        display: flex;
        margin-left: 550px;
       justify-content: center;
        opacity: 1; 
        transition: opacity 0.5s ease; 
        margin-bottom: 500px;
        z-index: 1;
    }
</style>