import numpy as np
import serial
import time

# Seriële communicatie instellingen
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


def vraag_stappen_en_grootte():
    aantal_stappen = int(input("Hoeveel stappen wil je doen voor de calibratie? "))
    stap_grootte = int(input("Wat is de stapgrootte in gram? (standaard is 20) ") or "20")
    return aantal_stappen, stap_grootte

def meet_gemiddelde_voor_stap(aantal_metingen=5):
    metingen = []
    for _ in range(aantal_metingen):
        gewicht = read_serial_data()
        if gewicht is not None:
            metingen.append(gewicht)
        time.sleep(1)  # Wacht even tussen metingen
    return sum(metingen) / len(metingen) if metingen else 0

def calibratie_proces(aantal_stappen, stap_grootte):
    calibratie_data = []
    for stap in range(aantal_stappen):  # Voeg gewichten toe
        gewicht_stap = stap * stap_grootte
        input(f"Plaats {gewicht_stap} gram en druk op Enter om door te gaan...")
        gemiddelde_gewicht = meet_gemiddelde_voor_stap()
        calibratie_data.append((gewicht_stap, gemiddelde_gewicht))
        print(f"Stap {stap + 1}: Gemiddelde gewicht = {gemiddelde_gewicht} voor {gewicht_stap} gram")
    return calibratie_data

def bereken_kalibratielijn(calibratie_data):
    x = np.array([data[0] for data in calibratie_data])
    y = np.array([data[1] for data in calibratie_data])
    A, B = np.polyfit(x, y, 1)  # Lineaire regressie om Y = AX + B te vinden
    return A, B

def verifieer_calibratie(calibratie_data, A, B, aantal_stappen, stap_grootte):
    print("Begin verificatie van de kalibratie...")
    for stap in range(aantal_stappen):  # Verifieer door gewichten te verwijderen
        gewicht_stap = (aantal_stappen - stap - 1) * stap_grootte
        input(f"Verwijder om naar {gewicht_stap} gram te gaan en druk op Enter om door te gaan...")
        gemiddelde_gewicht = meet_gemiddelde_voor_stap()
        verwachte_waarde = A * gewicht_stap + B
        fout = abs(verwachte_waarde - gemiddelde_gewicht)
        print(f"Verificatie Stap {stap + 1}: Gemeten gewicht = {gemiddelde_gewicht}, Verwachte gewicht = {verwachte_waarde}, Fout = {fout}")


def main():
    print("Script is gestart")
    aantal_stappen, stap_grootte = vraag_stappen_en_grootte()
    calibratie_data = calibratie_proces(aantal_stappen, stap_grootte)
    A, B = bereken_kalibratielijn(calibratie_data)
    print(f"Kalibratie voltooid: A = {A}, B = {B}")
    verifieer_calibratie(calibratie_data, A, B, aantal_stappen, stap_grootte)

if __name__ == "__main__":
    main()
