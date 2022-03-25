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

frequency = 0


def readreg(reg, dec):
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


def readdata(filedata):
    global frequency

    date_time = strftime('%Y-%m-%d %H:%M:%S', localtime())

    for i in range(2):
        apparent_power = readreg(rS_T,  0)
        test_frequency = readreg(rFrec, 2)
        if is_verified(test_frequency):
            frequency = test_frequency
            break

    human_message = "%s: %dW, %.1fHz" % (date_time, apparent_power, frequency)
    rf_message = "%.0f,%.1f" % (apparent_power, frequency)
    csv_record = "%s,%.0f,%.1f\n" % (date_time, apparent_power, frequency)
    print(human_message)
    ser.write(rf_message.encode())
    filedata.write(csv_record)


def checktime(sec):
    while True:
        res = round(time() % sec)
        if res == 0.0:
            readdata(filedata)
        sleep(0.5)


while True:
    checktime(1)
