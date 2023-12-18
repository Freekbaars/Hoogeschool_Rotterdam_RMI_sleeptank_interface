import eel
import serial.tools.list_ports
import serial
import threading
import pandas as pd
import time

eel.init('test\web')  # Vervang met het pad naar je web map

# Globale variabele voor het bijhouden van de laatste krachtmeting
latest_force_reading = None
serial_instance = None
is_test_running = False
data_frame = None
csv_bestandsnaam = None

def read_serial_data():
    global data_frame, is_test_running, latest_force_reading
    while is_test_running and serial_instance.isOpen():
        data = serial_instance.readline().decode().strip()
        if data_frame is not None:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            data_frame = data_frame.append({'Tijd': current_time, 'Data': data}, ignore_index=True)
        latest_force_reading = data  # Update de laatste meting

@eel.expose
def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]
print(get_serial_ports())


@eel.expose
def open_serial_port(portVar):
    global serial_instance, is_test_running
    try:
        serial_instance = serial.Serial(portVar, baudrate=9600, timeout=1)
        if not is_test_running:
            is_test_running = True
            # Start de thread zonder argumenten mee te geven
            threading.Thread(target=read_serial_data, daemon=True).start()
        return True
    except Exception as e:
        print(f"Fout bij het openen van de poort {portVar}: {str(e)}")
        return False


@eel.expose
def get_latest_force_reading():
    global latest_force_reading
    return latest_force_reading


@eel.expose
def set_csv_bestandsnaam(bestandsnaam):
    global csv_bestandsnaam
    csv_bestandsnaam = bestandsnaam
    print("Bestandsnaam voor CSV is ingesteld op:", csv_bestandsnaam)



@eel.expose
def start_test():
    global is_test_running, data_frame, csv_bestandsnaam
    if not is_test_running and csv_bestandsnaam:
        is_test_running = True
        data_frame = pd.DataFrame(columns=['Tijd', 'Data'])
        
        # Sla een leeg DataFrame op als CSV-bestand om het bestand aan te maken
        data_frame.to_csv(csv_bestandsnaam + '.csv', index=False)
        
        # Start de thread voor het lezen van data
        threading.Thread(target=read_serial_data, daemon=True).start()
        print("Test gestart, leeg CSV-bestand aangemaakt:", csv_bestandsnaam + '.csv')
    else:
        print("Test is al gestart of bestandsnaam is niet ingesteld")



@eel.expose
def stop_test():
    global is_test_running, data_frame, csv_bestandsnaam
    if is_test_running:
        is_test_running = False
        if data_frame is not None:
            data_frame.to_csv(csv_bestandsnaam + '.csv', index=False)
            print("Data opgeslagen in:", csv_bestandsnaam + '.csv')
        data_frame = None
        csv_bestandsnaam = None  # Reset de bestandsnaam
    else:
        print("Geen actieve test om te stoppen")






eel.start('index.html')
