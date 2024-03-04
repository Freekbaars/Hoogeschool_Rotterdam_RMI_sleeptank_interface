function laadPagina(pagina) {
    fetch(pagina)
        .then(response => response.text())
        .then(html => {
            document.getElementById('appContent').innerHTML = html;
            initialiseerGrafieken(); // Roep deze aan na het succesvol laden van de pagina

            if (pagina === 'start.html') {
                initialiseerComPortModal();
            }
            // Voer extra initialisatie uit indien nodig
        })
        .catch(err => console.error('Fout bij het laden van de pagina:', err));
}