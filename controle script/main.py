import numpy as np
import serial
import time
import threading


# Seriële communicatie instellingen
serial_port = 'COM3'
baud_rate = 9600
serial_instance = serial.Serial(serial_port, baud_rate, timeout=1)
weight = None


# Globale variabelen voor threading
latest_data = None
continue_reading = True

def data_reading_thread():
    global latest_data, continue_reading
    while continue_reading:
        if serial_instance.in_waiting > 0:
            data = serial_instance.readline().decode().strip()
            parts = data.split(',')
            if len(parts) == 3:
                weight, angle_x, angle_y = parts
                latest_data = float(weight)
        time.sleep(0.05)  # Korte pauze om de loop beheersbaar te houden


def start_data_thread():
    global continue_reading
    continue_reading = True
    thread = threading.Thread(target=data_reading_thread)
    thread.start()
    return thread

def stop_data_thread():
    global continue_reading
    continue_reading = False
def vraag_stappen_en_grootte():
    aantal_stappen = int(input("Hoeveel stappen wil je doen voor de calibratie? "))
    stap_grootte = int(input("Wat is de stapgrootte in gram? (standaard is 20) ") or "20")
    return aantal_stappen, stap_grootte


def meet_gemiddelde_voor_stap(aantal_metingen=20):
    metingen = []
    for i in range(aantal_metingen):
        if latest_data is not None:
            metingen.append(latest_data)
        time.sleep(0.1)  # Wacht tussen metingen om realistische samples te krijgen

    if metingen:
        gemiddelde_gewicht = sum(metingen) / len(metingen)
    else:
        gemiddelde_gewicht = None

    return gemiddelde_gewicht



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
    thread = start_data_thread()  # Start de dataleesthread
    
    # Voer je oorspronkelijke kalibratie logica hier uit
    aantal_stappen, stap_grootte = vraag_stappen_en_grootte()
    calibratie_data = calibratie_proces(aantal_stappen, stap_grootte)
    A, B = bereken_kalibratielijn(calibratie_data)
    print(f"Kalibratie voltooid: A = {A}, B = {B}")
    
    stop_data_thread()  # Stop de dataleesthread
    thread.join()  # Wacht tot de thread volledig is gestopt
    print("Script is beëindigd")


if __name__ == "__main__":
    main()
