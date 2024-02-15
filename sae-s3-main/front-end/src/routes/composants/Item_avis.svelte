<script>
    export let commentaire;
    export let note;
    export let date;
</script>

<body>
    <div>
        <img src="src/img/Avis{note}.png" alt="note" margin-left="100px">
        <p>Le {date}</p>
    </div>
    <p class="avis_string">{commentaire}</p>
</body>

<style>

    .avis_string{
		font-size:25px;
		margin-left:15px;
	}

    div{
		display:grid;
		grid-template-columns:1fr 3fr;
		font-size:25px;
		align-items:center;
	}

    


</style>