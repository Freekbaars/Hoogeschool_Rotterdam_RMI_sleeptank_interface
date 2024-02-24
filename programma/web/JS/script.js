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

// Wanneer de pagina geladen is worden de serial ports geladen en de grafieken getekend 
window.onload = function() {
    laadPagina('start.html')
    loadSerialPorts();
    tekenGewichtsGrafiek();
    tekenGyroGrafiek();
    tekenKalibratieGrafiek();
    showComPortModal(); // Toon de modal bij het laden van de pagina
};
