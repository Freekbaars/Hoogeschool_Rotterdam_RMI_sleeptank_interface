import numpy as np
import serial
import time

# Placeholder voor seriële communicatie instellingen
# Zorg ervoor dat je de juiste poort en baudrate instelt voor jouw setup
serial_port = 'COM3'
baud_rate = 9600
serial_instance = serial.Serial(serial_port, baud_rate, timeout=1)


def read_serial_data():
    if serial_instance.in_waiting > 0:
        data = serial_instance.readline().decode().strip()
        parts = data.split(',')
        if len(parts) == 3:
            weight, angle_x, angle_y = parts
            return float(weight)  # Aanname: 'weight' is al in de juiste eenheid
    return None

def format_data(weight):
    # Pas deze functie aan indien nodig om de data te converteren
    return weight

def vraag_stappen_en_grootte():
    aantal_stappen = int(input("Hoeveel stappen wil je doen voor de calibratie? "))
    stap_grootte = int(input("Wat is de stapgrootte in gram? (standaard is 20) ") or "20")
    return aantal_stappen, stap_grootte

def meet_gemiddelde_voor_stap(aantal_metingen=5):
    metingen = []
    for _ in range(aantal_metingen):
        gewicht = read_serial_data()
        if gewicht is not None:
            metingen.append(format_data(gewicht))
        time.sleep(1)  # Wacht even tussen metingen
    return sum(metingen) / len(metingen) if metingen else 0

def calibratie_proces(aantal_stappen, stap_grootte):
    calibratie_data = []
    for stap in range(2 * aantal_stappen):  # Heen en terug
        gewicht_stap = stap_grootte * (stap if stap < aantal_stappen else 2 * aantal_stappen - stap - 1)
        input(f"Plaats {gewicht_stap} gram en druk op Enter om door te gaan...")
        gemiddelde_gewicht = meet_gemiddelde_voor_stap()
        calibratie_data.append((gewicht_stap, gemiddelde_gewicht))
        print(f"Stap {stap + 1}/{2 * aantal_stappen}: Gemiddelde gewicht = {gemiddelde_gewicht} voor {gewicht_stap} gram")
    return calibratie_data

def bereken_kalibratielijn(calibratie_data):
    x = np.array([data[0] for data in calibratie_data])
    y = np.array([data[1] for data in calibratie_data])
    A, B = np.polyfit(x, y, 1)  # Lineaire regressie om Y = AX + B te vinden
    return A, B

def main():
    print("Script is gestart")
    aantal_stappen, stap_grootte = vraag_stappen_en_grootte()
    calibratie_data = calibratie_proces(aantal_stappen, stap_grootte)
    A, B = bereken_kalibratielijn(calibratie_data)
    print(f"Kalibratie voltooid: A = {A}, B = {B}")

if __name__ == "__main__":
    main()
