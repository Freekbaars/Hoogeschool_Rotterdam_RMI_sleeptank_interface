// Beschrijving: JavaScript voor de webpagina
// Auteur: Freek Baars
// Laatst bewerkt: 22-01-2024
// Versie: 1.0

// Globale variabelen
let isTestActief = false;
let updateInterval;
let startTijd;
var gewichtsChart;


// Zijmenu openen en sluiten
function toggleZijmenu() {
    var zijmenu = document.getElementById("zijmenu");
    zijmenu.style.width = zijmenu.style.width === "250px" ? "0" : "250px";
}

function laadPagina(pagina) {
    fetch(pagina)
        .then(response => response.text())
        .then(html => {
            document.getElementById('appContent').innerHTML = html;
            // Verberg of verwijder de knoppen
            document.querySelector('.menu').style.display = 'none'; // Verbergen
            // of
            document.querySelector('.menu').remove(); // Volledig verwijderen
            if (pagina === 'sleep_test.html') {
                tekenGewichtsGrafiek();
                tekenGyroGrafiek();
            }
        })
        .catch(err => console.error('Fout bij het laden van de pagina:', err));
}


// Wanneer de pagina geladen is worden de serial ports geladen en de grafieken getekend 
window.onload = function() {
    loadSerialPorts();
    tekenGewichtsGrafiek();
    tekenGyroGrafiek();
    tekenCalibratieGrafiek();
    showComPortModal(); // Toon de modal bij het laden van de pagina
};
