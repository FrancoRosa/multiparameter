#!/usr/bin/env python
import serial
import minimalmodbus
from time import sleep, strftime, localtime, time
print("...sleeping")
sleep(10)
# meterID
idestacion = "1"
# Power Analizer ModBus Registers
rV_U = 37
rV_V = 38
rV_W = 39

rV_UV = 40
rV_VW = 41
rV_WU = 42

rI_U = 43
rI_V = 44
rI_W = 45

rP_U = 46
rP_V = 47
rP_W = 48
rP_T = 49

rQ_U = 50
rQ_V = 51
rQ_W = 52
rQ_T = 53

rPF_U = 54
rPF_V = 55
rPF_W = 56
rPF_T = 57

rS_U = 58
rS_V = 59
rS_W = 60
rS_T = 61

rFrec = 62

rWWP = [63, 64]
rWPN = [65, 66]
rWQP = [67, 68]
rWQN = [69, 70]
rEPP = [71, 72]
rEPN = [73, 74]
rEQP = [75, 76]
rWQN = [77, 78]

# Modbus configuration Options
# port name, slave address (in decimal)
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 12)
#instrument.debug = True
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1  # seconds
instrument.mode = minimalmodbus.MODE_RTU

filedir = "meterData.csv"
filedata = open(filedir, "a")

ser = serial.Serial("/dev/ttyS0")


def readreg(reg, dec):
    # Function to read a MODBUS register
    while True:
        sleep(0.1)
        try:
            return instrument.read_register(reg, dec)

        except:
            pass


def dataver():
    if frecuencia > 40 and frecuencia < 99:
        return True
    return False


def readdata():
    # Function to read all requested data
    global fechahora
    global potaparente
    global frecuencia
    global filedata

    fecha = strftime('%Y-%m-%d', localtime())
    hora = strftime('%H:%M:%S', localtime())

    fechahora = "%s %s" % (fecha, hora)
    for i in range(5):
        potaparente = readreg(rS_T,  0)
        frecuencia = readreg(rFrec, 2)
        if frecuencia < 50:
            frecuencia = 50
        if frecuencia > 70:
            frecuencia = 70
        if dataver():
            break

    # filedata.write(("%s,%5.2f,%5.2f\n")%(fechahora,potaparente,frecuencia))

    print(" ")
    print("%s" % fechahora)
    print("potaparente:", potaparente)
    print("frecuencia:", frecuencia)
    pottext = ("%d" % (int(potaparente))).rjust(4)
    fretext = "%d" % (int(frecuencia*10))
    plotext = ("%d" % (int((frecuencia-50)*9.5))).zfill(3)
    sertext = "%s%s%s\r" % (pottext, fretext, plotext)
    print(sertext)
    ser.write(sertext)


def checktime(sec):
    # Function to trigger the readdata funtion from "sec" to "sec"
    while True:
        res = round(time() % sec)
        if res == 0.0:
            readdata()
        sleep(0.2)


while True:
    checktime(1)

    #print("2500W 59.5Hz 60Hz")
    # ser.write("2500595095\r")
    # sleep(1)
