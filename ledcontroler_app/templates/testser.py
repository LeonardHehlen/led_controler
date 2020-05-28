import serial

port = "/dev/cu.usbmodem1421"

s = serial.Serial(port, 9600)

s.open()