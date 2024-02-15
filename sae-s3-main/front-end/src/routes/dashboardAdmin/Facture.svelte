<script>
    async function fetchAndOpenPDF() {
        const response = await fetch('http://127.0.0.1:8000/facture?id=1', {
            headers: {
                'accept': 'application/json',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3MDYwNDI1NTl9.FFXDVQuEzzOwRlmHzo7t7aH3Dv1XA3R28_zOLQd4_j4'
            }
        });

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        window.open(url);
    }
</script>

<button on:click={fetchAndOpenPDF}>Requêter l'endpoint et afficher le PDF</button>
