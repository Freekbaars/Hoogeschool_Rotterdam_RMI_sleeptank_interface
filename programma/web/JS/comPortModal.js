function initialiseerComPortModal() {
    // Toon de modal
    showComPortModal();

    // Voeg event listener toe aan de sluitknop
    document.querySelector('.close').addEventListener('click', function() {
        document.getElementById("comPortModal").style.display = "none";
    });
}

function showComPortModal() {
    var modal = document.getElementById("comPortModal");
    if (modal) {
        modal.style.display = "block";
    }
}

async function openSelectedPort(port) {
    let isOpened = await eel.open_serial_port(port)();
    if(isOpened) {
        alert("COM poort " + port + " succesvol geopend.");
        var modal = document.getElementById("comPortModal");
        modal.style.display = "none";
    } else {
        alert("Fout bij het openen van de poort");
    }
}

function startKalibratie() {
    var modal = document.getElementById("kalibratieModal");
    modal.style.display = "block";
    
    // Sluit de modal wanneer de gebruiker op de sluitknop klikt
    var span = document.getElementsByClassName("close")[0];
    span.onclick = function() {
      modal.style.display = "none";
    }
    
    // Sluit de modal wanneer de gebruiker ergens buiten de modal klikt
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
}
  
function startKalibratieProces() {
    const aantalStappen = document.getElementById('stappen').value;
    const stapGrootte = document.getElementById('gewicht').value;
  
    // Roep de Python-functie aan met de ingevoerde waarden
    eel.start_kalibratie(aantalStappen, stapGrootte)((response) => {
        const [calibratieData, A, B] = response;
        updateKalibratieGrafieken(calibratieData, A, B);
    });
  
    // Sluit de modal na het starten van de kalibratie
    document.getElementById('kalibratieModal').style.display = 'none';
}
  
function updateKalibratieGrafieken(calibratieData, A, B) {
    // Implementeer het updaten van de grafieken met de ontvangen kalibratie data
}

eel.expose(toonKalibratieStapModal);
function toonKalibratieStapModal(tekst) {
    document.getElementById("kalibratieStapTekst").innerText = tekst;
    document.getElementById("kalibratieStapModal").style.display = "block";
}
  
function sluitKalibratieStapModal() {
    document.getElementById("kalibratieStapModal").style.display = "none";
}
  
function bevestigKalibratieStap() {
    eel.gewicht_plaatsing_bevestigen();  // Stuur bevestiging naar Python
        console.log("Gewicht plaatsing bevestigd, doorgaan met kalibratie");
        // Optioneel: Update UI om de volgende stap aan te geven

    sluitKalibratieStapModal();
}