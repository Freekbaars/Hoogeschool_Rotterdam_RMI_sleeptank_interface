# Importeer benodigde bibliotheken
import board
from digitalio import DigitalInOut
from hx711.hx711_gpio import HX711_GPIO
import adafruit_mpu6050
import math
import busio

# Definieer de GPIO pinnen voor de HX711
gpio_data = DigitalInOut(board.D5)
gpio_clk = DigitalInOut(board.D6)

# Definieer de I2C pinnen voor de gyro
i2c = board.I2C()

# Maak het HX711 object aan
hx711 = HX711_GPIO(gpio_data, gpio_clk, tare=True)

# Probeer het MPU6050 object aan te maken
try:
    mpu = adafruit_mpu6050.MPU6050(i2c)
    mpu_connected = True
except ValueError:
    mpu_connected = False

# Tijdinterval tussen metingen (in seconden)
delta_t = 0.01

# Hoofdlus
while True:
    try:
        # Lees gewicht
        weight = hx711.read()

        if mpu_connected:
            # Lees gyro en versnellingsmeter data
            gyro = mpu.gyro
            accel = mpu.acceleration

            # Bereken hoeken met versnellingsmeterdata
            angle_x = math.atan2(accel[1], accel[2])
            angle_y = math.atan2(accel[0], accel[2])

            # Converteer naar graden
            angle_x_deg = math.degrees(angle_x)
            angle_y_deg = math.degrees(angle_y)
        else:
            angle_x_deg = 0
            angle_y_deg = 0

        # Verstuur de gegevens via de seriële verbinding
        print(f"{weight},{angle_x_deg},{angle_y_deg}")

    except OSError:
        print("Leesfout")

