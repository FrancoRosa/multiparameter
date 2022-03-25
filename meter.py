#!/usr/bin/env python
import serial
import minimalmodbus
from registers import *
from settings import *
from time import sleep, strftime, localtime, time

filedata = open(filedir, "a")
ser = serial.Serial(rf_port)
power_meter = minimalmodbus.Instrument(modbus_port, 12)
power_meter.serial.baudrate = 9600
power_meter.serial.bytesize = 8
power_meter.serial.parity = serial.PARITY_NONE
power_meter.serial.stopbits = 1
power_meter.serial.timeout = 1
power_meter.mode = minimalmodbus.MODE_RTU
power_meter.debug = modbus_debug


def save_record(file, line):
    f = open(file, "a")
    f.write(line)
    f.close()


def read_register(reg, dec):
    for i in range(2):
        sleep(0.1)
        try:
            return power_meter.read_register(reg, dec)
        except:
            return 0
            pass


def is_verified(frequency):
    if frequency > 40 and frequency < 99:
        return True
    return False


def read_data():
    frequency = None
    for i in range(2):
        apparent_power = read_register(rS_T,  0)
        test_frequency = read_register(rFrec, 2)
        if is_verified(test_frequency):
            frequency = test_frequency
            break
    return {"frequency": frequency, "power": apparent_power}


def checktime(sec):
    return round(time() % sec) == 0


while True:
    if (checktime(1)):
        data = read_data()
        date_time = strftime('%Y-%m-%d %H:%M:%S', localtime())
        if data["frequency"]:
            human_message = "%s: %dW, %.1fHz" % (
                date_time, data["power"], data["frequency"])
            print(human_message)
        else:
            print("... modbus error")

    if checktime(5) and data["frequency"]:
        rf_message = "%.0f,%.1f" % (data["power"], data["frequency"])
        ser.write(rf_message.encode())
        print("... rf")

    if checktime(5) and data["frequency"]:
        csv_record = "%s,%.0f,%.1f\n" % (
            date_time, data["power"], data["frequency"])
        save_record(filedir, csv_record)
        print("... csv")

    sleep(0.5)
