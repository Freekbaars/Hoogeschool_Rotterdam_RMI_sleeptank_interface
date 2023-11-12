import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import ujson
import pandas as pd

def find_serial_port():
    ports = list(serial.tools.list_ports.comports())
    portlist = []

    for p in ports:
        portlist.append(str(p.device))
        print(str(p.device))

    val = input("Selecteer de poort: COM")

    portVar = None
    for x in range(len(portlist)):
        if portlist[x].startswith("COM" + val):
            portVar = "COM" + val
            print(portlist[x])

    return portVar

def open_serial_port(portVar):
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = portVar

    try:
        serialInst.open()
    except Exception as e:
        print(f"Fout bij het openen van de poort {portVar}: {str(e)}")
        exit()

    return serialInst

def process_sensor_data(packet, kracht_data):
    stringN = packet.decode()
    string = stringN.rstrip()
    print(string)

    if "Verzonden gegevens" in string:
        try:
            data = ujson.loads(string.split("Verzonden gegevens: ")[1])
            kracht_data.append(data['kracht'])
        except ValueError:
            print(f"Kon de numerieke waarden niet uit de JSON-string halen: {string}")

def main():
    portVar = find_serial_port()
    if portVar is None:
        print(f"COM{val} niet gevonden. Programma wordt afgesloten.")
        return

    serialInst = open_serial_port(portVar)

    kracht_data = []  # Een lijst om gegevens op te slaan

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    fig.suptitle('Live Sensor Data')

    line_kracht, = ax1.plot([], [], lw=2, label='kracht')

    def update(frame):
        if serialInst.in_waiting:
            packet = serialInst.readline()
            process_sensor_data(packet, kracht_data)

            line_kracht.set_data(range(len(kracht_data)), kracht_data)
            
            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()

    ani = FuncAnimation(fig, update, frames=range(1000), repeat=False)
    plt.legend(handles=[line_kracht])
    plt.tight_layout()
    plt.show()

    serialInst.close()

if __name__ == "__main__":
    main()
