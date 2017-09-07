import struct
import smbus2 as smbus
import time


class Functions:

    bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

    @staticmethod
    def strip_line(line_str):
        x, y = line_str.split(';')
        return float(x), float(y.strip())

    @staticmethod
    def read_ups_voltage(bus=bus):
        address = 0x36
        read = bus.read_word_data(address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 78.125 / 1000000
        return voltage

    @staticmethod
    def read_ups_capacity(bus=bus):
        address = 0x36
        read = bus.read_word_data(address, 4)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped / 256
        return capacity

# orig = 5048.7260, 00305.1311
# dest = 5048.7259, 00305.1304
#
# print(round(Formulas.calculateDistance(orig, dest), 0))

# bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
#
# print("Voltage:%5.2fV" % Formulas.readUPSVoltage(bus))
#
# print("Battery:%5i%%" % Formulas.readUPSCapacity(bus))
