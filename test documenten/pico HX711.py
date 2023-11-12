from hx711 import HX711
import time
import dht
import ujson
import machine

led_pin = machine.Pin(25, machine.Pin.OUT)


baudrate = 9600

# Open de seriële poort met de opgegeven baudrate
uart = machine.UART(0, baudrate=baudrate)


class Scales(HX711):
    def __init__(self, d_out, pd_sck):
        super(Scales, self).__init__(d_out, pd_sck)
        self.offset = 0

    def reset(self):
        self.power_off()
        self.power_on()

    def tare(self):
        self.offset = self.read()

    def raw_value(self):
        return self.read() - self.offset

    def stable_value(self, reads=10, delay_us=500):
        values = []
        for _ in range(reads):
            values.append(self.raw_value())
            time.sleep(delay_us / 1000000)  # Sleep in seconds
        return self._stabilizer(values)

    @staticmethod
    def _stabilizer(values, deviation=10):
        weights = []
        for prev in values:
            weights.append(sum([1 for current in values if abs(prev - current) / (prev / 100) <= deviation]))
        return sorted(zip(values, weights), key=lambda x: x[1]).pop()[0]

if __name__ == "__main__":
    scales = Scales(d_out=5, pd_sck=4)
    scales.tare()
    while True:
        try:
            val = scales.stable_value()
            print(val)
            led_pin.on()
            time.sleep(0.1)  # Wacht 100 milliseconden (0.1 seconde) voordat je de volgende meting uitvoert
            led_pin.off()
            time.sleep(0.1)
            # Maak een JSON-object met temperatuur en vochtigheid
            data = {
                'kracht': val,
            }

            data_str = ujson.dumps(data)
            print(f"Verzonden gegevens: {data_str}")
            # Verstuur de JSON-gegevens via de seriële poort
            uart.write(data_str)

        except OSError as e:
            print('Failed to read sensor.')
