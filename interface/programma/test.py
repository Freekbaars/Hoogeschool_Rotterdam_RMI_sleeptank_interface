import unittest
from unittest.mock import patch
import serial.tools.list_ports
import programma

class TestFindSerialPort(unittest.TestCase):
    @patch('builtins.input', return_value='3')
    @patch.object(serial.tools.list_ports, 'comports', return_value=[serial.tools.list_ports_common.ListPortInfo(device='COM3')])
    def test_find_serial_port(self, input_mock, comports_mock):
        self.assertEqual(programma.find_serial_port(), 'COM3')

if __name__ == '__main__':
    unittest.main()