<script>
	let username = '';
	let password = '';

    const login = async() => {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);
        fetch('http://127.0.0.1:8000/token', {
            method: "POST",
            mode: "cors",
            headers: {
                "Accept": "application/json"
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            window.localStorage.setItem("token", data.access_token);
        })
        .catch(e => {
            console.log(e);
        })
    };
</script>

<main>
	<div>
		 <input type="submit" name="google" value= "Se connecter avec Google">
		<hr>
	</div>
    <form >
		<label for="username">Nom d'utilisateur</label>
        <input bind:value={username} type="username" id="username" name="username" required>
        <label for="password">Mot de passe</label>
        <input bind:value={password} type="password" id="password" name="password" required>
     </form>
    <div> 
			<button type="button" on:click={login}>Valider</button>
		</div>
</main>

<style>
	input[name = "google"]{
		background-color : white;
		border-radius: 10px;
		color : black;
		
	}
	button{
		background-color : orange;
		border-radius: 10px;
		align-items : center;
		width : 190px
		
	}
	label{
		display : block;
		text-align : center;
		color : black;
		
	}
	input[type=username]{
		border-radius : 10px;
		background-color : white;
		width : 190px
	}
	input[type=password]{
		border-radius : 10px;
		background-color : white;
		width : 190px
	}
	main{
		  display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: white;
	}
	
	div{
		display : block
	}
</style>