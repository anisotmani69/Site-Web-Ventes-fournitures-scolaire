<script>
    import { onMount } from "svelte";

    let file = null;

    async function uploadImage() {
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:8000/image", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data.message);
            } else {
                console.error("Upload failed");
            }
        } catch (error) {
            console.error(error);
        }
    }

    function handleFileChange(event) {
        file = event.target.files[0];
    }
</script>

<input type="file" accept=".png" on:change={handleFileChange} />
<button on:click={uploadImage}>Upload</button>
